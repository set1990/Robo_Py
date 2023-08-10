import socket

RoboAddressPort: tuple[str, int]
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClientSocket.settimeout(2.0)
bufferSize = 1024

def init(RoboAddressIP: str, RoboPort: int ,MyAddressIP = "", MyPort = 20001):
    global RoboAddressPort
    RoboAddressPort = (RoboAddressIP,RoboPort)
    UDPClientSocket.bind((MyAddressIP,MyPort))
    return

def ADC_read():
    msg = 0x01.to_bytes(length=4, byteorder='little')
    UDPClientSocket.sendto(msg, RoboAddressPort)
    while True:
        try:
            data, addr = UDPClientSocket.recvfrom(bufferSize)
            if addr[0] == RoboAddressPort[0]:
                break
        except socket.timeout:
            data = 0
            print("ADC_read: network timeout")
            break
    return data


def add_step(servo, value):
    servo = servo.to_bytes(length=1, byteorder='big')
    value = value.to_bytes(length=2, byteorder='big')
    msg = 0x06.to_bytes(length=1, byteorder='little') + servo + value
    UDPClientSocket.sendto(msg, RoboAddressPort)
    return


def clear_list():
    msg = 0x07.to_bytes(length=4, byteorder='little')
    UDPClientSocket.sendto(msg, RoboAddressPort)
    return


def LIS3MDL_Triger():
    msg = 0x09.to_bytes(length=4, byteorder='little')
    UDPClientSocket.sendto(msg, RoboAddressPort)
    return


def LIS3MDL_Read():
    msg = 0x0A.to_bytes(length=4, byteorder='little')
    UDPClientSocket.sendto(msg, RoboAddressPort)
    while True:
        try:
            data, addr = UDPClientSocket.recvfrom(bufferSize)
            if addr[0] == RoboAddressPort[0]:
                break
        except socket.timeout:
            data = 0
            print("LIS3MDL_Read: network timeout")
            break
    return data

def PD_disable_servo(servo):
    servo = servo.to_bytes(length=3, byteorder='little')
    msg = 0x04.to_bytes(length=1, byteorder='little') + servo
    UDPClientSocket.sendto(msg, RoboAddressPort)
    return


def PD_enable_servo(servo):
    servo = servo.to_bytes(length=3, byteorder='little')
    msg = 0x03.to_bytes(length=1, byteorder='little') + servo
    UDPClientSocket.sendto(msg, RoboAddressPort)
    return


def PD_set_value(servo, value):
    servo = servo.to_bytes(length=1, byteorder='big')
    value = value.to_bytes(length=2, byteorder='big')
    msg = 0x02.to_bytes(length=1, byteorder='little') + servo + value
    UDPClientSocket.sendto(msg, RoboAddressPort)
    return


def read_list():
    msg = 0x08.to_bytes(length=4, byteorder='little')
    UDPClientSocket.sendto(msg, RoboAddressPort)
    while True:
        try:
            data, addr = UDPClientSocket.recvfrom(bufferSize)
            if addr[0] == RoboAddressPort[0]:
                break
        except socket.timeout:
            data = 0
            print("read_list: network timeout")
            break
    return data


def run_progrma():
    msg = 0x05.to_bytes(length=4, byteorder='little')
    UDPClientSocket.sendto(msg, RoboAddressPort)
    return

