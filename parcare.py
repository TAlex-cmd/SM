import time
import pigpio
import RPi.GPIO as GPIO
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
    GPIO.output(trig, GPIO.HIGH)

    time.sleep(0.00001)
    GPIO.output(trig, GPIO.LOW)

    start = time.time()
    stop = time.time()


    while GPIO.input(echo) == 0:
        start = time.time()


    while  GPIO.input(echo) == 1:
        stop = time.time()

    duration = stop - start

    distance = 34300/2 * duration

    if distance < 0.5 and distance > 400:
        return 0
    else:
        return distance

try:
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
