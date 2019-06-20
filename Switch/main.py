from machine import Pin, Timer
from neopixel import NeoPixel

BLANCO = (255, 255, 255)
VERDE = (255, 0, 0)
ROJO = (0, 255, 0)
AZUL = (0, 0, 255)

# apago el buzzer
buzzer = Pin(15, Pin.OUT)
buzzer.value(0)

def cambiar_color(led, color):
    led[0] = color
    led.write()


pin_led = Pin(2, Pin.OUT)
led = NeoPixel(pin_led, 1)


class Switch:

    def __init__(self, pin_no, name):
        self._state = 0
        self.value = 0
        self.pin = Pin(pin_no)
        self.name = name
        self._pressed = False

    def setup(self):
        self.pin.init(mode=Pin.IN, pull=Pin.PULL_UP)

    def output(self):
        return self.name if self.value else '.'

    def update_internal_state(self):
        bit = self.pin.value()
        self._state = ((self._state << 1) | bit) & 0xfff
        if self._state == 0x000:
            self.value = True
            self._pressed = True
        elif self._state == 0xfff:
            self.value = False
    
    def pressed(self):
        return True if self.value else False

    def released(self):
        if self._pressed and not self.value:
            self._pressed = False
            return True
        
        return False


class Debouncer:

    def __init__(self):
        self.switches = []
        self.timer = Timer(-1)
        self.timer.init(period=6, mode=Timer.PERIODIC, callback=self.tick)

    
    def register(self, switch):
        self.switches.append(switch)
        switch.setup()
        return switch
        

    def tick(self, _):
        for switch in self.switches:
            switch.update_internal_state()

        
    
colores = [AZUL, ROJO, BLANCO, VERDE]


d = Debouncer()
s = d.register(Switch(14, "inicio"))
sb = 0
c = 0

while True:
    if s.released():
        cambiar_color(led, colores[c])
        c += 1
        if c > 3:
            c = 0