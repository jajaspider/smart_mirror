import csv

f = open('metro.csv', 'r')
rdr = csv.reader(f)

for line in rdr:
    print(line[1] + "역 " + " Y : " + line[2] + " X: " + line[3] +" 역코드 : "+line[4])
