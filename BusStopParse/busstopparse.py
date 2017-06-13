# -*- coding: utf-8 -*-

import urllib.request
from xml.dom import minidom
import time
import os
import datetime
from socket import *
from select import select

SERVER_IP = '113.198.236.96'
SERVER_PORT = '29903'
BUF_SIZE = 1024
ADDR = (SERVER_IP, SERVER_PORT)


def crolling():
    # 현재 시간 기록
    now_time = datetime.datetime.now()
    now_time = now_time.strftime('%Y%m%d%H%M%S')

    system_log(now_time, '[BusLocationSystem] Start Crolling')
    # url 접근
    apiurl = "http://61.43.246.153/openapi-data/service/busanBIMS/busStop?ServiceKey=4YstE1tC4r8vbbmmDCGqQ3P65YsFYZOPASjitkuyZUNfgwKG3gCy0QZpKfWzjIUKaZPYZOtCgfm7uPyxw5jcbA%3D%3D"
    dom = minidom.parse(urllib.request.urlopen(apiurl))
    system_log(now_time, '[BusLocationSystem] Url Connetion')
    # 파싱시작
    items = dom.getElementsByTagName("item")
    system_log(now_time, '[BusLocationSystem] Start Parse')
    print(now_time)
    print('---------------------')
    data_count =0
    for item in items:
        for node in item.childNodes:
            if node.nodeName == "bstopId":
                system_log(now_time, '[BusLocationSystem] ' + node.childNodes[0].nodeValue + ' bstopId Find')
                location_log(now_time, node.childNodes[0].nodeValue)
                print(node.childNodes[0].nodeValue)
                send_data = node.childNodes[0].nodeValue
                send_data = send_data + '/' + now_time + '/' + 'L'
            if node.nodeName == "bstopNm":
                system_log(now_time, '[BusLocationSystem] ' + node.childNodes[0].nodeValue + ' bstopNm Find')
                location_log(now_time, node.childNodes[0].nodeValue)
                print(node.childNodes[0].nodeValue)
                send_data = send_data + '/' + node.childNodes[0].nodeValue
            if node.nodeName == "gpsX":
                system_log(now_time, '[BusLocationSystem] ' + node.childNodes[0].nodeValue + ' gpsX Find')
                location_log(now_time, node.childNodes[0].nodeValue)
                print(node.childNodes[0].nodeValue)
                send_data = send_data + '/' + node.childNodes[0].nodeValue
            if node.nodeName == "gpsY":
                system_log(now_time, '[BusLocationSystem] ' + node.childNodes[0].nodeValue + ' gpsY Find')
                location_log(now_time, node.childNodes[0].nodeValue)
                print(node.childNodes[0].nodeValue)
                send_data = send_data + '/' + node.childNodes[0].nodeValue
                location_log(now_time, '---------------')
                print('---------------------')
            data_count+=1
    print("data_count : "+str(data_count))
    send_result = server_connection(now_time, send_data)
    if send_result == 1:
        system_log(now_time, '[BusLocationSystem] Location Data Send End')
    elif send_result == 0:
        system_log(now_time, '[BusLocationSystem] Connection Fail, Keep Going')
        return 0
    # time.sleep(90)
    # crolling()


# 로그 파일생성용 함수
def location_log(now_time, log_data):
    # 파라미터인 현재 시간 + 로그파일네임
    file_name = os.path.dirname(os.path.abspath(__file__)) + '\\log\\' + now_time + '_bus_location' + '.txt'
    # 이미존재하면 파일을 a모드로 오픈
    if os.path.exists(file_name):
        f = open(file_name, 'a')
    # 존재하지않으면 파일을 w모드로 오픈
    else:
        f = open(file_name, 'w')
    # 로그데이터기록
    f.write(log_data)
    f.write('\n')
    f.close()


def system_log(now_time, log_data):
    file_name = os.path.dirname(os.path.abspath(__file__)) + '\\log\\' + now_time + '_system_log' + '.txt'
    # 이미존재하면 파일을 a모드로 오픈
    if os.path.exists(file_name):
        f = open(file_name, 'a')
    # 존재하지않으면 파일을 w모드로 오픈
    else:
        f = open(file_name, 'w')
    # 로그데이터기록
    f.write(log_data)
    f.write('\n')
    f.close()


def server_connection(now_time, send_data):
    client_socket = socket(AF_INET, SOCK_STREAM)

    try:
        client_socket.connect(ADDR)
    except Exception as e:
        system_log(now_time, '[BusLocationSystem] Socket Connetion Fail')
        return 0
    system_log(now_time, '[BusLocationSystem] Socket Connetion Success')
    print(send_data)

    client_socket.send(send_data)
    system_log(now_time, '[BusLocationSystem] Send Data Success')

    client_socket.close()
    system_log(now_time, '[BusLocationSystem] Socket Connetion Close')
    return 1


crolling()
