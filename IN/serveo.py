import time,requests
from threading import Thread
from subprocess import run
import sys

if len(sys.argv) > 1:
    domain = sys.argv[1]
    print("Using custom domain : {}".format(domain))
else:
    domain = 'troshos'
    print("Using default domain : 'troshos'")

def background():
    run(['ssh','-R','{}:80:localhost:5000'.format(domain),'serveo.net'],close_fds=True)

t = Thread(target=background)
t.start()

count = 0
try:
    while True:
        time.sleep(60)
        requests.get("http://{}.serveo.net".format(domain))
        count+=1
except:
    exit("Server was online for {} minutes : {}\nbye".format(count))