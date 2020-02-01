import pyaudio
import numpy as np
import wave
from datetime import datetime, timedelta
import platform
import sched
import time
import capture_wave
import startSync
try :
    this_time = startSync.sync()
    #ここから返信ですぅ


    freq = 2000
    dur = 2000
    if platform.system() == "Windows":
        # Windowsの場合は、winsoundというPython標準ライブラリを使います.
        import winsound
        winsound.Beep(freq, dur)
    else:
        # Macの場合には、Macに標準インストールされたplayコマンドを使います.
        import os
        os.system('play -n synth %s sin %s' % (dur/1000, freq))
    #同期
    now = datetime.now()
    comp = datetime(now.year, now.month, now.day, now.hour, now.minute+1,0)
    print(now)
    print(comp)
    diff = comp - now
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(diff.seconds, 1, capture_wave.get_wave )
    #スタート
    scheduler.run()

except KeyboardInterrupt:   
    print('keyborad')