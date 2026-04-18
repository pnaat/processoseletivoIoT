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

