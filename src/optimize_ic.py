import json
import os
import subprocess
from tempfile import TemporaryDirectory
import matplotlib.pyplot as plt
from scipy.optimize import minimize, Bounds
from zerodsolver import compared_PV_loops_simlated

import numpy as np
import pandas as pd

import pysvzerod

def cost_function(params,names, visual):
    # print(params)
    with open("models/RegChamberCRL_SplitPul.json", "r") as jsonFile:
        config = json.load(jsonFile)
        config["simulation_parameters"]["number_of_time_pts_per_cardiac_cycle"] = 300
        config["simulation_parameters"]["number_of_cardiac_cycles"] = 20
        x = 0
        for key in names:
            if x == 0: 
                config["initial_condition"][key] = params[0]
            elif x == 1:
                config["initial_condition"][key] = params[1]
            elif x < 4:
                config["initial_condition"][key] = params[2]
            elif x < 6:
                config["initial_condition"][key] = params[3]
            else: 
                config["initial_condition"][key] = params[4]
            x += 1

        #         "pressure:pulmonary:pul_artery": 15.39766270405246,    
        # "pressure:pul_artery:J0": 15.39766270405246,
        # "pressure:J0:Rpul_artery": 15.39766270405246,
        # "pressure:J0:Lpul_artery": 15.39766270405246,   
        # "pressure:J0a:Rpul_vein": 12.990389112964845,  
        # "pressure:J0b:Lpul_vein": 12.990389112964845,
        # "flow:pul_artery:J0": 100,   
        # "flow:Rpul_artery:J0a": 37.5977453,   
        # "flow:Lpul_artery:J0b": 37.5977453,  
        # "flow:Lpul_vein:J2a": 98.1083814496,
        # "flow:Rpul_vein:J2a": 98.1083814496

    sim_result = pysvzerod.simulate(config)
    gt_result = pysvzerod.simulate("models/RegChamberCRL_NewParams.json")
    chambers = ['pressure:left_ventricle:aortic', "pressure:left_atrium:mitral", "pressure:right_atrium:tricuspid", "pressure:right_ventricle:pulmonary",'Vc:left_atrium', 'Vc:right_atrium', 'Vc:left_ventricle', 'Vc:right_ventricle']
    mask = sim_result['name'].isin(chambers)
    sim_result = sim_result[mask]
    sim_result = sim_result.pivot(index='time', columns='name', values='y')
    sim_result = sim_result.iloc[-300:]
    mask = gt_result['name'].isin(chambers)
    gt_result = gt_result[mask]
    gt_result = gt_result.pivot(index='time', columns='name', values='y')
    gt_result = gt_result.iloc[-300:]

    # Mean Error of Pressures
    # LVError = np.sum(((sim_result.reset_index())['pressure:left_ventricle:aortic'] - (gt_result.reset_index())['pressure:left_ventricle:aortic'])**2)/300
    # LAError = np.sum(((sim_result.reset_index())['pressure:left_atrium:mitral'] - (gt_result.reset_index())['pressure:left_atrium:mitral'])**2)/300
    # RVError = np.sum(((sim_result.reset_index())['pressure:right_ventricle:pulmonary'] - (gt_result.reset_index())['pressure:right_ventricle:pulmonary'])**2)/300
    # RAError = np.sum(((sim_result.reset_index())['pressure:right_atrium:tricuspid'] - (gt_result.reset_index())['pressure:right_atrium:tricuspid'])**2)/300

    LVError = np.sqrt(np.sum(((sim_result.reset_index())['pressure:left_ventricle:aortic'] - (gt_result.reset_index())['pressure:left_ventricle:aortic'])**2+((sim_result.reset_index())['Vc:left_ventricle'] - (gt_result.reset_index())['Vc:left_ventricle'])**2))
    LAError = np.sqrt(np.sum(((sim_result.reset_index())['pressure:left_atrium:mitral'] - (gt_result.reset_index())['pressure:left_atrium:mitral'])**2+((sim_result.reset_index())['Vc:left_atrium'] - (gt_result.reset_index())['Vc:left_atrium'])**2))
    RVError = np.sqrt(np.sum(((sim_result.reset_index())['pressure:right_ventricle:pulmonary'] - (gt_result.reset_index())['pressure:right_ventricle:pulmonary'])**2+((sim_result.reset_index())['Vc:right_ventricle'] - (gt_result.reset_index())['Vc:right_ventricle'])**2))
    RAError = np.sqrt(np.sum(((sim_result.reset_index())['pressure:right_atrium:tricuspid'] - (gt_result.reset_index())['pressure:right_atrium:tricuspid'])**2+((sim_result.reset_index())['Vc:right_atrium'] - (gt_result.reset_index())['Vc:right_atrium'])**2))
    
    # Mean percent error
    # LVError = np.sum(np.abs((sim_result.reset_index())['pressure:left_ventricle:aortic'] - (gt_result.reset_index())['pressure:left_ventricle:aortic'])/(gt_result.reset_index())['pressure:left_ventricle:aortic'])/300
    # LAError = np.sum(np.abs((sim_result.reset_index())['pressure:left_atrium:mitral'] - (gt_result.reset_index())['pressure:left_atrium:mitral'])/(gt_result.reset_index())['pressure:left_atrium:mitral'])/300
    # RVError = np.sum(np.abs((sim_result.reset_index())['pressure:right_ventricle:pulmonary'] - (gt_result.reset_index())['pressure:right_ventricle:pulmonary'])/(gt_result.reset_index())['pressure:right_ventricle:pulmonary'])/300
    # RAError = np.sum(np.abs((sim_result.reset_index())['pressure:right_atrium:tricuspid'] - (gt_result.reset_index())['pressure:right_atrium:tricuspid'])/(gt_result.reset_index())['pressure:right_atrium:tricuspid'])/300

    visual.loc[len(visual.index)] = [LVError,RVError,LAError, RAError]
    # error = LAError
    error = LAError + LVError + RVError + RVError
    print(params, error)
    return error

def optimize_heart_chamber():
    names = {"pressure:aortic:sys_artery": 63.469005164828886,
        "pressure:J2:sys_vein": 23.489460083645984, 
        "pressure:J0:Rpul_artery": 15.39766270405246,
        "pressure:J0:Lpul_artery": 15.39766270405246, 
        "pressure:J0a:Rpul_vein": 12.990389112964845,  
        "pressure:J0b:Lpul_vein": 12.990389112964845,        
        "pressure:Rpul_vein:J2a": 6.990389112964845,  
        "pressure:Lpul_vein:J2a": 6.990389112964845}
    initial_params = [63.469005164828886, 23.489460083645984, 15.39766270405246, 12.990389112964845,6.358519599789586]
    error = {"LV" : [],"RV" : [],"LA" : [],"RA" : []}
    visual = pd.DataFrame(data=error)
    bounds = [
        (0, 73),
        (0, 33),
        (0, 25),
        (0, 22),
        (0, 17)
    ]
    
    # Perform the optimization
    result = minimize(cost_function, initial_params, args=(names,visual), bounds=bounds, method='Nelder-Mead')
    visual.plot()
    plt.show()
    # Extract the optimized parameters
    optimized_params = result.x

    with open("models/RegChamberCRL_SplitPul.json", "r") as jsonFile:
        config = json.load(jsonFile)
        x = 0
        for key in names:
            if x == 0:
                config["initial_condition"][key] = optimized_params[0]
            elif x == 1:
                config["initial_condition"][key] = optimized_params[1]
            elif x < 4:
                config["initial_condition"][key] = optimized_params[2]
            elif x < 6:
                config["initial_condition"][key] = optimized_params[3]
            else: 
                config["initial_condition"][key] = optimized_params[4]
            x += 1
    sim_result = pysvzerod.simulate(config)
    compared_PV_loops_simlated(sim_result)
    return optimized_params

optimized_params = optimize_heart_chamber()
print("Optimized Parameters:", optimized_params)