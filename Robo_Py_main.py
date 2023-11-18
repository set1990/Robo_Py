import Robo_Py_simple_GUI as Robo
import PySimpleGUI as main_g
import Robo_Py_reposition

menu_layout = [
    [main_g.Button('Kalibracja', size=(10, 2), font='Any 15', key='calib_main'), main_g.Button('Odczyt\npozycji', size=(10, 2), font='Any 15', key='read_pos')],
    [main_g.Button('', size=(10, 2), font='Any 15', key='', disabled=True), main_g.Button('', size=(10, 2), font='Any 15', key='', disabled=True)]
]

main_win = main_g.Window('ROBO MAIN', menu_layout, size=(280, 170))
main_win.finalize()


def Main_GUI_handler():
    event_main, values = main_win.read(timeout=10)
    if event_main == main_g.WIN_CLOSED or event_main == 'Exit':
        main_win.close()
        return False
    match event_main:
        case "calib_main":
            Robo_Py_reposition.calibration_repos_adc()
        case "read_pos":
            Robo_Py_reposition.set_memory(Robo_Py_reposition.read_pos())
    return True


while Robo.GUI_main():
    if not Main_GUI_handler(): Robo.window.close()
    pass
