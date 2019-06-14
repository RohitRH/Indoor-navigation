#!/usr/bin/python3
import time,requests
count = 0 
try:
    while True:
        print(requests.get("http://troshos.serveo.net"),count)
        time.sleep(60)
        count+=1
except:
    exit("bye")
