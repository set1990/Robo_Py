import Robo_Py_simple_GUI as Robo
import numpy as num
from time import sleep

def read_LIS3MDL_LSM6DS33():
    vector_B = []
    vector_Gyro = []
    vector_ACC = []
    Robo.Magnetometr_read()
    sleep(1)
    Robo.Gyro_ACC_read()
    if Robo.net_status:
        for key in ["x", "y", "z"]:
                vector_B.append(float(Robo.window["LIS3MDL{}_T".format(key)].get().replace(',', '.'))*(400/32767))
                vector_Gyro.append(float(Robo.window["LSM6DS33_G_{}_T".format(key)].get().replace(',', '.'))*(2000/32767))
                vector_ACC.append(float(Robo.window["LSM6DS33_A_{}_T".format(key)].get().replace(',', '.'))*(2/32767))
    return vector_B, vector_Gyro, vector_ACC


def orientation_calc():
    B, Gyro, ACC = read_LIS3MDL_LSM6DS33()
    Pitch = num.rad2deg(num.arctan2(ACC[1], ACC[2]))
    sinAmgle = num.sin(num.deg2rad(Pitch))
    cosAmgle = num.cos(num.deg2rad(Pitch))
    Bfy = B[1]*cosAmgle - B[2]*sinAmgle
    Bz = B[1]*sinAmgle + B[2]*cosAmgle
    Gz = ACC[1]*sinAmgle + ACC[2]*cosAmgle
    Yaw = num.rad2deg(num.arctan(-ACC[0]/Gz))
    sinAmgle = num.sin(num.deg2rad(Yaw))
    cosAmgle = num.cos(num.deg2rad(Yaw))
    Bfx = B[0]*cosAmgle + Bz*sinAmgle
    Roll = num.rad2deg(num.arctan2(-Bfy,Bfx))
    print("kąty")
    print(Pitch)
    print(Roll)
    print(Yaw)
    return Pitch, Roll, Yaw

