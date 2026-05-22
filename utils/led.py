# class of leds to import in other files and use
from machine import Pin, PWM
from time import sleep

class Led:
    MAX_DUTY_CYCLE = 65535
    current_val = 100

    def __init__(self, pin: int) -> None:
        self.pin = PWM(Pin(pin))

        self.pin.freq(1000)
        self.wait()
        self.set(self.current_val) # start with it turned on
        self.wait()

    def wait(self):
        # execute at end of every command to wait that leds update
        sleep(0.01)

    def set(self, percent: int):
        if not 0 <= percent <= 100:
            print("percent error")
            return

        self.current_val = percent
        self.pin.duty_u16(self.MAX_DUTY_CYCLE // 100 * percent)
        self.wait()

    def set_n(self, n: int):
        # as set but not in percent directly in value (can be useful)
        if not 0 <= n <= self.MAX_DUTY_CYCLE:
            print("number error")
            return

        self.pin.duty_u16(n)
        self.wait()


    def off(self):
        self.set(0)

    def on(self):
        self.set(self.current_val)

    def toggle(self):
        self.pin.duty_u16(
            abs(self.pin.duty_u16() - self.MAX_DUTY_CYCLE) if self.pin.duty_u16() in [0, self.MAX_DUTY_CYCLE] else 0
        )
        self.wait()



shop_led = Led(33)
ceiling_led = Led(26)
