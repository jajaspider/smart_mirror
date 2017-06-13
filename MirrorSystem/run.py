#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib
import socket
import datetime
import math
from xml.dom import minidom
import cv2
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

servicekey = "4YstE1tC4r8vbbmmDCGqQ3P65YsFYZOPASjitkuyZUNfgwKG3gCy0QZpKfWzjIUKaZPYZOtCgfm7uPyxw5jcbA%3D%3D"

def get_ip():
    url = 'http://checkmyip.com'
    readurl = urllib.urlopen(url).read()
    readurl = readurl.decode('utf-8')
    splitresult = readurl.split('\n')
    for result in splitresult:
        if result.find('Your IP is') > 0:
            ip = result.split('primary">')
            ip_1 = ip[1].split('</span>')
    return ip_1[0]

def ip_parser():
    global gps_x
    global gps_y
    ip = get_ip()
    try:
        input_url = "http://ip-api.com/line/" + ip
        readurl = urllib.urlopen(input_url).read()
    except:
        print(input_url + " url 접속 에러")
        exit(0)

    readurl = readurl.decode('utf-8')
    splitresult = readurl.split('\n')
    data_count = 0
    for result in splitresult:
        # print(result)
        data_count += 1
        if (data_count == 8):
            gps_x = result
        if (data_count == 9):
            gps_y = result

    print("[DEBUG] gps_x : " + gps_x)
    print("[DEBUG] gps_y : " + gps_y)


def grid(v1, v2):
    RE = 6371.00877  # 지구 반경(km)
    GRID = 5.0  # 격자 간격(km)
    SLAT1 = 30.0  # 투영 위도1(degree)
    SLAT2 = 60.0  # 투영 위도2(degree)
    OLON = 126.0  # 기준점 경도(degree)
    OLAT = 38.0  # 기준점 위도(degree)
    XO = 43  # 기준점 X좌표(GRID)
    YO = 136  # 기1준점 Y좌표(GRID)

    DEGRAD = math.pi / 180.0
    RADDEG = 180.0 / math.pi

    re = RE / GRID;
    slat1 = SLAT1 * DEGRAD
    slat2 = SLAT2 * DEGRAD
    olon = OLON * DEGRAD
    olat = OLAT * DEGRAD

    sn = math.tan(math.pi * 0.25 + slat2 * 0.5) / math.tan(math.pi * 0.25 + slat1 * 0.5)
    sn = math.log(math.cos(slat1) / math.cos(slat2)) / math.log(sn)
    sf = math.tan(math.pi * 0.25 + slat1 * 0.5)
    sf = math.pow(sf, sn) * math.cos(slat1) / sn
    ro = math.tan(math.pi * 0.25 + olat * 0.5)
    ro = re * sf / math.pow(ro, sn);
    rs = {};

    ra = math.tan(math.pi * 0.25 + (v1) * DEGRAD * 0.5)
    ra = re * sf / math.pow(ra, sn)

    theta = v2 * DEGRAD - olon
    if theta > math.pi:
        theta -= 2.0 * math.pi
    if theta < -math.pi:
        theta += 2.0 * math.pi
    theta *= sn
    rs['x'] = math.floor(ra * math.sin(theta) + XO + 0.5)
    rs['y'] = math.floor(ro - ra * math.cos(theta) + YO + 0.5)

    now = datetime.datetime.now()
    base_date = now.strftime('%Y%m%d')

    if 24 > (int(now.strftime('%H')) - 1):
        base_time = "2300"
        if 23 > (int(now.strftime('%H')) - 1):
            base_time = "2000"
            if 20 > (int(now.strftime('%H')) - 1):
                base_time = "1700"
                if 17 > (int(now.strftime('%H')) - 1):
                    base_time = "1400"
                    if 14 > (int(now.strftime('%H')) - 1):
                        base_time = "1100"
                        if 11 > (int(now.strftime('%H')) - 1):
                            base_time = "0800"
                            if 8 > (int(now.strftime('%H')) - 1):
                                base_time = "0500"
                                if 5 > (int(now.strftime('%H')) - 1):
                                    base_time = "0200"

    nx = str(rs["x"]).split('.')[0]
    ny = str(rs["y"]).split('.')[0]
    string = "http://newsky2.kma.go.kr/service/SecndSrtpdFrcstInfoService2/ForecastSpaceData?ServiceKey=" + servicekey + "&base_date=" + base_date + "&base_time=" + base_time + "&nx=" + nx + "&ny=" + ny
    print("[DEBUG] apiurl : " + string)
    return string

def weather_parse():
    apiurl = grid(float(gps_x), float(gps_y))
    dom = minidom.parse(urllib.urlopen(apiurl))
    # 파싱시작
    items = dom.getElementsByTagName("item")
    print('---------------------')
    sky_flag = 0

    for item in items:
        for node in item.childNodes:
            if node.nodeName == "category":
                if node.childNodes[0].nodeValue == "SKY":
                    sky_flag = 1
            if sky_flag == 1:
                if node.nodeName == "fcstValue":
                    if node.childNodes[0].nodeValue == "1":
                        weather_status = "clear"
                        print("[날씨] 맑음")
                        print('---------------------')
                    if node.childNodes[0].nodeValue == "2":
                        weather_status = "little cloud"
                        print("[날씨] 구름조금")
                        print('---------------------')
                    if node.childNodes[0].nodeValue == "3":
                        weather_status = "many cloud"
                        print("[날씨] 구름많음")
                        print('---------------------')
                    if node.childNodes[0].nodeValue == "4":
                        weather_status = "cloudy"
                        print("[날씨] 흐림")
                        print('---------------------')
    return weather_status

def mise_parse():
    apiurl = "http://opendata.busan.go.kr/openapi/service/AirQualityInfoService/getAirQualityInfoClassifiedByStation?ServiceKey=4YstE1tC4r8vbbmmDCGqQ3P65YsFYZOPASjitkuyZUNfgwKG3gCy0QZpKfWzjIUKaZPYZOtCgfm7uPyxw5jcbA%3D%3D"
    dom = minidom.parse(urllib.urlopen(apiurl))
    # 파싱시작
    items = dom.getElementsByTagName("item")
    for item in items:
        for node in item.childNodes:
            if node.nodeName == "pm10Cai":
                temp_pm10Cai = node.childNodes[0].nodeValue
            if node.nodeName == "site":
                if node.childNodes[0].nodeValue == "전포동":
                    temp_pm10Cai = temp_pm10Cai.strip()
                    if temp_pm10Cai == "1":
                        mise_status = "good"
                        print("[미세먼지] 좋음")
                        print('---------------------')
                    if temp_pm10Cai == "2":
                        mise_status = "so so"
                        print("[미세먼지] 보통")
                        print('---------------------')
                    if temp_pm10Cai == "3":
                        mise_status = "bad"
                        print("[미세먼지] 나쁨")
                        print('---------------------')
                    if temp_pm10Cai == "4":
                        mise_status = "very bad"
                        print("[미세먼지] 매우나쁨")
                        print('---------------------')
    return mise_status

def metro_parse():
    station_code = "PSS222"
    upDownTypeCode = "U"
    global end_station
    if (station_code[3] == "2") & (upDownTypeCode == "U"):
        end_station = "JangSan"

    apiurl = "http://openapi.tago.go.kr/openapi/service/SubwayInfoService/getSubwaySttnAcctoSchdulList?ServiceKey=4YstE1tC4r8vbbmmDCGqQ3P65YsFYZOPASjitkuyZUNfgwKG3gCy0QZpKfWzjIUKaZPYZOtCgfm7uPyxw5jcbA%3D%3D&subwayStationId=PSS222&upDownTypeCode=U&dailyTypeCode=01&numOfRows=999"
    dom = minidom.parse(urllib.urlopen(apiurl))
    # 파싱시작
    items = dom.getElementsByTagName("item")
    now = datetime.datetime.now()
    now_time = now.strftime('%H%M%S')
    now_arrive_flag = 0
    first_1 = 1

    for item in items:
        for node in item.childNodes:
            if node.nodeName == "arrTime":
                if now_time < node.childNodes[0].nodeValue:
                    arrive_time = node.childNodes[0].nodeValue
                    now_arrive_flag = 1
            if now_arrive_flag == 1 & first_1 == 1:
                if node.nodeName == "endSubwayStationNm":
                    global now_arrive_U
                    now_arrive_U = end_station + " train" + str(arrive_time) + "at arrive"
                    print(now_arrive_U)
                    first_1 -= 1

    upDownTypeCode = "D"
    if (station_code[3] == "2") & (upDownTypeCode == "D"):
        end_station = "YangSan"
    apiurl1 = "http://openapi.tago.go.kr/openapi/service/SubwayInfoService/getSubwaySttnAcctoSchdulList?ServiceKey=4YstE1tC4r8vbbmmDCGqQ3P65YsFYZOPASjitkuyZUNfgwKG3gCy0QZpKfWzjIUKaZPYZOtCgfm7uPyxw5jcbA%3D%3D&subwayStationId=PSS222&upDownTypeCode=D&dailyTypeCode=01&numOfRows=999"
    dom1 = minidom.parse(urllib.urlopen(apiurl1))
    # 파싱시작
    items1 = dom1.getElementsByTagName("item")
    now1 = datetime.datetime.now()
    now_time1 = now1.strftime('%H%M%S')
    now_arrive_flag = 0
    first_2 = 1
    for item in items1:
        for node in item.childNodes:
            if node.nodeName == "arrTime":
                if now_time1 < node.childNodes[0].nodeValue:
                    arrive_time = node.childNodes[0].nodeValue
                    now_arrive_flag = 1
            if now_arrive_flag == 1 & first_2 == 1:
                if node.nodeName == "endSubwayStationNm":
                    global now_arrive_D
                    now_arrive_D = end_station + " train " + str(arrive_time) + " at arrive"
                    print(now_arrive_D)
                    first_2 -= 1


CAM_ID = 0

cam = cv2.VideoCapture(CAM_ID)
if cam.isOpened() == False:
    print
    "Can't open the CAM(%d)" % (CAM_ID)
    exit()

cv2.namedWindow('CAM_Window', cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty('CAM_Window', cv2.WND_PROP_FULLSCREEN, cv2.cv.CV_WINDOW_FULLSCREEN)

ip_parser()
weather_status = weather_parse()
mise_status = mise_parse()
metro_parse()
weather_str = "Weather : "+ weather_status
mise_str = "Fine Dust : "+ mise_status
U_arrive_str = now_arrive_U
D_arrive_str = now_arrive_D

while True:
    ret, frame = cam.read()
    ########### 추가 ##################
    # frame이라는 이미지에 글씨 넣는 함수
    # frame : 카메라 이미지
    # str : 문자열 변수
    # (0, 100) : 문자열이 표시될 좌표 x = 0, y = 100
    # cv2.FONT_HERSHEY_SCRIPT_SIMPLEX : 폰트 형태
    # 1 : 문자열 크기(scale) 소수점 사용가능
    # (0, 255, 0) : 문자열 색상 (r,g,b)
    cv2.putText(frame, weather_str, (50, 50), 2, 0.5, (255, 255, 255))
    cv2.putText(frame, mise_str, (50, 80), 2, 0.5, (255, 255, 255))
    cv2.putText(frame, U_arrive_str, (50, 110), 2, 0.5, (255, 255, 255))
    cv2.putText(frame, D_arrive_str, (50, 140), 2,0.5, (255, 255, 255))

    cv2.imshow('CAM_Window', frame)
    # 10ms 동안 키입력 대기
    if cv2.waitKey(10) >= 0:
        #cv2.destroyWindow('CAM_Window')
        break

cam.release()
cv2.destroyWindow('CAM_Window')