Biobjective gradient descent for Feature Selection (BFS)
==========================================================

Code for BFS, a biobjective gradient descent feature selection method based on network sparsification. 

Installation
--------------
To install BFS from git, clone the project using the following command: 

::

    git clone https://forge.ibisc.univ-evry.fr/tissa/BFS/tree/master/BFS.git

To reproduce the conda environment with the required packages and appropriate versions,
use the following command: 

For Mac users: 
::

    conda env create -f BFS_mac.yml

For Linux users:
::

    conda env create -f BFS_linux.yml


To install BFS using pip:

:: 

    pip install BGFS

Usage
------
If downloaded using git, before using BFS, first go to the source files' directory using the following command:

::

    cd BFS/source


From there or when downloaded with pip, BFS can be loaded in a python script as any other module using the ``import`` command.
BFS can be used with the following commands:

::

    from BGFS.BFS import BFS

    model = BFS(n_attr, pref_vector1, pref_vector2, n_hidden, n_output)
    model.compile(init_optimizer, train_optimizer, init_learning_rate, train_learning_rate, metrics)
    model.fit(X_train, y_train, validation_data=(X_val, y_val))


Documentation
---------------
BFS documentation can be found on: https://bfss.readthedocs.io/

License
--------
BFS was created by Tina Issa. It is licensed under the terms
of the MIT license.

