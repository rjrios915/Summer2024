import json
import os
import subprocess
from tempfile import TemporaryDirectory
import matplotlib.pyplot as plt
from scipy.optimize import minimize, Bounds

import numpy as np
import pandas as pd

import pysvzerod

def cost_function(params, visual):
    # print(params)
    with open("models/RegChamberCRL_SplitPul.json", "r") as jsonFile:
        config = json.load(jsonFile)
        config["simulation_parameters"]["number_of_time_pts_per_cardiac_cycle"] = 100
        config["simulation_parameters"]["number_of_cardiac_cycles"] = 10
        config['vessels'][0]["zero_d_element_values"]['C'] = params[0]
        config['vessels'][0]["zero_d_element_values"]['R_poiseuille'] = params[2]
        config['vessels'][1]["zero_d_element_values"]['C'] = params[0]
        config['vessels'][1]["zero_d_element_values"]['R_poiseuille'] = params[2]
        config['vessels'][2]["zero_d_element_values"]['C'] = params[1]
        config['vessels'][2]["zero_d_element_values"]['R_poiseuille'] = params[3]
        config['vessels'][3]["zero_d_element_values"]['C'] = params[1]
        config['vessels'][3]["zero_d_element_values"]['R_poiseuille'] = params[3]

    sim_result = pysvzerod.simulate(config)
    gt_result = pysvzerod.simulate("models/RegChamberCRL_NewParams.json")
    chambers = ['Vc:left_ventricle', "Vc:left_atrium", "Vc:right_atrium", "Vc:right_ventricle"]
    mask = sim_result['name'].isin(chambers)
    sim_result = sim_result[mask]
    sim_result = sim_result.pivot(index='time', columns='name', values='y')
    sim_result = sim_result.iloc[-300:]
    mask = gt_result['name'].isin(chambers)
    gt_result = gt_result[mask]
    gt_result = gt_result.pivot(index='time', columns='name', values='y')
    gt_result = gt_result.iloc[-300:]

    #Mean Error
    # LVError = np.sum(((sim_result.reset_index())['Vc:left_ventricle'] - (gt_result.reset_index())['Vc:left_ventricle'])**2)/300
    # LAError = np.sum(((sim_result.reset_index())['Vc:left_atrium'] - (gt_result.reset_index())['Vc:left_atrium'])**2)/300
    # RVError = np.sum(((sim_result.reset_index())['Vc:right_ventricle'] - (gt_result.reset_index())['Vc:right_ventricle'])**2)/300
    # RAError = np.sum(((sim_result.reset_index())['Vc:right_atrium'] - (gt_result.reset_index())['Vc:right_atrium'])**2)/300

    #
    LVError = np.sum(np.abs((sim_result.reset_index())['Vc:left_ventricle'] - (gt_result.reset_index())['Vc:left_ventricle'])/(gt_result.reset_index())['Vc:left_ventricle'])*3
    LAError = np.sum(np.abs((sim_result.reset_index())['Vc:left_atrium'] - (gt_result.reset_index())['Vc:left_atrium'])/(gt_result.reset_index())['Vc:left_atrium'])*3
    RVError = np.sum(np.abs((sim_result.reset_index())['Vc:right_ventricle'] - (gt_result.reset_index())['Vc:right_ventricle'])/(gt_result.reset_index())['Vc:right_ventricle'])*3
    RAError = np.sum(np.abs((sim_result.reset_index())['Vc:right_atrium'] - (gt_result.reset_index())['Vc:right_atrium'])/(gt_result.reset_index())['Vc:right_atrium'])*3

    visual.loc[len(visual.index)] = [LVError,RVError,LAError, RAError]
    error = LVError + LAError + RVError + RAError
    print(error)
    return error

def optimize_heart_chamber():
    initial_params = [5, 8, 0.064, 0.07]
    error = {"LV" : [],"RV" : [],"LA" : [],"RA" : []}
    visual = pd.DataFrame(data=error)
    bounds = Bounds(lb=[1.0, 1.0,0,0])
        
        
    #     [
    #     (0, 40),    # Emax
    #     (0, 64),   # Emin
    #     (0, 0.1), # Vrd
    #     (0, 0.1), # Vrs
    # ]
    
    # Perform the optimization
    result = minimize(cost_function, initial_params, args=(visual), bounds=bounds, method='Nelder-Mead')
    visual.plot()
    plt.show()
    # Extract the optimized parameters
    optimized_params = result.x
    return optimized_params

optimized_params = optimize_heart_chamber()
print("Optimized Parameters:", optimized_params)