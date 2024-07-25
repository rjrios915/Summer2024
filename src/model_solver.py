import json
import os
import subprocess
from tempfile import TemporaryDirectory
import matplotlib.pyplot as plt
import sys

import numpy as np
import pandas as pd

import pysvzerod

def sperate_PV_Loops(file):
    result = pysvzerod.simulate(file)

    mask = result['name'].isin(['Vc:left_atrium', 'pressure:left_atrium:mitral'])
    filtered_df = result[mask]
    filtered_df = filtered_df.pivot(index='time', columns='name', values='y')
    a = filtered_df.plot(x='Vc:left_atrium',y='pressure:left_atrium:mitral')
    a.get_legend().remove()
    plt.title("Left Atrium PV Curve")
    plt.xlabel("Left Atrium Volume (mL)")
    plt.ylabel("Left Atrium Pressure (mmHg)")
    plt.savefig("Left_Atrium")

    mask = result['name'].isin(['Vc:left_ventricle', 'pressure:left_ventricle:aortic'])
    filtered_df = result[mask]
    filtered_df = filtered_df.pivot(index='time', columns='name', values='y')
    b = filtered_df.plot(x='Vc:left_ventricle',y='pressure:left_ventricle:aortic')
    b.get_legend().remove()
    plt.title("Left Ventricle PV Curve")
    plt.xlabel("Left Ventricle Volume (mL)")
    plt.ylabel("Left Ventricle Pressure (mmHg)")
    plt.savefig("Left_Ventricle")

    mask = result['name'].isin(['Vc:right_atrium', 'pressure:right_atrium:tricuspid'])
    filtered_df = result[mask]
    filtered_df = filtered_df.pivot(index='time', columns='name', values='y')
    a = filtered_df.plot(x='Vc:right_atrium',y='pressure:right_atrium:tricuspid')
    a.get_legend().remove()
    plt.title("Right Atrium PV Curve")
    plt.xlabel("Right Atrium Volume (mL)")
    plt.ylabel("Right Atrium Pressure (mmHg)")
    plt.savefig("Right_Atrium")

    mask = result['name'].isin(['Vc:right_ventricle', 'pressure:right_ventricle:pulmonary'])
    filtered_df = result[mask]
    filtered_df = filtered_df.pivot(index='time', columns='name', values='y')
    b = filtered_df.plot(x='Vc:right_ventricle',y='pressure:right_ventricle:pulmonary')
    b.get_legend().remove()
    plt.title("Right Ventricle PV Curve")
    plt.xlabel("Right Ventricle Volume (mL)")
    plt.ylabel("Right Ventricle Pressure (mmHg)")
    plt.savefig("Right_Ventricle")

    plt.show()

def combined_PV_Loops(file):

    file = "models/RegChamberCRL_NewParams.json"
    result = pysvzerod.simulate(file)

    LAmask = result['name'].isin(['Vc:left_atrium', 'pressure:left_atrium:mitral'])
    filtered_df = result[LAmask]
    filtered_df = filtered_df.pivot(index='time', columns='name', values='y')
    a = filtered_df.plot(x='Vc:left_atrium',y='pressure:left_atrium:mitral', label="left atrium")

    RAmask = result['name'].isin(['Vc:right_atrium', 'pressure:right_atrium:tricuspid'])
    filtered_df = result[RAmask]
    filtered_df = filtered_df.pivot(index='time', columns='name', values='y')
    filtered_df.plot(x='Vc:right_atrium',y='pressure:right_atrium:tricuspid',ax=a, label="right atrium")
    a.get_legend().remove()

    plt.title("Atria PV Curves")
    plt.xlabel("Atrial Volume (mL)")
    plt.ylabel("Artial Pressure (mmHg)")

    LVmask = result['name'].isin(['Vc:left_ventricle', 'pressure:left_ventricle:aortic'])
    filtered_df = result[LVmask]
    filtered_df = filtered_df.pivot(index='time', columns='name', values='y')
    a = filtered_df.plot(x='Vc:left_ventricle',y='pressure:left_ventricle:aortic',  label="left ventricle")

    RVmask = result['name'].isin(['Vc:right_ventricle', 'pressure:right_ventricle:pulmonary'])
    filtered_df = result[RVmask]
    filtered_df = filtered_df.pivot(index='time', columns='name', values='y')
    filtered_df.plot(x='Vc:right_ventricle',y='pressure:right_ventricle:pulmonary',ax=a, label="right ventricle")
    a.get_legend().remove()
    plt.title("Right Ventricle PV Curve")
    plt.xlabel("Right Ventricle Volume (mL)")
    plt.ylabel("Right Ventricle Pressure (mmHg)")
    plt.show()


def VvT(file):
    df = pysvzerod.simulate(file)

    filtered_df = df[(df['name'] == "Vc:left_atrium")]
    bx = filtered_df.plot(x="time", y="y",label="LA")
    filtered_df = df[(df['name'] == "Vc:left_ventricle")]
    filtered_df.plot(x="time", y="y",label="LV", ax=bx)
    filtered_df = df[(df['name'] == "Vc:right_atrium")]
    filtered_df.plot(x="time", y="y", ax=bx,label="RA")
    filtered_df = df[(df['name'] == "Vc:right_ventricle")]
    filtered_df.plot(x="time", y="y", ax=bx,label="RV")
    plt.show()


def PvT(file):
    df = pysvzerod.simulate(file)
    filtered_df = df[(df['name'] == "pressure:left_ventricle:aortic")]
    bx = filtered_df.plot(x="time", y="y")
    filtered_df = df[(df['name'] == "pressure:right_ventricle:pulmonary")]
    filtered_df.plot(x="time", y="y", ax=bx)
    filtered_df = df[(df['name'] == "pressure:left_atrium:bicuspid")]
    filtered_df.plot(x="time", y="y", ax=bx)
    filtered_df = df[(df['name'] == "pressure:right_atrium:tricuspid")]
    filtered_df.plot(x="time", y="y", ax=bx)
    plt.show()

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

def compared_PV_loops(file):
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


def compared_PvT(file):
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

def compared_VvT(file):
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

def compared_T(file):
    result = pysvzerod.simulate(file)

    sim_chambers = ["pressure:pulmonary:pul_artery_C", "pressure:J0b:pul_vein","flow:pul_artery_L:J0b", "flow:pul_vein:J3"]
    pgt_chambers = ['p_AR_PUL', 'p_VEN_PUL',]
    qgt_chambers = ['Q_AR_PUL', 'Q_VEN_PUL',]
    mask = result['name'].isin(sim_chambers)
    filtered_df = result[mask]
    filtered_df = filtered_df.pivot(index='time', columns='name', values='y').reset_index()
    filtered_df = filtered_df.iloc[-689:]
    print(filtered_df)

    pgt = pd.read_csv("pressures.csv")
    pgt = pgt.iloc[-689:]
    qgt = pd.read_csv("flows.csv")
    qgt = qgt.iloc[-689:]

    for i in range(4):
        ax = filtered_df.plot(x='time',y=sim_chambers[i])
        if i < 2:
            LV = pgt[[pgt_chambers[i],"time"]]
            LV.plot(x="time",y=pgt_chambers[i], ax=ax)
            plt.title(pgt_chambers[i])
            plt.savefig(pgt_chambers[i])
        else:
            LV = qgt[[qgt_chambers[i-2],"time"]]
            LV.plot(x="time",y=qgt_chambers[i-2], ax=ax)
            plt.title(qgt_chambers[i-2])
            plt.savefig(qgt_chambers[i-2])
            
    plt.show()

def get_data(file):
    result = pysvzerod.simulate(file)


    sim_chambers = ['pressure:pulmonary:pul_artery','flow:pul_vein:J3']
    mask = result['name'].isin(sim_chambers)
    filtered_df = result[mask]
    filtered_df = filtered_df.pivot(index='time', columns='name', values='y').reset_index()
    filtered_df = filtered_df.iloc[-689:]
    print(filtered_df['pressure:pulmonary:pul_artery'].to_list())
    print(filtered_df['flow:pul_vein:J3'].to_list())
    


def main():
    file = "models/RegChamberCRL_SplitPul.json"
    if len(sys.argv) > 1:
        function = sys.argv[1]
        if function == "compared_PV_loops":
            compared_PV_loops(file)
        elif function == "PvT":
            PvT(file)
        elif function == "VvT":
            VvT(file)
        elif function == "compared_PvT":
            compared_PvT(file)
        elif function == "compared_VvT":
            compared_VvT(file)
        elif function == "seperate_PV_loops":
            sperate_PV_Loops(file)
        elif function == "combined_PV_loops":
            combined_PV_Loops(file)
        elif function == "compared_T":
            compared_T(file)
        elif function == "get_data":
            get_data(file)
        else:
            print("please enter a a valid function:")
            print("compared_PV_loops, PvT, VvT, compared_PvT, compared_VvT, seperate_PV_loops, combined_PV_loops, compared_T")
    else:
        print("Please input function")

if __name__ == "__main__":
    main()

