from startiot-catm1 import StartIot
import uos

def run():
    # Connect to the NB-IoT network (Requires that the modem is flashed with the CatM1 firmware)
    print('Try to connect...')
    startIoT = StartIot()
    startIoT.connect()
    print('Connected to Cat M1...')

    try:
        print("Send dummy message...")
        tmp = ((uos.urandom(1)[0] / 256) * 10) + 20
        hum = ((uos.urandom(1)[0] / 256) * 10) + 60
        msg = '"temperature":"'+ str(tmp) + '", "humidity": "'+ str(hum) + '", "latlng": "69.681812, 18.988209"'
        startIoT.send(msg)
      except:
          print("Something went wrong, exception caught...")
        pass
      time.sleep(30)

print('Run the example code...')
run()
