from machine import PWM, Pin
from neopixel import NeoPixel
import utime

BLANCO = (255, 255, 255)
VERDE = (255, 0, 0)
ROJO = (0, 255, 0)
AZUL = (0, 0, 255)

"""
freq 50 Hertz, por lo que el ciclo tiene 20ms
ese ciclo se divide en 1024 del duty
un duty de 1.5 ms hace que quede parado = 1.5 * 1024 / 20 = 76.8 Usar aprox 77 para que quede parado
un duty de 1.0 ms hace que gire CCW = 1.0 * 1024 / 20 = 51.2 usar 51 aprox para que gire
un duty de 2.0 ms hace que gire CW = 2.0 * 1024 / 20 = 102.4 usar 102 aprox para que gire
"""

# apago el buzzer
buzzer = Pin(15, Pin.OUT)
buzzer.value(0)

# setup motores
motor_der = PWM(Pin(5), freq=50)
motor_izq = PWM(Pin(4), freq=50)
motor_der.duty(0)
motor_izq.duty(0)

# setup IR
IR_der = Pin(13, Pin.IN)
IR_izq = Pin(12, Pin.IN)

pulsador = Pin(14, Pin.IN, Pin.PULL_UP)

pin_led = Pin(2, Pin.OUT)
led = NeoPixel(pin_led, 1)

def esperar_pulsador(pulsador):
    valor = pulsador.value()
    activo = 0
    while activo < 20:
        p = pulsador.value()
        if p != valor:
            activo += 1
        else:
            activo = 0
        utime.sleep_ms(1)

def cambiar_color(led, color):
    led[0] = color
    led.write()

def avanzar(velocidad=1, sentido="adelante", ajuste=(0, 0)):
    base = 75
    offset = int(velocidad * 25)
    if sentido == "adelante":
        motor_der.duty(base + ajuste[0] - offset)
        motor_izq.duty(base + ajuste[1] + offset)
        print("motor", motor_der.duty(), motor_izq.duty())
    else:
        motor_der.duty(base + ajuste[0] + offset)
        motor_izq.duty(base + ajuste[1] - offset)

def detener():
    motor_der.duty(0)
    motor_izq.duty(0)

def girar_derecha(velocidad=1, ajuste=(0, 0)):
    base = 75
    offset = int(velocidad * 25)
    motor_der.duty(base + ajuste[0] + offset)
    motor_izq.duty(base + ajuste[1] + offset)

def girar_izquierda(velocidad=1, ajuste=(0, 0)):
    base = 75
    offset = int(velocidad * 25)
    motor_der.duty(base + ajuste[0] - offset)
    motor_izq.duty(base + ajuste[1] - offset)

cambiar_color(led, BLANCO)

esperar_pulsador(pulsador)
cambiar_color(led, AZUL)
utime.sleep(1)

while True:
    if IR_der.value() == 0 and IR_izq.value() == 0:
        avanzar()
    elif IR_der.value() == 0 and IR_izq.value() == 1:
        girar_derecha()
    elif IR_der.value() == 1 and IR_izq.value() == 0:
        girar_izquierda()
    elif IR_der.value() == 1 and IR_izq.value() == 1:
        detener()

