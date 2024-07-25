import json
import os
import subprocess
from tempfile import TemporaryDirectory
import matplotlib.pyplot as plt
import sys

import numpy as np
import pandas as pd

import pysvzerod

# Output all PV loops seperately
def sperate_PV_Loops(result):
    valves = {"left_atrium":":mitral", "left_ventricle":":aortic", "right_atrium":":tricuspid", "right_ventricle":":pulmonary"}
    mask = result['name'].isin(["Vc:" + x for x in valves]+["pressure:" + x + valves[x] for x in valves])
    result = ((result[mask]).pivot(index='time', columns='name', values='y').reset_index()).iloc[-689:]
    for chamber in valves:
        result.plot(x="Vc:"+chamber, y="pressure:"+chamber+valves[chamber], label=chamber).get_legend().remove()
        plt.title(f"{chamber} PV Curve")
        plt.xlabel(f"{chamber}Volume (mL)")
        plt.ylabel(f"{chamber} Pressure (mmHg)")
        # plt.savefig(chamber)
    plt.show()

# Plots ventricle and atrial PV loops
def combined_PV_Loops(result):

    LAmask = result['name'].isin(['Vc:left_atrium', 'pressure:left_atrium:mitral'])
    filtered_result = result[LAmask]
    filtered_result = filtered_result.pivot(index='time', columns='name', values='y')
    a = filtered_result.plot(x='Vc:left_atrium',y='pressure:left_atrium:mitral', label="left atrium")

    RAmask = result['name'].isin(['Vc:right_atrium', 'pressure:right_atrium:tricuspid'])
    filtered_result = result[RAmask]
    filtered_result = filtered_result.pivot(index='time', columns='name', values='y')
    filtered_result.plot(x='Vc:right_atrium',y='pressure:right_atrium:tricuspid',ax=a, label="right atrium")
    a.get_legend().remove()

    plt.title("Atria PV Curves")
    plt.xlabel("Atrial Volume (mL)")
    plt.ylabel("Artial Pressure (mmHg)")

    LVmask = result['name'].isin(['Vc:left_ventricle', 'pressure:left_ventricle:aortic'])
    filtered_result = result[LVmask]
    filtered_result = filtered_result.pivot(index='time', columns='name', values='y')
    a = filtered_result.plot(x='Vc:left_ventricle',y='pressure:left_ventricle:aortic',  label="left ventricle")

    RVmask = result['name'].isin(['Vc:right_ventricle', 'pressure:right_ventricle:pulmonary'])
    filtered_result = result[RVmask]
    filtered_result = filtered_result.pivot(index='time', columns='name', values='y')
    filtered_result.plot(x='Vc:right_ventricle',y='pressure:right_ventricle:pulmonary',ax=a, label="right ventricle")
    a.get_legend().remove()
    plt.title("Right Ventricle PV Curve")
    plt.xlabel("Right Ventricle Volume (mL)")
    plt.ylabel("Right Ventricle Pressure (mmHg)")
    plt.show()

# Plots the chamber volumes against time
def VvT(result):
    chambers = ["left_atrium", "left_ventricle", "right_atrium", "right_ventricle"]
    mask = result['name'].isin(["Vc:" + x for x in chambers])
    result = ((result[mask]).pivot(index='time', columns='name', values='y').reset_index()).iloc[-689:]
    fig, bx = plt.subplots()
    for chamber in chambers:
        result.plot(x="time", y="Vc:" + chamber, label=chamber, ax=bx)
    plt.show()

# Plots the chamber pressures against time
def PvT(result):
    chambers = ["left_atrium:mitral", "left_ventricle:aortic", "right_atrium:tricuspid", "right_ventricle:pulmonary"]
    mask = result['name'].isin(["pressure:" + x for x in chambers])
    result = ((result[mask]).pivot(index='time', columns='name', values='y').reset_index()).iloc[-689:]
    fig, bx = plt.subplots()
    for chamber in chambers:
        result.plot(x="time", y="pressure:" + chamber, label=chamber, ax=bx)
    plt.show()

# Creates a CSV of requested data against time
def get_data(result, blocks):
    mask = result['name'].isin(blocks)
    filtered_result = result[mask]
    filtered_result = filtered_result.pivot(index='time', columns='name', values='y').reset_index()
    filtered_result = filtered_result.iloc[-689:]
    print(filtered_result['pressure:pulmonary:pul_artery'].to_list())
    print(filtered_result['flow:pul_vein:J3'].to_list())
    


def main():
    file = "models/RegChamberCRL_SplitPulmonary.json"
    result = pysvzerod.simulate(file)
    if len(sys.argv) > 1:
        function = sys.argv[1]
        if function == "PvT":
            PvT(result)
        elif function == "VvT":
            VvT(result)
        elif function == "seperate_PV_loops":
            sperate_PV_Loops(result)
        elif function == "combined_PV_loops":
            combined_PV_Loops(result)
        elif function == "get_data":
            blocks = ['pressure:pulmonary:pul_artery']
            get_data(result, blocks)
        else:
            print("please enter a a valid function:")
            print("compared_PV_loops, PvT, VvT, compared_PvT, compared_VvT, seperate_PV_loops, combined_PV_loops, compared_T")
    else:
        print("Please input function")

if __name__ == "__main__":
    main()

