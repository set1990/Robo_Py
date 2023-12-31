import PySimpleGUI as psg
import Robo_Py_udp_api as robo
import Robo_Py_pad as pad
from numpy import int16
from time import sleep

net_status = False

def LEDIndicator(key=None, radius=30):
    return psg.Graph(canvas_size=(radius, radius),
                     graph_bottom_left=(-radius, -radius),
                     graph_top_right=(radius, radius),
                     pad=(0, 0), key=key)

def SetLED(window, key, color):
    graph = window[key]
    graph.erase()
    graph.draw_circle((0, 0), 12, fill_color=color, line_color=color)

def Check_net():
    global net_status
    if (robo.ping() == 0):
        SetLED(window, 'Network_connect', 'red')
        net_status = False
    else:
        SetLED(window, 'Network_connect', 'green')
        net_status = True
    return

def New_address():
    layoutadres = [[psg.T('Your typed chars appear here:'), psg.T('', key='-OUTPUT-')],
                   [MyInput(0), psg.T('.'), MyInput(1), psg.T('.'),
                    MyInput(2), psg.T('.'), MyInput(3)],
                   [psg.B('Ok', key='-OK-', bind_return_key=True), psg.B('Exit'), psg.B('Default')]]
    Adres_win = psg.Window("Adres", layoutadres, return_keyboard_events=True)
    Adres_win.finalize()
    while True:
        eventadres, values = Adres_win.read()
        if eventadres == "Exit" or eventadres == psg.WIN_CLOSED:
            break
        elem = Adres_win.find_element_with_focus()
        if eventadres == 'Default':
            elem.update(192)
            elem = Adres_win[elem.key + 1]
            elem.set_focus()
            elem.update(168)
            elem = Adres_win[elem.key + 1]
            elem.set_focus()
            elem.update(1)
            elem = Adres_win[elem.key + 1]
            elem.set_focus()
            elem.update(150)
            Adres_win['-OK-'].set_focus()
            continue
        if elem is not None:
            key = elem.Key
            # get value of input field that has focus
            if key != '-OK-':
                value = values[key]
                if eventadres == '.' and key != '-OK-':  # if a ., then advance to next field
                    elem.update(value[:-1])
                    value = value[:-1]
                    next_elem = Adres_win[key + 1]
                    next_elem.set_focus()
                elif eventadres not in '0123456789':
                    elem.update(value[:-1])
                elif len(value) > 2 and key < 3:  # if 2 digits typed in, move on to next input
                    next_elem = Adres_win[key + 1]
                    next_elem.set_focus()
                elif len(value) > 2 and key == 3:
                    Adres_win['-OK-'].set_focus()
            else:
                new_addres = '{}.{}.{}.{}'.format(*values.values())
                robo.close()
                robo.init(RoboAddressIP=new_addres, RoboPort=5001)
                Check_net()
                break
    Adres_win.close()
    return

toggle_btn_off = b'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'
toggle_btn_on = b'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'

def MyInput(key): return psg.I('', size=(3, 1), key=key, pad=(0, 2))

layout = [
    [psg.Menu([['Ustawienia', ['Adres']]])],
    [psg.Button('', image_data=toggle_btn_off, key='SL1_ON',
                button_color=(psg.theme_background_color(), psg.theme_background_color()), border_width=0),
     psg.Slider(range=(0, 100), size=(52, 20), default_value=50, disable_number_display=True, resolution=0.1,
                orientation='horizontal', key='SL1', enable_events=True),
     psg.Input('50', size=(4, 1), font='Any 15', justification='r', key='SL1_in', enable_events=True),
     psg.Column([[psg.Button('▲', size=(1, 1), font='Any 7', border_width=2,
                             button_color=(psg.theme_text_color(), psg.theme_background_color()), key='UPSL1')],
                 [psg.Button('▼', size=(1, 1), font='Any 7', border_width=2,
                             button_color=(psg.theme_text_color(), psg.theme_background_color()), key='DOWNSL1')]]),
     LEDIndicator('SL1_led')],

    [psg.Button('', image_data=toggle_btn_off, key='SL2_ON',
                button_color=(psg.theme_background_color(), psg.theme_background_color()), border_width=0),
     psg.Slider(range=(0, 100), size=(52, 20), default_value=50, disable_number_display=True, resolution=0.1,
                orientation='horizontal', key='SL2', enable_events=True),
     psg.Input('50', size=(4, 1), font='Any 15', justification='r', key='SL2_in', enable_events=True),
     psg.Column([[psg.Button('▲', size=(1, 1), font='Any 7', border_width=2,
                             button_color=(psg.theme_text_color(), psg.theme_background_color()), key='UPSL2')],
                 [psg.Button('▼', size=(1, 1), font='Any 7', border_width=2,
                             button_color=(psg.theme_text_color(), psg.theme_background_color()), key='DOWNSL2')]]),
     LEDIndicator('SL2_led')],

    [psg.Button('', image_data=toggle_btn_off, key='SL3_ON',
                button_color=(psg.theme_background_color(), psg.theme_background_color()), border_width=0),
     psg.Slider(range=(0, 100), size=(52, 20), default_value=50, disable_number_display=True, resolution=0.1,
                orientation='horizontal', key='SL3', enable_events=True),
     psg.Input('50', size=(4, 1), font='Any 15', justification='r', key='SL3_in', enable_events=True),
     psg.Column([[psg.Button('▲', size=(1, 1), font='Any 7', border_width=2,
                             button_color=(psg.theme_text_color(), psg.theme_background_color()), key='UPSL3')],
                 [psg.Button('▼', size=(1, 1), font='Any 7', border_width=2,
                             button_color=(psg.theme_text_color(), psg.theme_background_color()), key='DOWNSL3')]]),
     LEDIndicator('SL3_led')],

    [psg.Button('', image_data=toggle_btn_off, key='SL4_ON',
                button_color=(psg.theme_background_color(), psg.theme_background_color()), border_width=0),
     psg.Slider(range=(0, 100), size=(52, 20), default_value=50, disable_number_display=True, resolution=0.1,
                orientation='horizontal', key='SL4', enable_events=True),
     psg.Input('50', size=(4, 1), font='Any 15', justification='r', key='SL4_in', enable_events=True),
     psg.Column([[psg.Button('▲', size=(1, 1), font='Any 7', border_width=2,
                             button_color=(psg.theme_text_color(), psg.theme_background_color()), key='UPSL4')],
                 [psg.Button('▼', size=(1, 1), font='Any 7', border_width=2,
                             button_color=(psg.theme_text_color(), psg.theme_background_color()), key='DOWNSL4')]]),
     LEDIndicator('SL4_led')],

    [psg.Button('', image_data=toggle_btn_off, key='SL5_ON',
                button_color=(psg.theme_background_color(), psg.theme_background_color()), border_width=0),
     psg.Slider(range=(0, 100), size=(52, 20), default_value=50, disable_number_display=True, resolution=0.1,
                orientation='horizontal', key='SL5', enable_events=True),
     psg.Input('50', size=(4, 1), font='Any 15', justification='r', key='SL5_in', enable_events=True),
     psg.Column([[psg.Button('▲', size=(1, 1), font='Any 7', border_width=2,
                             button_color=(psg.theme_text_color(), psg.theme_background_color()), key='UPSL5')],
                 [psg.Button('▼', size=(1, 1), font='Any 7', border_width=2,
                             button_color=(psg.theme_text_color(), psg.theme_background_color()), key='DOWNSL5')]]),
     LEDIndicator('SL5_led')],

    [psg.Text('  Chwytak: ', font='Any 15'),
     psg.Button('', image_data=toggle_btn_off, key='SL6_ON',
                button_color=(psg.theme_background_color(), psg.theme_background_color()), border_width=0)],

    [psg.Button('Wyślij położenie', size=(10, 2), font='Any 15', key='SENDSTEP'),
     psg.Button('Dodaj krok', size=(12, 2), font='Any 15', key='ADDSTEP'),
     psg.Button('Uruchom program', size=(12, 2), font='Any 15', key='RUN'),
     psg.Button('Wyczyść listę', size=(12, 2), font='Any 15', key='CLIST')],

    [psg.Button('Odczyt \n ADC', size=(10, 2), font='Any 15', key='RADC'),
     psg.Button('Odczyt \n LIS3MDL', size=(12, 2), font='Any 15', key='RLIS3MDL'),
     psg.Button('Odczyt \n LSM6DS33', size=(12, 2), font='Any 15', key='RLILSM6'),
     psg.Button('Odczyt listy', size=(12, 2), font='Any 15', key='RLIST')],

    [psg.Column([[psg.Text('                               X:', font='Any 15'), psg.Text('          Y:', font='Any 15'), psg.Text('         Z:', font='Any 15'),],
                 [psg.Text('     LIS3MDL :  ', font='Any 15'),
                  psg.Text('50,0', font='Any 15', background_color='black', size=(7, 1), justification='right', key='LIS3MDLx_T'),
                  psg.Text('50,0', font='Any 15', background_color='black', size=(7, 1), justification='right', key='LIS3MDLy_T'),
                  psg.Text('50,0', font='Any 15', background_color='black', size=(7, 1), justification='right', key='LIS3MDLz_T')],

                 [psg.Text('  LSM6DS33 : ', font='Any 15'),
                  psg.Column([[psg.Text('50,0', font='Any 15', background_color='black', size=(7, 1), justification='right', key='LSM6DS33_G_x_T'),
                               psg.Text('50,0', font='Any 15', background_color='black', size=(7, 1), justification='right', key='LSM6DS33_G_y_T'),
                               psg.Text('50,0', font='Any 15', background_color='black', size=(7, 1), justification='right', key='LSM6DS33_G_z_T')],
                              [psg.Text('50,0', font='Any 15', background_color='black', size=(7, 1), justification='right', key='LSM6DS33_A_x_T'),
                               psg.Text('50,0', font='Any 15', background_color='black', size=(7, 1), justification='right', key='LSM6DS33_A_y_T'),
                               psg.Text('50,0', font='Any 15', background_color='black', size=(7, 1), justification='right', key='LSM6DS33_A_z_T')]])]]),
     psg.Text(' ', font='Any 15'),
     psg.Column([[psg.Text('     NET: ', font='Any 12'), LEDIndicator('Network_connect')],
                 [psg.Checkbox('PAD', font='Any 12', enable_events=True, key='PAD'), LEDIndicator('PAD_connect')]])],

    [psg.Text('  ADC : ', font='Any 15')],
    [psg.Text('1:', font='Any 15'),
     psg.Text('50,0', font='Any 15', background_color='black', size=(7, 1), justification='right', key='ADC1_T'),
     psg.Text('2:', font='Any 15'),
     psg.Text('50,0', font='Any 15', background_color='black', size=(7, 1), justification='right', key='ADC2_T'),
     psg.Text('3:', font='Any 15'),
     psg.Text('50,0', font='Any 15', background_color='black', size=(7, 1), justification='right', key='ADC3_T'),
     psg.Text('4:', font='Any 15'),
     psg.Text('50,0', font='Any 15', background_color='black', size=(7, 1), justification='right', key='ADC4_T'),
     psg.Text('5:', font='Any 15'),
     psg.Text('50,0', font='Any 15', background_color='black', size=(7, 1), justification='right', key='ADC5_T')],

    [psg.Multiline(echo_stdout_stderr=True, reroute_stdout=True, autoscroll=True, background_color='black',
                   text_color='white',
                   key='-MLINE-', expand_y=True, expand_x=True, disabled=True, write_only=True)]
]

robo.init(RoboAddressIP='192.168.1.150', RoboPort=5001)
robo.Print_answer_timeout_FLAG = True
window = psg.Window('ROBO', layout, size=(705, 820))
window.finalize()
Check_net()
SetLED(window, 'PAD_connect', 'red')
SL6_enable = False
l_SL_alloc = 0
r_SL_alloc = 0
SL_alloc_LED = {1: 'SL1_led', 2: 'SL2_led', 3: 'SL3_led', 4: 'SL4_led', 5: 'SL5_led'}

class SL_N:
    def __init__(self, event_input: str, event_slider: str, event_down: str, event_up: str, event_on: str, number: int):
        self.enable = False
        self.value = 50.0
        self.new = False
        self.event_input = event_input
        self.event_slider = event_slider
        self.event_down = event_down
        self.event_up = event_up
        self.event_on = event_on
        self.number = number

    def SL_in(self):
        self.enable = not self.enable
        if self.enable:
            data = robo.PD_enable_servo(self.number)
        else:
            data = robo.PD_disable_servo(self.number)
        if (data == 0):
            self.enable = not self.enable
            SetLED(window, 'Network_connect', 'red')
        else:
            window[self.event_on].update(image_data=toggle_btn_on if self.enable else toggle_btn_off)
            SetLED(window, 'Network_connect', 'green')
        return self.enable

    def events_hendler(self, event, values):
        match event:
            case self.event_on:
                self.enable = self.SL_in()
            case self.event_input:
                self.value = float(values[self.event_input])
                self.new = True
                window[self.event_slider].update(self.value)
            case self.event_slider:
                self.value = values[self.event_slider]
                self.new = True
                window[self.event_input].update(format(self.value, '.1f'))
            case self.event_up:
                if (self.value <= 100):
                    self.value = self.value + 0.1
                    self.new = True
                    window[self.event_slider].update(self.value)
                    window[self.event_input].update(format(self.value, '.1f'))
            case self.event_down:
                if (self.value > 0.0):
                    self.value = self.value - 0.1
                    self.new = True
                    window[self.event_slider].update(self.value)
                    window[self.event_input].update(format(self.value, '.1f'))
            case "PAD":
                self.value -= values
                self.new = True
                if (self.value > 100):
                    self.value = 100
                elif (self.value < 0):
                    self.value = 0
                window[self.event_slider].update(self.value)
                window[self.event_input].update(format(self.value, '.1f'))

SL_grup: list[SL_N] = [SL_N('SL1_in', 'SL1', 'DOWNSL1', 'UPSL1', 'SL1_ON', 0),
                       SL_N('SL2_in', 'SL2', 'DOWNSL2', 'UPSL2', 'SL2_ON', 1),
                       SL_N('SL3_in', 'SL3', 'DOWNSL3', 'UPSL3', 'SL3_ON', 2),
                       SL_N('SL4_in', 'SL4', 'DOWNSL4', 'UPSL4', 'SL4_ON', 3),
                       SL_N('SL5_in', 'SL5', 'DOWNSL5', 'UPSL5', 'SL5_ON', 4)]

def ADC_read():
    window['RADC'].set_cursor("watch")
    dataADC = robo.ADC_read()
    if (dataADC != 0):
        window['ADC1_T'].update(format((dataADC[0] + (dataADC[1] * 256)), '.1f'))
        window['ADC2_T'].update(format((dataADC[2] + (dataADC[3] * 256)), '.1f'))
        window['ADC3_T'].update(format((dataADC[4] + (dataADC[5] * 256)), '.1f'))
        window['ADC4_T'].update(format((dataADC[6] + (dataADC[7] * 256)), '.1f'))
        window['ADC5_T'].update(format((dataADC[8] + (dataADC[9] * 256)), '.1f'))
    if (dataADC == 0):
        SetLED(window, 'Network_connect', 'red')
    else:
        SetLED(window, 'Network_connect', 'green')
    window['RADC'].set_cursor("arrow")

def Magnetometr_read():
    window['RLIS3MDL'].set_cursor("watch")
    if not robo.LIS3MDL_Triger(): return
    sleep(1)
    dataLIS3MDL = robo.LIS3MDL_Read()
    if (dataLIS3MDL != 0):
        window['LIS3MDLx_T'].update(format(int16(dataLIS3MDL[1]|(dataLIS3MDL[2]<<8)), '.1f'))
        window['LIS3MDLy_T'].update(format(int16(dataLIS3MDL[3]|(dataLIS3MDL[4]<<8)), '.1f'))
        window['LIS3MDLz_T'].update(format(int16(dataLIS3MDL[5]|(dataLIS3MDL[6]<<8)), '.1f'))
    if (dataLIS3MDL == 0):
        SetLED(window, 'Network_connect', 'red')
    else:
        SetLED(window, 'Network_connect', 'green')
    window['RLIS3MDL'].set_cursor("arrow")

def Gyro_ACC_read():
    window['RLILSM6'].set_cursor("watch")
    if not robo.LSM6DS33_Triger(): return
    sleep(1)
    dataLSM6DS33 = robo.LSM6DS33_Read()
    if (dataLSM6DS33 != 0):
        window['LSM6DS33_G_x_T'].update(format(int16(dataLSM6DS33[1]|(dataLSM6DS33[2]<<8)), '.1f'))
        window['LSM6DS33_G_y_T'].update(format(int16(dataLSM6DS33[3]|(dataLSM6DS33[4]<<8)), '.1f'))
        window['LSM6DS33_G_z_T'].update(format(int16(dataLSM6DS33[5]|(dataLSM6DS33[6]<<8)), '.1f'))
        window['LSM6DS33_A_x_T'].update(format(int16(dataLSM6DS33[7]|(dataLSM6DS33[8]<<8)), '.1f'))
        window['LSM6DS33_A_y_T'].update(format(int16(dataLSM6DS33[9]|(dataLSM6DS33[10]<<8)), '.1f'))
        window['LSM6DS33_A_z_T'].update(format(int16(dataLSM6DS33[11]|(dataLSM6DS33[12]<<8)), '.1f'))
    if (dataLSM6DS33 == 0):
        SetLED(window, 'Network_connect', 'red')
    else:
        SetLED(window, 'Network_connect', 'green')
    window['RLILSM6'].set_cursor("arrow")
    pass

def Read_step_list():
    window[event].set_cursor("watch")
    dataStep = robo.read_list()
    if (dataStep != 0):
        for i in range(0, len(dataStep), 3):
            if (dataStep[i] == 9):
                print("Lista pusta")
            else:
                print("num:{:d} val={:d}".format(dataStep[i], (dataStep[i + 1] + (dataStep[i + 2] * 256))))
    if (dataStep == 0):
        SetLED(window, 'Network_connect', 'red')
    else:
        SetLED(window, 'Network_connect', 'green')
    window[event].set_cursor("arrow")

def Send_robo_step():
    window['SENDSTEP'].set_cursor("watch")
    for SL_i in SL_grup:
        if SL_i.new:
            data = robo.PD_set_value(SL_i.number, int(SL_i.value * 10))
            SL_i.new = False
            if data == 0:
                SetLED(window, 'Network_connect', 'red')
            else:
                SetLED(window, 'Network_connect', 'green')
    window['SENDSTEP'].set_cursor("arrow")


def Add_step_to_list():
    window[event].set_cursor("watch")
    for SL_i in SL_grup:
        if SL_i.new:
            data = robo.add_step(SL_i.number, int(SL_i.value * 10))
            SL_i.new = False
            if (data == 0):
                SetLED(window, 'Network_connect', 'red')
            else:
                SetLED(window, 'Network_connect', 'green')
    window[event].set_cursor("arrow")

def gripper_click():
    global SL6_enable
    SL6_enable = not SL6_enable
    if robo.gripper(SL6_enable):
        SetLED(window, 'Network_connect', 'green')
        window['SL6_ON'].update(image_data=toggle_btn_on if SL6_enable else toggle_btn_off)
    else:
        SL6_enable = not SL6_enable
        SetLED(window, 'Network_connect', 'red')

def SL_alloc_f(SL_alloc, SL_alloc_diff, sig, color):
    if SL_alloc:
        SetLED(window, SL_alloc_LED[SL_alloc], 0)
    if sig == "+":
        SL_alloc = SL_alloc + 1
        if (SL_alloc == SL_alloc_diff): SL_alloc = SL_alloc + 1
        if (SL_alloc > 5): SL_alloc = 1
        if (SL_alloc == SL_alloc_diff): SL_alloc = SL_alloc + 1
    else:
        SL_alloc = SL_alloc - 1
        if (SL_alloc == SL_alloc_diff): SL_alloc = SL_alloc - 1
        if (SL_alloc < 1): SL_alloc = 5
        if (SL_alloc == SL_alloc_diff): SL_alloc = SL_alloc - 1
    if SL_alloc:
        SetLED(window, SL_alloc_LED[SL_alloc], color)
    return SL_alloc

@pad.PAD_hendler
def PAD_hendler(key, value=0):
    global SL6_enable
    global r_SL_alloc
    global l_SL_alloc
    match key:
        case "LM":
            Magnetometr_read()
            Gyro_ACC_read()
        case "ADC":
            ADC_read()
        case "red_led":
            SetLED(window, 'PAD_connect', 'red')
        case "green_led":
            SetLED(window, 'PAD_connect', 'green')
        case "gripper_on_off":
            gripper_click()
        case "r_plus_SL":
            r_SL_alloc = SL_alloc_f(r_SL_alloc, l_SL_alloc, '+', 'gold')
        case "r_minus_SL":
            r_SL_alloc = SL_alloc_f(r_SL_alloc, l_SL_alloc, '-', 'gold')
        case "l_plus_SL":
            l_SL_alloc = SL_alloc_f(l_SL_alloc, r_SL_alloc, '+', 'cyan')
        case "l_minus_SL":
            l_SL_alloc = SL_alloc_f(l_SL_alloc, r_SL_alloc, '-', 'cyan')
        case "enable_disable_l":
            if l_SL_alloc:
                SL_grup[l_SL_alloc - 1].SL_in()
        case "enable_disable_r":
            if r_SL_alloc:
                SL_grup[r_SL_alloc - 1].SL_in()
        case "SL_val_l":
            if l_SL_alloc:
                SL_grup[l_SL_alloc - 1].events_hendler("PAD", value)
                Send_robo_step()
        case "SL_val_r":
            if r_SL_alloc:
                SL_grup[r_SL_alloc - 1].events_hendler("PAD", value)
                Send_robo_step()
        case "exit":
            for Led in SL_alloc_LED.values():
                SetLED(window, Led, 0)
            r_SL_alloc = l_SL_alloc = 0

def GUI_main():
    global event
    event, values = window.read(timeout=10)
    if event == psg.WIN_CLOSED or event == 'Exit':
        if pad.running:
            pad.stop()
        window.close()
        return False
    match event:
        case 'PAD':
            if (values['PAD']):
                pad.start()
            else:
                pad.stop()
        case 'Adres':
            New_address()
        case 'SL6_ON':
            gripper_click()
        case 'ADDSTEP':
            Add_step_to_list()
        case 'RUN':
            window[event].set_cursor("watch")
            if robo.run_progrma():
                SetLED(window, 'Network_connect', 'green')
            else:
                SetLED(window, 'Network_connect', 'red')
            window[event].set_cursor("arrow")
        case 'CLIST':
            if robo.clear_list():
                SetLED(window, 'Network_connect', 'green')
            else:
                SetLED(window, 'Network_connect', 'red')
        case 'RLIST':
            Read_step_list()
        case 'SENDSTEP':
            Send_robo_step()
        case 'RADC':
            ADC_read()
        case 'RLIS3MDL':
            Magnetometr_read()
        case 'RLILSM6':
            Gyro_ACC_read()
        case _:
            for SL_i in SL_grup:
                SL_i.events_hendler(event, values)
    return True
