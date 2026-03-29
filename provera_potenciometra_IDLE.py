import time
import  board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from rpi_lcd import LCD

#1. Inicijalizacija
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
ads.gain = 1
chan = AnalogIn(ads, 0)
lcd = LCD()

print("-- ANALOG ONLINE --")
print("Pomeraj dzojstik i prati brojeve")

try:
    while True:
        val = chan.value
        volt = chan.voltage

        #ispis u Thonny Shell
        print(f"Sirova vrednost: {val:5d} | Napon: {volt:3f}V")

        #Ispis na tvoj LCD
        lcd.text(f"Pot: {val}", 1)
        if val > 20000:
            lcd.text("Status: DESNO", 2)
        elif val < 10000:
            lcd.text("Status: LEVO", 2)
        else:
            lcd.text("Status: MIRUJE", 2)

        time.sleep(0.1) # Da ne treperi ekran prebrzo
except KeyboardInterrupt:
    lcd.clear()
    print("Test zavrsen.")