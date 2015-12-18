import sys
import os 
import subprocess

num=int(sys.argv[1])
count = 0

prog_dir = os.path.dirname(os.path.abspath(__file__))

f = open("%s/id.csv" %prog_dir, "r+")
for lines in f:
    count = count+1
f.close()

if (num < count):
    count = num 

f = open("%s/id.csv" %prog_dir, "r+")
for lines in f:
    line=lines.split(',')
    print line[0]
    prog = subprocess.Popen("python %s/client.py %s &" %(prog_dir,line[0]), shell=True )
    count = count-1
    if count==0:
        break
f.close()
