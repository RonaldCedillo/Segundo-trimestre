from machine import Pin, I2C
import ssd1306
import time

 
i2c = I2C(0, scl=Pin(22), sda=Pin(21))

oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)


oled.text("Hola mundo", 10, 10)


for i in range(1, 11):
    oled.fill(0)
    oled.text("Hola mundo", 10, 10)
    oled.text(f"Cuenta: {i}", 10, 30)  
    oled.show()
    time.sleep(1)  
