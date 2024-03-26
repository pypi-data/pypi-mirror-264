import numpy as np
import pandas as pd


def circle_points(r, n):
    circles = []
    for r,n in zip(r, n):
        t = np.linspace(0, 0.5*np.pi, n)
        x = 1 * np.cos(t)
        y = 1 * np.sin(t)
        circles.append(np.c_[x,y])
    return circles

def s_score(network_weights, sparsity_level, bfs_bool):
    sum_null_weights = 0
    sum_all_weights = 0
    sparsity = 0
    if bfs_bool == True:
        for i in range(0, len(network_weights)-2):
            sum_null_weights += np.sum(np.abs(network_weights[i]) < sparsity_level)
            if len(network_weights[i].shape) == 1:
                sum_all_weights += network_weights[i].shape[0]
            else:
                sum_all_weights += network_weights[i].shape[0] * network_weights[i].shape[1] 
        sparsity = sum_null_weights / (sum_all_weights)
    else :
        for i in range(0, len(network_weights)):
            sum_null_weights += np.sum(np.abs(network_weights[i]) < sparsity_level)
            if len(network_weights[i].shape) == 1:
                sum_all_weights += network_weights[i].shape[0]
            else:
                sum_all_weights += network_weights[i].shape[0] * network_weights[i].shape[1]
        sparsity = sum_null_weights / (sum_all_weights)
    return sparsity

def average_fs_score(network_weights, features_name, relevant_features):
    ind_ifwr = np.sum(np.abs(network_weights[0]), axis = 1)
    ifwr_results = pd.DataFrame(ind_ifwr, columns = ['ifwr'] ,index= features_name)
    ifwr_results = ifwr_results.sort_values(by='ifwr', ascending = False)
    count = 0
    for x in ifwr_results.index.to_numpy():
        if x in relevant_features:
            count += ifwr_results.T[x].to_numpy() 
    fs_score = count / ifwr_results.sum().to_numpy()
    return fs_score

def individual_fs_score(network_weights, features_name):
    ind_ifwr = np.sum(np.abs(network_weights[0]), axis = 1)
    ifwr_results = pd.DataFrame(ind_ifwr, columns = ['ifwr'] ,index= features_name)
    fs_score = []
    
    for x in ifwr_results.index.to_numpy():
        feature_score = ifwr_results.T[x].to_numpy() 
        fs_score.append(feature_score)
        
    fs_score_df = pd.DataFrame(ind_ifwr, columns = ['feature_score'] ,index= features_name)
    fs_score_df = fs_score_df.sort_values(by='feature_score', ascending = False)
    return fs_score_df
