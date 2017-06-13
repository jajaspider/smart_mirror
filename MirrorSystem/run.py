import urllib.request
import socket
import datetime
import math
from xml.dom import minidom

hostName = socket.gethostname()
ip = socket.gethostbyname(hostName)
servicekey = "4YstE1tC4r8vbbmmDCGqQ3P65YsFYZOPASjitkuyZUNfgwKG3gCy0QZpKfWzjIUKaZPYZOtCgfm7uPyxw5jcbA%3D%3D"


def ip_parser():
    global gps_x
    global gps_y
    try:
        input_url = "http://ip-api.com/line/" + ip
        readurl = urllib.request.urlopen(input_url).read()
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


ip_parser()
apiurl = grid(float(gps_x), float(gps_y))
dom = minidom.parse(urllib.request.urlopen(apiurl))
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
                    print("[날씨] 맑음")
                    print('---------------------')
                if node.childNodes[0].nodeValue == "2":
                    print("[날씨] 구름조금")
                    print('---------------------')
                if node.childNodes[0].nodeValue == "3":
                    print("[날씨] 구름많음")
                    print('---------------------')
                if node.childNodes[0].nodeValue == "4":
                    print("[날씨] 흐림")
                    print('---------------------')

apiurl = "http://opendata.busan.go.kr/openapi/service/AirQualityInfoService/getAirQualityInfoClassifiedByStation?ServiceKey=4YstE1tC4r8vbbmmDCGqQ3P65YsFYZOPASjitkuyZUNfgwKG3gCy0QZpKfWzjIUKaZPYZOtCgfm7uPyxw5jcbA%3D%3D"
dom = minidom.parse(urllib.request.urlopen(apiurl))
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
                    print("[미세먼지] 좋음")
                    print('---------------------')
                if temp_pm10Cai == "2":
                    print("[미세먼지] 보통")
                    print('---------------------')
                if temp_pm10Cai == "3":
                    print("[미세먼지] 나쁨")
                    print('---------------------')
                if temp_pm10Cai == "4":
                    print("[미세먼지] 매우나쁨")
                    print('---------------------')

apiurl = "http://openapi.tago.go.kr/openapi/service/SubwayInfoService/getSubwaySttnAcctoSchdulList?ServiceKey=4YstE1tC4r8vbbmmDCGqQ3P65YsFYZOPASjitkuyZUNfgwKG3gCy0QZpKfWzjIUKaZPYZOtCgfm7uPyxw5jcbA%3D%3D&subwayStationId=PSS222&upDownTypeCode=U&dailyTypeCode=01&numOfRows=999"
dom = minidom.parse(urllib.request.urlopen(apiurl))
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
                print(node.childNodes[0].nodeValue + "행 열차가 " + arrive_time + "에 도착 예정입니다.")
                first_1 -= 1

apiurl1 = "http://openapi.tago.go.kr/openapi/service/SubwayInfoService/getSubwaySttnAcctoSchdulList?ServiceKey=4YstE1tC4r8vbbmmDCGqQ3P65YsFYZOPASjitkuyZUNfgwKG3gCy0QZpKfWzjIUKaZPYZOtCgfm7uPyxw5jcbA%3D%3D&subwayStationId=PSS222&upDownTypeCode=D&dailyTypeCode=01&numOfRows=999"
dom1 = minidom.parse(urllib.request.urlopen(apiurl1))
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
                print(node.childNodes[0].nodeValue + "행 열차가 " + arrive_time + "에 도착 예정입니다.")
                first_2 -= 1
