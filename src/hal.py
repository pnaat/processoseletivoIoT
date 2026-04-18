from machine import Pin, ADC, PWM
import config

class LDRMatrix:
    def __init__(self, smoothing_factor=0.2):
        self.tl = ADC(Pin(config.PIN_LDR_TL))
        self.tr = ADC(Pin(config.PIN_LDR_TR))
        self.bl = ADC(Pin(config.PIN_LDR_BL))
        self.br = ADC(Pin(config.PIN_LDR_BR))

        self.alpha = smoothing_factor
        self.filtered_values = {'tl': 0, 'tr': 0, 'bl': 0, 'br': 0}

        for ldr in (self.tl, self.tr, self.bl, self.br):
            ldr.atten(ADC.ATTN_11DB)
            ldr.width(ADC.WIDTH_12BIT)

        self._initialize_filters()

    def _initialize_filters(self):
        self.filtered_values = {
            'tl': self.tl.read(),
            'tr': self.tr.read(),
            'bl': self.bl.read(),
            'br': self.br.read(),
        }

    def read_filtered(self):
        try:
            raw = {
                'tl': self.tl.read(),
                'tr': self.tr.read(),
                'bl': self.bl.read(),
                'br': self.br.read(),
            }

            for key in self.filtered_values:
                self.filtered_values[key] = (raw[key] * self.alpha) + (self.filtered_values[key] * (1 - self.alpha))

            return self.filtered_values
            
        except Exception as e:
            print(f"HW Fault - LDR read failed: {e}")
            return self.filtered_values

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

    def get_current_angle(self):
        return self.current_angle
