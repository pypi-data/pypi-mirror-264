import sys
import cvxopt
from cvxopt import matrix
import numpy as np
import platform
import tensorflow as tf
import tensorflow.keras as keras
from tensorflow.keras.layers import Dense, Input, ReLU, Softmax
from sklearn.model_selection import train_test_split

class BFS(keras.Model):
    '''
        Implementation of a constrained biobjective gradient descent neural network for feature selection purposes
        that works for High Dimensions Low Sample datasets. The method extends the Model class from keras. The two losses are 
        the cross entropy and the sparse group lasso. 
        Requires keras, numpy, scikit-learn and cvxopt. 
        Returns a sparse neural network with an importance score for each feature. 
    '''

    def __init__(self, n_attr, pref_vector1, pref_vector2, n_hidden=[100,200], n_output=2):
        '''
            Model initialization function 
            Args: 
                n_attr: number of attributes
                pref_vector1: first preference vector delimiting the region
                pref_vector2: second preference vector delimiting the region
                n_hidden: number of neurons in each layer
                n_output: number of classes
        '''
        super().__init__()
        self.n_hidden = n_hidden
        self.n_attr = n_attr
        self.n_output = n_output

        self.preference_vector1 = pref_vector1
        self.preference_vector2 = pref_vector2
        z1 = [ self.preference_vector1[1], -self.preference_vector1[0]]
        z2 = [ - self.preference_vector2[1], self.preference_vector2[0]]
        self.z = tf.constant([z1, z2], tf.float32)
        
        self.train_indicator = tf.Variable(False, trainable=False)
        self.f_init = tf.Variable([0.0,0.0], shape = (2,), trainable=False)
        
        # Neural network architecture
        self.hidden_layers = self.create_hidden_layers()
        self.out = self.create_output_layers()
  
        
    def call(self, inputs):
        x = inputs 
        for layer in self.hidden_layers:
            x = layer(x)
        for layer in self.out:
            x = layer(x)
        return x
    
    def create_output_layers(self):
        output_layers = []
        output_layers.append(Dense(units= self.n_output, name = "output_layer"))
        output_layers.append(Softmax())
        return output_layers

    def create_hidden_layers(self): 
        hidden_layers = []
        for i, y in enumerate(self.n_hidden):
            hidden_layers.append(Dense(y, name = f'Hidden_{i}'))
            hidden_layers.append(ReLU())
        return hidden_layers
    
    def optimizer_to_use(self, optimizer_name, learning_rate, **kwargs):
        if platform.system() == "Darwin" and platform.processor() == "arm":
            optimizers_mac = { 
                        'Adam' : tf.keras.optimizers.legacy.Adam(learning_rate), 
                        'Adadelta' : tf.keras.optimizers.legacy.Adadelta(learning_rate),
                        'Adagrad' : tf.keras.optimizers.legacy.Adagrad(learning_rate),
                        'SGD' : tf.optimizers.legacy.SGD(learning_rate), 
                        'Momentum' : tf.optimizers.legacy.SGD(learning_rate, kwargs.get('momentum', 0.8)), 
                        }
            return optimizers_mac[optimizer_name]
        else:
                    
            optimizers_linux = { 
                        'Adam' : tf.keras.optimizers.Adam(learning_rate), 
                        'Adadelta' : tf.keras.optimizers.Adadelta(learning_rate),
                        'Adagrad' : tf.keras.optimizers.Adagrad(learning_rate),
                        'SGD' : tf.optimizers.SGD(learning_rate), 
                        'Momentum' : tf.optimizers.SGD(learning_rate, kwargs.get('momentum', 0.8)), 
                        }
            return optimizers_linux[optimizer_name]
        
        
    def compile(self, init_optimizer = 'Adam', train_optimizer='Adam', init_learning_rate = 0.01, train_learning_rate=0.01, metrics = ['accuracy'], **kwargs): 
        '''
            We define two different optimizers with different learning rates for the initialization and training steps.
        '''
        
        try: 
            self.init_optimizer = self.optimizer_to_use(init_optimizer, init_learning_rate, **kwargs)
        except ValueError:
            raise ValueError('Init optimizer choice not available/syntax error. Only SGD, Momentum, Adam, Adagrad and Adadelta are acceptable')   
        try: 
            self.train_optimizer = self.optimizer_to_use(init_optimizer, train_learning_rate, **kwargs)
        except ValueError:
            raise ValueError('Train optimizer choice not available/syntax error. Only SGD, Momentum, Adam, Adagrad and Adadelta are acceptable')
        super().compile(metrics=metrics)

    
    @tf.function
    def train_step(self, data):
        '''
            Just like in keras.Model, train_step is the function called by fit.
            Args:
                data 
            Returns:
                dictionary with the different metrics and losses
        '''
        if (len(data) == 2):
            X_train, y_train = data
        elif len(data) == 3:
            X_train, y_train, _ = data
        else:
            raise ValueError(f"Invalid input size.  {len(data)} not compatible with 2 or 3")

        train_index = 0
        if tf.equal(self.train_indicator, True):
            train_index = 1
 
        with tf.GradientTape() as tape1, tf.GradientTape() as tape2:
            output = self(X_train)
            losses = self.compute_losses(y_train, output, self.trainable_variables, train_index)
        
        grad1 = tape1.gradient(losses[0], self.trainable_variables)
        grad2 = tape2.gradient(losses[1], self.trainable_variables)
        
        grad_shapes = [g.shape for g in grad1]
        shapes_prod = [np.prod(s) for s in grad_shapes]
        grad1 = [tf.reshape(g, [-1]) for g in grad1]
        grad1 = tf.concat(grad1, axis = 0)
        grad2 = [tf.reshape(g, [-1]) for g in grad2]
        grad2 = tf.concat(grad2, axis =0) 
        grads = tf.stack([grad1, grad2])
   
        # Calculate constraints
        constraints = - tf.tensordot(self.z, losses[2] , axes=1 )
        unverified_constraint = tf.math.greater(constraints , 0)
        nonzero_unverified_constraint = tf.where(tf.not_equal(unverified_constraint, False))
        
        if tf.equal(self.train_indicator, True):
            # if the network is in the train step
            grad = []
            if tf.reduce_sum(tf.cast(unverified_constraint, tf.int32)) == 0:
                # if the network is in its region, calculate direction
                grad = tf.numpy_function(self.solve_qp, [grads], np.float32)
    
            else:
                # if the network is not in its region, calculate third objective then direction
                unverified_z = self.z[nonzero_unverified_constraint[0][0]]
                grad3 = [- tf.tensordot(tf.transpose(grads), unverified_z, axes = 1)] 
                gradients = tf.concat((grads, grad3), axis = 0)
                grad = tf.numpy_function(self.solve_qp, [gradients], np.float32)
                
            grad = tf.split(grad, shapes_prod)
            grad = [tf.reshape(g,s) for g,s in zip(grad, grad_shapes)]
            self.train_optimizer.apply_gradients(zip(grad, self.trainable_variables))            

        else:
            # if the network is in the init step
            grad = []
            if tf.reduce_sum(tf.cast(unverified_constraint, tf.int32)) == 0:
                # if the network is in its region, gradient = 0 (no more change)
                grad = tf.zeros(grad1.shape, dtype=tf.float32)
              
            else:
                # if the network is not in its region, calculate gradient
                unverified_z = self.z[nonzero_unverified_constraint[0][0]]
                grad = - tf.tensordot(tf.transpose(grads),unverified_z,axes = 1)
                
            grad = tf.split(grad, shapes_prod)
            grad = [tf.reshape(g,s) for g,s in zip(grad, grad_shapes)]
            
            # update weights
            self.init_optimizer.apply_gradients(zip(grad, self.trainable_variables))

        # update metrics and history dictionary
        self.compiled_metrics.update_state(y_train, output)
        hist = { m.name : m.result() for m in self.metrics }
        hist['loss_ce'] = losses[2][0]
        hist['loss_sgl'] = losses[2][1]
        hist['loss_ce_norm'] = losses[0]
        hist['loss_sgl_norm'] = losses[1]
        
        return hist

    def model(self):
        '''
            Instantiate a neural network. 
            Returns: 
                A keras.Model instance
        '''
        x = Input(shape=(self.n_attr), name='Input')
        output = self.call(x)
        return tf.keras.Model(inputs=[x],
                                     outputs=[output],
                                     name='BFS')
        
    def solve_qp(self, vecs):
        '''
            Function to solve the multiobjective optimization problem in order to find the descent 
            direction. We rewrite the problem to a quadratic problem and solve it using cvxopt.
            Args: 
                List of gradients
            Returns: 
                Optimal descent direction 
        '''
        
        nobj, dim = vecs.shape
        P_temp = np.dot(vecs, vecs.T)
        P = matrix(np.dot(vecs, vecs.T).astype(np.double))
        q = matrix(np.zeros(nobj))
        G = matrix(- np.eye(nobj))
        h = matrix(np.zeros(nobj))
        A = matrix(np.ones(nobj).reshape(1, nobj))
        b = matrix(np.ones(1))
        cvxopt.solvers.options['kktreg'] =  1e-9
        cvxopt.solvers.options['show_progress'] = False
        sol = cvxopt.solvers.qp(P,q,G,h,A,b, kktsolver="chol")
        sol = np.array(sol['x']).reshape((P_temp.shape[1],))
        direction = 0
        
        for i in range(len(sol)):
            direction += sol[i] * vecs[i]
        return direction        

    @tf.function 
    def test_step(self, data):
        '''
            Just like in keras, the test_step function is called by the predict() function in BFS.
            Args: 
                test data
            Returns:
                dictionary with all metrics and losses values. 
        '''
        if (len(data) == 2):
            X_test, y_test = data
        elif len(data) == 3:
            X_test, y_test, _ = data
        else:
            raise ValueError(f"Invalid input size.  {len(data)} not compatible with 2 or 3")

        train_index = 0
        if tf.equal(self.train_indicator, True):
            train_index = 1

        pred_out = self(X_test, training=False)  # forward pass
        losses = self.compute_losses(y_test, pred_out, self.trainable_variables, train_index)
        # Update metrics and history dictionary
        self.compiled_metrics.update_state(y_test, pred_out)
        hist = { m.name : m.result() for m in self.metrics }
        hist['loss_ce'] = losses[2][0]
        hist['loss_sgl'] = losses[2][1]
        hist['loss_ce_norm'] = losses[0]
        hist['loss_sgl_norm'] = losses[1]
        return hist
    
    def fit(self, X, y, **kwargs):
        '''
            Same function as in keras. fit() is used to train the model.
            Args: 
                (X,y): train dataset
                validation data: validation dataset
            Returns: 
                History dictionary with metrcis and losses' values at each iteration. 
                
        '''
        self.n_epochs = kwargs.get('epochs', 500)

        if 'validation_data' not in kwargs.keys():
            self.X, data_val, self.y, target_val = train_test_split(
                X,
                y,
                test_size=kwargs.get('validation_split', 0.2),
                stratify=y)
        else:
            self.X, self.y = X, y
            data_val, target_val = kwargs['validation_data']

        hist = super().fit(
            self.X,
            self.y,
            validation_data=(data_val, target_val),
            epochs=self.n_epochs,
            batch_size=kwargs.get('batch_size', 32),
            verbose=kwargs.get('verbose', 0),
            callbacks=[checkTrain(self)] + kwargs.get('callbacks', []),
            workers=kwargs.get('workers', 1)) 
        return hist

    def l21_norm(self, W):
        '''
            Function that calculates l21 norm for a group of neurons
            Args: 
                Group weights'
            Returns: 
                l21 norm for the group
        '''
        return tf.reduce_sum(tf.norm(W, axis = 1))
    
    def get_group_regularization(self, variables):
        '''
            Function that calculates the group lasso for a network. Group lasso is needed to 
            calculate the sparse group lasso of the network. The sparse group lasso is only applied on the 
            weights and not on the biases. Inspired from the code provided by Scardapane et al. 
            Args: 
                Network's weights
            Returns: 
                Group lasso value of the network
        '''
        const_coeff = lambda W: tf.sqrt(tf.cast(W.get_shape().as_list()[1], tf.float32))
        return tf.reduce_sum([tf.multiply(const_coeff(W), self.l21_norm(W)) for W in variables if 'bias' not in W.name and 'normalization' not in W.name])

    def get_L1_norm(self, variables):
        '''
            Function that calculates the lasso value of a network. The l1 is needed to calculate 
            the sparse group lasso of the network. The l1 norm is applied on both weights and biases.
            Args: 
                Network's weights
            Returns:
                lasso value of the network
            
        '''
        variables = [tf.reshape(v, [-1]) for v in variables]
        variables = tf.concat(variables, axis = 0)
        return tf.norm(variables, ord = 1)

    def sparse_group_lasso(self, variables): 
        '''
            Function that calls both get_group_regularization and get_l1_norm  in order to calculate
            the sparse group lasso of the network. 
            Args: 
                Network's weights
            Returns:
                sparse group lasso value of the network
        '''
        sparse_lasso = self.get_group_regularization(variables) + self.get_L1_norm(variables)
        return sparse_lasso

    def compute_losses(self, y_train, output, variables, train_index):
        '''
            Function called by train_step and test_step to compute the losses of the neural network. It calls 
            the sparse group lasso function. It normalizes the two objectives before computing the values 
            of the losses. 
            Args: 
                True labels of the dataset
                Predicted labels of the dataset
                Network's weights
                Boolean indicating whether it's the init or training step
            Returns:
                List of both  normalized and unnormalized losses
                
        '''
        ce_loss = tf.reduce_mean(tf.keras.losses.categorical_crossentropy(y_train, output))
        sgl_loss = self.sparse_group_lasso(variables)
        losses = [ce_loss, sgl_loss] 
        losses_norm= []
        if train_index == 1:
            # train step normalization 
            losses_norm = losses/tf.norm(self.f_init) 
        else: 
            # Init step normalization
            losses_norm = losses/tf.norm(losses)
        return [losses_norm[0], losses_norm[1], losses]

class checkTrain(keras.callbacks.Callback):
    '''
        Class that inherits from the keras Callback class. The purpose of this class is to set the train indicater to 
        the train step after a certain number of epochs has passed. It also allows to set the value of the init cross entropy 
        and sparse group lasso values to be used by compute_losses() in the training normalization step.
    '''
    def __init__(self, model):
        self.model = model

    def on_epoch_end(self,epoch, logs = None):
        if epoch == self.model.n_epochs * 0.2:
            tf.keras.backend.set_value(self.model.train_indicator, True)
            logs = logs or {}
            f_init_ce = logs.get("loss_ce")
            f_init_sgl = logs.get("loss_sgl")
            tf.keras.backend.set_value(self.model.f_init, [f_init_ce, f_init_sgl])
        