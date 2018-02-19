import time
import serial
import py2_weather_click as weather

# setup serial for AWS click
ser = serial.Serial(
    port='/dev/serial0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=0.5,
)

ser.xonxoff = False
ser.rtscts = False
ser.dsrdtr = False

reset = ser.readline()

def recvdata(waitstr):
    response = ''
    while waitstr not in response:
        ch = ser.read()
        response += ch


def sendcmd(data):
    ser.write(data)

    
def resetaws():
    print "Resyncing with AWS please wait"
    waitstr = "OK\r\n"
    ser.timeout = 0.01
    for i in range(1,50):
        idx = 0
        sendcmd('ATE0\r\n')

        response = ''
        while waitstr not in response:
            idx += 1
            ch = ser.read()
            response += ch
            if idx == 20:
                break
        if waitstr in response:
            break
    ser.timeout = 2

    
def setup():
    resetaws()
    
    sendcmd('ATE0\r\n')
    recvdata('OK\r\n')

    sendcmd('AT+AWSPUBCLOSE=0\r\n')
    recvdata('OK\r\n')

    sendcmd('AT+AWSPUBOPEN=0,"WEATHER"\r\n')
    recvdata('OK\r\n')

    weather.setup()
    print "setup complete"

def main():
    setup()
    while True:
        jsonmsg = ''

        jsonmsg = weather.getdata(jsonmsg)
        jsonlen = len(jsonmsg)

        sendcmd("AT+AWSPUBLISH=0,%d\r\n" % jsonlen)
        recvdata('>')    
        sendcmd(jsonmsg)
        recvdata('OK\r\n')

        # frequency of reading
        time.sleep(30)

    ser.close()

if __name__=="__main__":
    main()
