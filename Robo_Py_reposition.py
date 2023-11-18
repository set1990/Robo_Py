import Robo_Py_simple_GUI as Robo
import PySimpleGUI as psg
import json
import os
from time import sleep
import Robo_Py_orientation

calibration_list = {"SL1":[0,0,1.0,0.0], "SL2":[0,1,1.0,0.0], "SL3":[0,2,1.0,0.0], "SL4":[0,3,1.0,0.0], "SL5":[0,4,1.0,0.0],
                    "alfa1":[0,0,1.0,0.0], "alfa2":[0,1,1.0,0.0], "alfa3":[0,2,1.0,0.0], "alfa4":[0,3,1.0,0.0], "alfa5":[0,4,1.0,0.0]}


def save_calib_ini():
    with open("calib.ini", mode="wt") as f:
        json.dump(calibration_list,f)


def read_calib_ini():
    global calibration_list
    with open("calib.ini", mode="rt") as f:
        calibration_list = dict(json.load(f))


def calibration_process(num):
    calibration_list[num][2] = 0.0
    calibration_list[num][3] = 0.0
    if not read_pos():
        return False
    engin_on(calibration_list[num][1])
    for postion in range(0, 110, 10):
       set_pos(calibration_list[num][1], postion)
       execute_pos(calibration_list[num][1])
       sleep(3)
       if postion != 0:
           calibration_list[num][2] += (read_pos(False)[calibration_list[num][1]] - calibration_list[num][3])/postion
       else:
           calibration_list[num][3] = read_pos(False)[calibration_list[num][1]]
    engin_off(calibration_list[num][1])
    calibration_list[num][2] = calibration_list[num][2]/10
    calibration_list[num][0] = 1
    save_calib_ini()
    return True


def calibration_repos_adc():
    calib_layout = [
        [psg.Text('Wybierz złącze : ', font='Any 15'), psg.Combo(["SL1", "SL2", "SL3", "SL4", "SL5"], default_value='SL1', font='Any 15', key='Sl_calib',readonly=True, enable_events=True)],
        [psg.Button('Kalibruj ADC', size=(12, 1), font='Any 15', key='calib_start'), Robo.LEDIndicator('calib_ok')],
        [psg.Button('Kalibruj Kąty', size=(12, 1), font='Any 15', key='pic_start'), Robo.LEDIndicator('calib_pitch')]
    ]
    calib_win = psg.Window('CALIBRATION', calib_layout, element_justification='center')
    calib_win.finalize()
    Robo.SetLED(calib_win, 'calib_ok', "green") if calibration_list[calib_win["Sl_calib"].get()][0] else Robo.SetLED(calib_win, 'calib_ok', "red")
    Robo.SetLED(calib_win, 'calib_pitch', "green") if calibration_list["alfa{}".format(calibration_list[calib_win["Sl_calib"].get()][0]+1)][0] else Robo.SetLED(calib_win, 'calib_pitch', "red")
    with open("vectors", mode="wt") as f:
        while True:
            event, values = calib_win.read()
            if event == "Exit" or event == psg.WIN_CLOSED:
                break
            match event:
                case "calib_start":
                    if calibration_process(values["Sl_calib"]):
                        Robo.SetLED(calib_win, 'calib_ok', "green")
                case "Sl_calib":
                    Robo.SetLED(calib_win, 'calib_ok', "green") if calibration_list[values["Sl_calib"]][0] else Robo.SetLED(calib_win, 'calib_ok', "red")
                    Robo.SetLED(calib_win, 'calib_pitch', "green") if calibration_list["alfa{}".format(calibration_list[calib_win["Sl_calib"].get()][0]+1)][0] else Robo.SetLED(calib_win, 'calib_pitch', "red")
                case "pic_start":
                    Robo_Py_orientation.orientation_calc()
                    pass
    calib_win.close()
    return
    pass


def set_pos(num, val):
    Robo.window['SL{}_in'.format(num + 1)].update(val)
    Robo.window['SL{}'.format(num + 1)].update(val)
    Robo.SL_grup[num].value = val
    return


def execute_pos(num):
    Robo.SL_grup[num].new = True
    Robo.Send_robo_step()
    return


def engin_on(num):
    if not Robo.SL_grup[num].enable:
        Robo.SL_grup[num].SL_in()
    return


def engin_off(num):
    if Robo.SL_grup[num].enable:
        Robo.SL_grup[num].SL_in()
    return


def scale(value, num):
    return (value-(calibration_list["SL{}".format(num+1)][3]))/(calibration_list["SL{}".format(num+1)][2]) if calibration_list["SL{}".format(num+1)][0] else 0


def read_pos(scaled=True):
    poss = []
    Robo.ADC_read()
    if Robo.net_status:
        for key in range(1, 6):
            if scaled:
                poss.append(scale(float(Robo.window["ADC{}_T".format(key)].get().replace(',', '.')),(key-1)))
            else:
                poss.append(float(Robo.window["ADC{}_T".format(key)].get().replace(',', '.')))
    return poss


def set_memory(poss_0to100):
    for pos, num in zip(range(5), poss_0to100):
        set_pos(pos, num)
    return

read_calib_ini() if os.path.exists("calib.ini") else save_calib_ini()
