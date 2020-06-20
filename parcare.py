import time
import pigpio
import RPi.GPIO as GPIO
from bottle import route, run, template, request

pi = pigpio.pi()


buzzer = 18

pi.set_mode(buzzer, pigpio.OUTPUT)
GPIO.setmode(GPIO.BOARD)

trig = 32
echo = 38

GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)
GPIO.setup(8, GPIO.OUT)

def calculate_distance():
    #set the trigger to HIGH
    GPIO.output(trig, GPIO.HIGH)

    #sleep 0.00001 s and the set the trigger to LOW
    time.sleep(0.00001)
    GPIO.output(trig, GPIO.LOW)

    #save the start and stop times
    start = time.time()
    stop = time.time()

    #modify the start time to be the last time until
    #the echo becomes HIGH
    while GPIO.input(echo) == 0:
        start = time.time()

    #modify the stop time to be the last time until
    #the echo becomes LOW
    while  GPIO.input(echo) == 1:
        stop = time.time()

    #get the duration of the echo pin as HIGH
    duration = stop - start

    #calculate the distance
    distance = 34300/2 * duration

    if distance < 0.5 and distance > 400:
        return 0
    else:
        #return the distance
        return distance


@route('/')
def index():
    return template('index.html')

@route('/refresh')

def refresh():
    dist = calculate_distance()
    return '%d' % dist


try:
    run(host = '0.0.0.0', port = '5000')
    while True:

        if calculate_distance() < 25:
            if calculate_distance() < 15:
                pi.hardware_PWM(buzzer, 500, 500000)
                GPIO.output(8, GPIO.HIGH)
                time.sleep(0.05)

                pi.hardware_PWM(buzzer, 0, 0)
                GPIO.output(8, GPIO.LOW)
                time.sleep(0.05)

            elif calculate_distance() < 10:
                pi.hardware_PWM(buzzer, 500, 500000)
                GPIO.output(8, GPIO.HIGH)
                time.sleep(2)

                GPIO.output(8, GPIO.LOW)
                pi.hardware_PWM(buzzer, 0, 0)

            else:
                pi.hardware_PWM(buzzer, 500, 500000)
                GPIO.output(8, GPIO.HIGH)
                time.sleep(0.1)

                pi.hardware_PWM(buzzer, 0, 0)
                GPIO.output(8, GPIO.LOW)
                time.sleep(0.05)

        else:
            pi.hardware_PWM(buzzer, 0, 0)
            GPIO.output(8, GPIO.LOW)

        time.sleep(0.1)


except KeyboardInterrupt:
    pass

pi.write(buzzer, 0)
GPIO.output(8, GPIO.LOW)
pi.stop()


GPIO.cleanup()
