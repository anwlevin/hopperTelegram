# launch_bot.py
import signal
import subprocess
import time

from makeIndex import makeIndex

print('🏀', 'run.py')
#p = subprocess.call(["python", "main.py"])

p = subprocess.Popen(["python", "main.py"])
time.sleep(60)

p.kill()
print('🏀🏀', 'KILL run.py')

print('🏀', 'make.index')

makeIndex()



