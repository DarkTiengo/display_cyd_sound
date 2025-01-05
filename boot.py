'''Micropython ILI9341 with xpt2046 touch screen demo for CYD
    libraries and boilerplate altered from @rdagger ili9341 repo
    https://raw.githubusercontent.com/rdagger/micropython-ili9341
'''

from ili9341 import Display, color565
from xpt2046 import Touch
from machine import idle, Pin, SPI, PWM, UART
from time import sleep
import random

uart = UART(2,baudrate=115200,rx=27,tx=22,rxbuf=1024)


CYAN = color565(0, 255, 255)
PURPLE = color565(255, 0, 255)
YELLOW = color565(255,255,0)
WHITE = color565(255, 255, 255)
BLACK = color565(0,0,0)

is_active = True

red_led = PWM(Pin(4),5000)
green_led = PWM(Pin(16),5000)
blue_led = PWM(Pin(17),5000)

'''
Display Pins:
IO2 	TFT_RS 	AKA: TFT_DC
IO12 	TFT_SDO 	AKA: TFT_MISO
IO13 	TFT_SDI 	AKA: TFT_MOSI
IO14 	TFT_SCK 	
IO15 	TFT_CS 	
IO21 	TFT_BL

Touch Screen Pins:
IO25 	XPT2046_CLK 	
IO32 	XPT2046_MOSI 	
IO33 	XPT2046_CS 	
IO36 	XPT2046_IRQ 	
IO39 	XPT2046_MISO
'''
    
    
''' Set up the display - ili9341
    Baud rate of 40000000 seems about the max '''
spi1 = SPI(1, baudrate=40000000, sck=Pin(14), mosi=Pin(13))
display = Display(spi1, dc=Pin(2), cs=Pin(15), rst=Pin(0))
x_inicial = display.width - 20
conexao = "Desconectado"
musica,titulo,artista,album = "Parada"," "," "," "


bl_pin = Pin(21, Pin.OUT)
bl_pin.on()

# Função para desenhar o sintonizador horizontal
def draw_tuner(display, frequency):
    # Cores
    WHITE = color565(255, 255, 255)
    RED = color565(255, 0, 0)
    BLACK = color565(0, 0, 0)
    GREEN = color565(0, 255, 0)

    # Dimensões do Sintonizador
    x_start = 30    # Posição X inicial
    y_start = 30   # Posição Y inicial
    width = 20     # Largura do sintonizador
    height = 200     # Altura do sintonizador
    freq_min = 88   # Frequência mínima (88 MHz)
    freq_max = 108  # Frequência máxima (108 MHz)
    # Limpa a área do sintonizador
    display.fill_rectangle(x_start, y_start, width, height, BLACK)

    # Desenha a borda do sintonizador
    display.draw_rectangle(x_start, y_start, width, height, WHITE)

    # Desenha as linhas de marcação de frequência
    for i in range(freq_min, freq_max + 1, 2):  # Linhas a cada 2 MHz
        y_pos = y_start + int((i - freq_min) / (freq_max - freq_min) * height)
        display.draw_line(x_start, y_pos, x_start + width, y_pos, WHITE)

    # Desenha o ponteiro da frequência atual
    freq_pos = y_start + int((frequency - freq_min) / (freq_max - freq_min) * height)
    display.draw_line(x_start, freq_pos, x_start + width, freq_pos, RED)

    # Exibe as frequências mínimas e máximas
    display.draw_text8x8(x_start - 30, y_start, f"{freq_min} MHz", GREEN,rotate=90)
    display.draw_text8x8(x_start - 30, y_start + height - 10, f"{freq_max} MHz", GREEN,rotate=90)

def play_pause():
    global is_active
    if not is_active:
        display.fill_rectangle(x_inicial - 150, display.width //2 -20, 50, 80 ,WHITE)
        display.fill_rectangle(x_inicial - 140, display.width //2 -5, 30, 20 ,BLACK)
        display.fill_rectangle(x_inicial - 140, display.width //2 + 25, 30, 20 ,BLACK)
        is_active = True
        red_led.duty(1023)
        green_led.duty(1023)
        blue_led.duty(0)
        uart.write("play")
    else:
        display.fill_rectangle(x_inicial - 150, display.width //2 -20, 50, 80 ,BLACK)
        display.draw_rectangle(x_inicial - 150, display.width //2 - 20, 50, 80 ,WHITE)
        display.fill_polygon(3,x_inicial - 125,display.width //2 + 18,20,WHITE,90)
        is_active = False
        red_led.duty(0)
        green_led.duty(0)
        blue_led.duty(1023)
        uart.write("pausa")

def touchscreen_press(x,y):
    global display
    x_calibrate = display.width -1 -x
    y_calibrate = display.height -1 -y
    
    if x_calibrate > 100 and x_calibrate < 200:
        freq = random.uniform(88,108)
        draw_tuner(display, freq)
        if y_calibrate >20 and y_calibrate < 90:
            uart.write("retroceder")
        elif y_calibrate >110 and y_calibrate < 180:
            play_pause()
        elif y_calibrate >210 and y_calibrate < 280:
            uart.write("avanca")
        

# Set up the touch screen digitizer - xpt2046
spi2 = SPI(2, baudrate=1000000, sck=Pin(25), mosi=Pin(32), miso=Pin(39))
touch = Touch(spi2, cs=Pin(33), int_pin=Pin(36),int_handler=touchscreen_press)
display.clear()


def printDisplay():
    global x_inicial,conexao,titulo,artista,album
    
    display.draw_text8x8(x_inicial, display.height // 2 - 80,"DarkTiengo ESP Music",WHITE,background=BLACK,rotate=90)
    display.draw_line(x_inicial - 5, 5 , x_inicial - 5, display.height - 5, WHITE)
    
    display.draw_text8x8(x_inicial - 20, 5, "LIMPAR TODO O TEXTO POSSIVEL ATE O FIM DA TELA",BLACK,rotate=90)
    display.draw_text8x8(x_inicial - 20, 5,conexao, CYAN, rotate=90)
    
    
    display.draw_text8x8(x_inicial - 40, 5,"Titulo: ", YELLOW, rotate=90)
    display.draw_text8x8(x_inicial - 40, 62, "LIMPAR TODO O TEXTO POSSIVEL ATE O FIM DA TELA",BLACK,rotate=90)
    display.draw_text8x8(x_inicial - 40, 62,titulo, WHITE, rotate=90)
    
    display.draw_text8x8(x_inicial - 60, 5,"Artista: ", YELLOW, rotate=90)
    display.draw_text8x8(x_inicial - 60, 70, "LIMPAR TODO O TEXTO POSSIVEL ATE O FIM DA TELA",BLACK,rotate=90)
    display.draw_text8x8(x_inicial - 60, 70,artista, WHITE, rotate=90)
    
    
    display.draw_text8x8(x_inicial - 80, 5,"Album: ", YELLOW, rotate=90)
    display.draw_text8x8(x_inicial - 80, 55, "LIMPAR TODO O TEXTO POSSIVEL ATE O FIM DA TELA",BLACK,rotate=90)
    display.draw_text8x8(x_inicial - 80, 55,album, WHITE, rotate=90)
    
    display.fill_rectangle(x_inicial - 150, display.width //2 -20, 50, 80 ,WHITE)
    display.fill_rectangle(x_inicial - 140, display.width //2 -5, 30, 20 ,BLACK)
    display.fill_rectangle(x_inicial - 140, display.width //2 + 25, 30, 20 ,BLACK)
    
    display.draw_rectangle(x_inicial - 150, display.width //2 -110, 50, 80 ,WHITE)
    display.fill_polygon(3,x_inicial - 125,display.width //2 -75,15,WHITE,270)
    display.fill_polygon(3,x_inicial - 125,display.width //2 -60,15,WHITE,270)
    
    display.draw_rectangle(x_inicial - 150, display.width - 50, 50, 80 ,WHITE)
    display.fill_polygon(3,x_inicial - 125,display.width -20,15,WHITE,90)
    display.fill_polygon(3,x_inicial - 125,display.width -5,15,WHITE,90)
    
    draw_tuner(display,100.5)

red_led.duty(0)
green_led.duty(1023)
blue_led.duty(1023)
printDisplay()


buffer = ""

while True:
    if uart.any():  # Verifica se há dados disponíveis
        data = uart.read()
        try:
            buffer += data.decode("utf-8")  # Adiciona os dados ao buffer
            if '\n' in buffer:  # Verifica se há uma mensagem completa
                messages = buffer.split('\n')  # Divide as mensagens pelo delimitador '\n'
                for msg in messages[:-1]:  # Processa todas as mensagens completas
                    msg = msg.strip()  # Remove espaços extras no início e no final
                    if msg.startswith("Artista:"):  
                        artista = msg.replace("Artista:","",1).strip()
                        printDisplay()
                    elif msg.startswith("Titulo:"):
                        titulo = msg.replace("Titulo:","",1).strip()
                        printDisplay()
                    elif msg.startswith("Album:"):
                        album = msg.replace("Album:","",1).strip()
                        printDisplay()
                    elif msg.startswith("Conexao:"):
                        conexao = msg.replace("Conexao:","",1).strip()
                        printDisplay()
                        if conexao == "Conectado":
                            red_led.duty(1023)
                            blue_led.duty(0)
                        else:
                            blue_led.duty(1023)
                            red_led.duty(0)
                    elif msg.startswith("Musica:"):
                        musica = msg.replace("Musica:","",1).strip()
                        if musica == "Iniciada":
                            is_active = True
                            play_pause()
                        else:
                            is_active = False
                            play_pause()
                buffer = messages[-1]
        except UnicodeError as e:
            print("Error: Artefatos na UART")
    sleep(0.05)  # Pequeno delay para reduzir a carga no loop


