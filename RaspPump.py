import RPi.GPIO as GPIO
import time
from gpiozero import MCP3208
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

# リレーモジュールPIN
Relay_PIN = 4

# リレー有効の場合はTrue
RELAY_STATUS = False
# 初期化処理
def setup():
    GPIO.setwarnings(True)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(Relay_PIN, GPIO.IN)

# リレーモジュールをONにする
def relay_on():
    global RELAY_STATUS

    if RELAY_STATUS is not True:
        # リレーON
        GPIO.setup(Relay_PIN, GPIO.OUT)
        RELAY_STATUS = True

# リレーモジュールをOFFにする
def relay_off():
    global RELAY_STATUS

    if RELAY_STATUS is not False:
        # リレーOFF
        GPIO.setup(Relay_PIN, GPIO.IN)
        RELAY_STATUS = False

DRY_THRESH = 0.6

def main():
    # 初期化
    Vref = 3.3
    factory = PiGPIOFactory()
    adc_ch0 = MCP3208(channel=0, max_voltage=Vref, pin_factory=factory)
    setup()

    while True:
        # MCP3002からの出力値と電圧値を表示
        val = adc_ch0.value
        if val > DRY_THRESH:
            print(f'dry - value:{val:.2f}')
            relay_on()

        elif val < DRY_THRESH:
            print(f'moist - value:{val:.2f}')
            relay_off()
        sleep(1)
    return
    
def destroy():
    GPIO.setup(Relay_PIN, GPIO.IN)
    GPIO.cleanup()

if __name__ == "__main__":
    try:
        main()

    except:
        print("error!!")

    finally:
        destroy()

