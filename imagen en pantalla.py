from ST7735 import TFT
from sysfont import sysfont
from sdcard import SDCard
import os
from machine import SPI, Pin, reset
import time
from time import sleep

# Configuración SPI para TFT
spi_tft = SPI(2, baudrate=20000000, polarity=0, phase=0, sck=Pin(14), mosi=Pin(13), miso=Pin(12))
tft = TFT(spi_tft, 16, 17, 18)
tft.initr()
tft.fill(TFT.BLACK)

# Configuración SPI para tarjeta SD
spi_sd = SPI(1, baudrate=10000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
cs_sd = Pin(27, Pin.OUT)
sd = SDCard(spi_sd, cs_sd)

# Función para mostrar imagen BMP
def display_bmp(file_path, display):
    try:
        os.mount(sd, '/sd')
        print("Archivos en la tarjeta SD:", os.listdir("/sd"))
        
        # Inicializar pantalla TFT y limpiar
        tft.fill(TFT.BLACK)
        
        with open(file_path, 'rb') as f:
            # Leer la cabecera del archivo BMP (61 bytes en lugar de 54)
            f.read(61)  # Cambiar de 54 a 61 bytes de la cabecera
            width, height = 128, 160  # Asegúrate que la resolución de la imagen coincida
            row_size = width * 3  # 3 bytes por pixel (RGB)
            
            for y in range(height):
                row_data = f.read(row_size)
                if not row_data:
                    print(f"Fin de la lectura de datos en la fila {y}")
                    break
                
                rgb565_row = bytearray()
                
                for i in range(0, len(row_data), 3):
                    r = row_data[i] >> 3
                    g = row_data[i + 1] >> 2
                    b = row_data[i + 2] >> 3
                    rgb565 = (r << 11) | (g << 5) | b
                    rgb565_row.extend(rgb565.to_bytes(2, 'big'))
                
                # Mostrar la fila en el TFT
                display._setwindowloc((0, y), (width - 1, y))
                display._writedata(rgb565_row)
        
        print(f"Imagen '{file_path}' mostrada correctamente.")
        os.umount('/sd')
        print("Tarjeta SD desmontada.")
    
    except Exception as e:
        print(f"Error al mostrar la imagen '{file_path}': {e}")

# Llamar a la función para mostrar la imagen
display_bmp('/sd/flammy.bmp', tft)
