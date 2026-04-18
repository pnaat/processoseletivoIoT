from machine import Pin, ADC, PWM
import config

class LDRMatrix:
    def __init__(self):
        self.tl = ADC(Pin(config.PIN_LDR_TL))
        self.tr = ADC(Pin(config.PIN_LDR_TR))
        self.bl = ADC(Pin(config.PIN_LDR_BL))
        self.br = ADC(Pin(config.PIN_LDR_BR))

        for ldr in (self.tl, self.tr, self.bl, self.br):
            ldr.atten(ADC.ATTN_11DB)
            ldr.width(ADC.WIDTH_12BIT)

    def read_all(self):
        try:
            return {
                'tl': self.tl.read(),
                'tr': self.tr.read(),
                'bl': self.bl.read(),
                'br': self.br.read(),
            }
        except Exception as e:
            print(f"HW Fault - LDR read failed: {e}")
            return {
                'tl': 0,
                'tr': 0,
                'bl': 0,
                'br': 0
            }

class SolarServo:
    def __init__(self, pin, start_angle=90):
        self.pwm = PWM(Pin(pin), freq=config.SERVO_FREQ)
        self.current_angle = start_angle
        self.set_angle(start_angle)

    def set_angle(self, angle):
        angle = max(0, min(180, angle))

        duty = int(
            config.SERVO_MIN_DUTY +
            angle / 180 * (config.SERVO_MAX_DUTY - config.SERVO_MIN_DUTY) 
        )

        self.pwm.duty(duty)
        self.current_angle = angle
