import time
import py2_weather_click as weather
import py2_aws_click as aws
def setup():
    aws.resetaws()
    aws.setup()

    weather.setup()

    print "setup complete"

    
def main():
    setup()
    while True:
        jsonmsg = ''

        jsonmsg = weather.getdata(jsonmsg)
        jsonlen = len(jsonmsg)

        aws.sendcmd("AT+AWSPUBLISH=0,%d\r\n" % jsonlen)
        aws.recvdata('>')    
        aws.sendcmd(jsonmsg)
        aws.recvdata('OK\r\n')

        # frequency of reading
        time.sleep(30)

    ser.close()

if __name__=="__main__":
    main()
