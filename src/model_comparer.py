import json
import os
import subprocess
from tempfile import TemporaryDirectory
import matplotlib.pyplot as plt
import sys

import numpy as np
import pandas as pd

import pysvzerod

# Performs comparison on already simulated result
def compared_PV_loops_simlated(result):
    sim_chambers = ['Vc:left_atrium', 'pressure:left_atrium:mitral','Vc:right_atrium', 'pressure:right_atrium:tricuspid','Vc:left_ventricle', 'pressure:left_ventricle:aortic','Vc:right_ventricle', 'pressure:right_ventricle:pulmonary']
    gt_chambers = ['V_LA', 'p_LA', 'V_RA', 'p_RA', 'V_LV', 'p_LV', 'V_RV','p_RV']
    mask = result['name'].isin(sim_chambers)
    filtered_df = result[mask]
    filtered_df = filtered_df.pivot(index='time', columns='name', values='y')
    filtered_df = filtered_df.iloc[-689:]

    gt = pd.read_csv("cardiac_PV.csv")
    gt = gt.iloc[-689:]

    LA = gt[["p_LA","V_LA"]]
    a = LA.plot(x="V_LA",y="p_LA", label="LA GT", color="black")
    RA = gt[["p_RA","V_RA"]]
    RA.plot(x="V_RA",y="p_RA", ax=a, label="RA GT",color="black")

        
    a = filtered_df.plot(x='Vc:left_atrium',y='pressure:left_atrium:mitral', label="LA Sim", ax=a)
    filtered_df.plot(x='Vc:right_atrium',y='pressure:right_atrium:tricuspid',ax=a, label="RA Sim")


    
    plt.title("Atria PV Curves")
    plt.xlabel("Atrial Volume (mL)")
    plt.ylabel("Artial Pressure (mmHg)")

    LV = gt[["p_LV","V_LV"]]
    b = LV.plot(x="V_LV",y="p_LV", label="LV GT",color="black")
    RV = gt[["p_RV","V_RV"]]
    RV.plot(x="V_RV",y="p_RV", ax=b, label="RV GT",color="black")

    filtered_df.plot(x='Vc:left_ventricle',y='pressure:left_ventricle:aortic', ax=b,  label="LV Sim")
    filtered_df.plot(x='Vc:right_ventricle',y='pressure:right_ventricle:pulmonary',ax=b, label="RV Sim")


    plt.title("Right Ventricle PV Curve")
    plt.xlabel("Right Ventricle Volume (mL)")
    plt.ylabel("Right Ventricle Pressure (mmHg)")

    # Calcualtes percent error
    # for i in range(8):
    #     error = ((filtered_df).reset_index()[sim_chambers[i]] - (gt).reset_index()[gt_chambers[i]])/(gt).reset_index()[gt_chambers[i]]
    #     maximum = (np.abs(error)).max()
    #     print(f"{gt_chambers[i]} max perecent error is {maximum*100}%")
    #     # print(f"the index is {np.abs(error).to_list().index(maximum)}")
    #     # # print(error.to_string())
    #     # print(f"{gt_chambers[i]} error is {(np.sqrt(np.sum(error)/689))}")
    
    plt.show()

# Outputs simulated and ground truth PV Curves from json
def PV_loops(file):
    result = pysvzerod.simulate(file)
    sim_chambers = ['Vc:left_atrium', 'pressure:left_atrium:mitral','Vc:right_atrium', 'pressure:right_atrium:tricuspid','Vc:left_ventricle', 'pressure:left_ventricle:aortic','Vc:right_ventricle', 'pressure:right_ventricle:pulmonary']
    gt_chambers = ['V_LA', 'p_LA', 'V_RA', 'p_RA', 'V_LV', 'p_LV', 'V_RV','p_RV']
    mask = result['name'].isin(sim_chambers)
    filtered_df = result[mask]
    filtered_df = filtered_df.pivot(index='time', columns='name', values='y')
    filtered_df = filtered_df.iloc[-689:]

    gt = pd.read_csv("cardiac_PV.csv")
    gt = gt.iloc[-689:]

    LA = gt[["p_LA","V_LA"]]
    a = LA.plot(x="V_LA",y="p_LA", label="LA GT", color="black")
    RA = gt[["p_RA","V_RA"]]
    RA.plot(x="V_RA",y="p_RA", ax=a, label="RA GT",color="black")

        
    a = filtered_df.plot(x='Vc:left_atrium',y='pressure:left_atrium:mitral', label="LA Sim", ax=a)
    filtered_df.plot(x='Vc:right_atrium',y='pressure:right_atrium:tricuspid',ax=a, label="RA Sim")
    
    plt.title("Atria PV Curves")
    plt.xlabel("Atrial Volume (mL)")
    plt.ylabel("Artial Pressure (mmHg)")

    LV = gt[["p_LV","V_LV"]]
    b = LV.plot(x="V_LV",y="p_LV", label="LV GT",color="black")
    RV = gt[["p_RV","V_RV"]]
    RV.plot(x="V_RV",y="p_RV", ax=b, label="RV GT",color="black")

    filtered_df.plot(x='Vc:left_ventricle',y='pressure:left_ventricle:aortic', ax=b,  label="LV Sim")
    filtered_df.plot(x='Vc:right_ventricle',y='pressure:right_ventricle:pulmonary',ax=b, label="RV Sim")


    plt.title("Right Ventricle PV Curve")
    plt.xlabel("Right Ventricle Volume (mL)")
    plt.ylabel("Right Ventricle Pressure (mmHg)")

    # Calcualtes percent error
    # for i in range(8):
    #     error = ((filtered_df).reset_index()[sim_chambers[i]] - (gt).reset_index()[gt_chambers[i]])/(gt).reset_index()[gt_chambers[i]]
    #     maximum = (np.abs(error)).max()
    #     print(f"{gt_chambers[i]} max perecent error is {maximum*100}%")
    #     # print(f"the index is {np.abs(error).to_list().index(maximum)}")
    #     # # print(error.to_string())
    #     # print(f"{gt_chambers[i]} error is {(np.sqrt(np.sum(error)/689))}")
    
    plt.show()

#Compares pressure vs. time curves
def PvT(file):
    result = pysvzerod.simulate(file)

    sim_chambers = ['pressure:left_atrium:mitral','pressure:right_atrium:tricuspid', 'pressure:left_ventricle:aortic', 'pressure:right_ventricle:pulmonary']
    gt_chambers = ['p_LA','p_RA', 'p_LV', 'p_RV']
    mask = result['name'].isin(sim_chambers)
    filtered_df = result[mask]
    filtered_df = filtered_df.pivot(index='time', columns='name', values='y').reset_index()
    filtered_df = filtered_df.iloc[-689:]

    gt = pd.read_csv("cardiac_PV.csv")
    gt = gt.iloc[-689:]

    for i in range(4):
        ax = filtered_df.plot(x='time',y=sim_chambers[i])
        LV = gt[[gt_chambers[i],"time"]]
        LV.plot(x="time",y=gt_chambers[i], ax=ax)
        plt.title(gt_chambers[i])
        plt.savefig(gt_chambers[i])
    plt.show()

#Compares volume vs. time curves
def VvT(file):
    result = pysvzerod.simulate(file)

    sim_chambers = ['Vc:left_atrium', 'Vc:right_atrium', 'Vc:left_ventricle', 'Vc:right_ventricle']
    gt_chambers = ['V_LA','V_RA', 'V_LV', 'V_RV']
    mask = result['name'].isin(sim_chambers)
    filtered_df = result[mask]
    filtered_df = filtered_df.pivot(index='time', columns='name', values='y').reset_index()
    filtered_df = filtered_df.iloc[-689:]
    print(filtered_df)

    gt = pd.read_csv("cardiac_PV.csv")
    gt = gt.iloc[-689:]

    for i in range(4):
        ax = filtered_df.plot(x='time',y=sim_chambers[i])
        LV = gt[[gt_chambers[i],"time"]]
        LV.plot(x="time",y=gt_chambers[i], ax=ax)
        plt.title(gt_chambers[i])
        plt.savefig(gt_chambers[i])
    plt.show()

def main():
    file = "models/RegChamberCRL_SplitPulmonary.json"
    if len(sys.argv) > 1:
        function = sys.argv[1]
        if function == "PV_loops":
            compared_PV_loops(file)
        elif function == "PvT":
            compared_PvT(file)
        elif function == "VvT":
            compared_VvT(file)
        else:
            print("please enter a a valid function:")
            print("PV_loops, PvT, VvT")
    else:
        print("Include the following arugments: [function]")

if __name__ == "__main__":
    main()

