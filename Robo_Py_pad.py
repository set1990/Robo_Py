import threading
from pygame import joystick
from time import sleep


def thread_function():
    global running
    global hendler
    if (joystick.get_count()):
        joystick_nr = joystick.Joystick(0)
        hendler("green_led")
        while (running):
            # Get the name from the OS for the controller/joystick
            # Usually axis run in pairs, up/down for one, and left/right for the other.
            if (joystick_nr.get_button(2)):
                hendler("ADC")
            elif (joystick_nr.get_button(1)):
                hendler("LM")
            elif (joystick_nr.get_button(0)):
                hendler("gripper_on_off")
            elif (joystick_nr.get_button(8)):
                hendler("enable_disable_l")
            elif (joystick_nr.get_button(9)):
                hendler("enable_disable_r")
            elif (joystick_nr.get_button(4)):
                hendler("l_plus_SL")
            elif (joystick_nr.get_button(5)):
                hendler("r_plus_SL")
            elif (joystick_nr.get_axis(4) > 0.800):
                hendler("l_minus_SL")
            elif (joystick_nr.get_axis(5) > 0.800):
                hendler("r_minus_SL")
            elif (joystick_nr.get_axis(1) > 0.1) or (joystick_nr.get_axis(1) < (-0.1)):
                hendler("SL_val_l", joystick_nr.get_axis(1)*2)
            elif (joystick_nr.get_axis(3) > 0.1) or (joystick_nr.get_axis(3) < (-0.1)):
                hendler("SL_val_r", joystick_nr.get_axis(3)*2)
            sleep(0.1)

        joystick_nr.quit()
    else:
        hendler("red_led")
        print("PAD Timeout")
    return


def start(input):
    global hendler
    global running
    joystick.init()
    running = True
    hendler = input
    thread = threading.Thread(target=thread_function)
    thread.start()

    return thread


def stop():
    global running
    running = False
    hendler("exit")
    return
