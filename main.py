import uos
import time
from startiot_catm1 import StartIot


def run():
    # Connect to the NB-IoT network (Requires that the modem is flashed with the CatM1 firmware)
    print('Try to connect...')
    startIoT = StartIot()
    startIoT.connect()
    print('Connected to Cat M1...')
    while True:
        try:
            print("Send dummy message:")
            tmp = ((uos.urandom(1)[0] / 256) * 10) + 20
            hum = ((uos.urandom(1)[0] / 256) * 10) + 60
            # return JSON.parse(payload.toString("utf-8")); as Uplink transform
            msg = '{"temperature":"'+ str(tmp) + '", "humidity": "'+ str(hum) + '", "latlng": "69.681812, 18.988209"}'
            print(msg)
            startIoT.send(msg)
        except Exception as e:
            print("Something went wrong, exception caught...")
            print(e)
            pass

        time.sleep(30)

print('Run the example code...')
run()
