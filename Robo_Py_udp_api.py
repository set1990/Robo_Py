import socket
from time import sleep

RoboAddressPort: tuple[str, int]
bufferSize = 1024
Print_answer_data_FLAG = False
Print_answer_timeout_FLAG = False

def wait_for_answer():
    while True:
        try:
            data, addr = UDPClientSocket.recvfrom(bufferSize)
            if addr[0] == RoboAddressPort[0]:
                if (Print_answer_data_FLAG): print(data)
                break
        except socket.timeout:
            data = 0
            if(Print_answer_timeout_FLAG): print("network timeout")
            break
    return data


def init(RoboAddressIP: str, RoboPort: int ,MyAddressIP = "", MyPort = 20001):
    global RoboAddressPort
    global UDPClientSocket
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPClientSocket.settimeout(2.0)
    RoboAddressPort = (RoboAddressIP,RoboPort)
    UDPClientSocket.bind((MyAddressIP,MyPort))
    return

def close():
    UDPClientSocket.close()
    return

def ping():
    msg = 0x0B.to_bytes(length=1, byteorder='little')
    UDPClientSocket.sendto(msg, RoboAddressPort)
    return wait_for_answer()

def ADC_read():
    msg = 0x01.to_bytes(length=4, byteorder='little')
    UDPClientSocket.sendto(msg, RoboAddressPort)
    return wait_for_answer()


def add_step(servo, value):
    servo = servo.to_bytes(length=1, byteorder='big')
    value = value.to_bytes(length=2, byteorder='big')
    msg = 0x06.to_bytes(length=1, byteorder='little') + servo + value
    UDPClientSocket.sendto(msg, RoboAddressPort)
    return wait_for_answer()


def clear_list():
    msg = 0x07.to_bytes(length=4, byteorder='little')
    UDPClientSocket.sendto(msg, RoboAddressPort)
    return wait_for_answer()


def LIS3MDL_Triger():
    msg = 0x09.to_bytes(length=4, byteorder='little')
    UDPClientSocket.sendto(msg, RoboAddressPort)
    return wait_for_answer()


def LIS3MDL_Read():
    msg = 0x0A.to_bytes(length=4, byteorder='little')
    UDPClientSocket.sendto(msg, RoboAddressPort)
    return wait_for_answer()

def PD_disable_servo(servo):
    servo = servo.to_bytes(length=3, byteorder='little')
    msg = 0x04.to_bytes(length=1, byteorder='little') + servo
    UDPClientSocket.sendto(msg, RoboAddressPort)
    return wait_for_answer()


def PD_enable_servo(servo):
    servo = servo.to_bytes(length=3, byteorder='little')
    msg = 0x03.to_bytes(length=1, byteorder='little') + servo
    UDPClientSocket.sendto(msg, RoboAddressPort)
    return wait_for_answer()


def PD_set_value(servo, value):
    servo = servo.to_bytes(length=1, byteorder='big')
    value = value.to_bytes(length=2, byteorder='big')
    msg = 0x02.to_bytes(length=1, byteorder='little') + servo + value
    UDPClientSocket.sendto(msg, RoboAddressPort)
    return wait_for_answer()

def gripper(state):
    if state:
        data = PD_enable_servo(5)
        if(data!=0):
            sleep(0.1)
            data = PD_set_value(5, 1000)
    else:
        data = PD_set_value(5, 800)
        if(data!=0):
            sleep(0.1)
            data = PD_disable_servo(5)
    return data

def read_list():
    msg = 0x08.to_bytes(length=4, byteorder='little')
    UDPClientSocket.sendto(msg, RoboAddressPort)
    return wait_for_answer()


def run_progrma():
    msg = 0x05.to_bytes(length=4, byteorder='little')
    UDPClientSocket.sendto(msg, RoboAddressPort)
    return wait_for_answer()