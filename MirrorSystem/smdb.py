import pymysql

def getTemp() :
	conn = pymysql.connect(host='113.198.236.96', user='root', password='flvmfptl1', db='smartmirror', charset='utf8')
	curs = conn.cursor(pymysql.cursors.DictCursor)
	sql = "select * from temperature"
	curs.execute(sql)
	rows = curs.fetchall()
	conn.close()
	return rows

def getSchedule() :
	conn = pymysql.connect(host='113.198.236.96', user='root', password='flvmfptl1', db='smartmirror', charset='utf8')
	curs = conn.cursor(pymysql.cursors.DictCursor)
	sql = "select * from schedule where date(schedule_time) = date(now())"
	curs.execute(sql)
	rows = curs.fetchall()
	conn.close()
	return rows

def getMetroStation(lat, lng) :
	conn = pymysql.connect(host='113.198.236.96', user='root', password='flvmfptl1', db='smartmirror', charset='utf8')
	curs = conn.cursor(pymysql.cursors.DictCursor)
	sql = "SELECT _id, (6371*acos(cos(radians(%s))*cos(radians(gpsY))*cos(radians(gpsX)-radians(%s))+sin(radians(%s))*sin(radians(gpsY)))) AS distance, gpsX, gpsY, station_name, station_code FROM metro_station HAVING distance < 5 ORDER BY distance LIMIT 1"
	curs.execute(sql, (lat,lng,lat))
	rows = curs.fetchall()
	conn.close()
	return rows
