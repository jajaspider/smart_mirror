#!/usr/bin/python3
#-*- coding: utf-8 -*-
import csv
import pymysql

conn = pymysql.connect(host='localhost', user='root', password='flvmfptl1', db='smartmirror', charset='utf8')
cursor = conn.cursor()
sql = """insert into metro_station values (NULL, %s, %s, %s, %s)"""

f = open('metro.csv', 'r')
rdr = csv.reader(f)
#rdr = codecs.open('metro.csv','r',encoding='utf-8')

for line in rdr:
    cursor.execute(sql, (line[1], line[3], line[2], line[4]))
    conn.commit()
    print(line[1] + "역 " + " Y : " + line[2] + " X: " + line[3] +" 역코드 : "+line[4])

conn.close()
