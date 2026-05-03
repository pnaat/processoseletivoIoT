"""
Drives e parâmetros base de config recomendados para uso do board-ssd1306 no simulador Wokwi.
"""

from micropython import const
import framebuf

SET_DISP = const(0xAE)
SET_MEM_ADDR = const(0x20)
SET_COL_ADDR = const(0x21)
SET_PAGE_ADDR = const(0x22)
SET_DISP_START_LINE = const(0x40)
SET_SEG_REMAP = const(0xA1)
SET_MUX_RATIO = const(0xA8)
SET_COM_OUT_DIR = const(0xC8)
SET_DISP_OFFSET = const(0xD3)
SET_COM_PIN_CFG = const(0xDA)
SET_DISP_CLK_DIV = const(0xD5)
SET_PRECHARGE = const(0xD9)
SET_VCOM_DESEL = const(0xDB)
SET_CONTRAST = const(0x81)
SET_ENTIRE_ON = const(0xA4)
SET_NORM_INV = const(0xA6)
SET_CHARGE_PUMP = const(0x8D)
SET_DISP_ON = const(0xAF)

class SSD1306_I2C:
    def __init__(self, width, height, i2c, addr=0x3C):
        self.i2c = i2c
        self.addr = addr
        self.width = width
        self.height = height
        self.pages = height // 8
        self.buffer = bytearray(self.pages * width)
        self.framebuf = framebuf.FrameBuffer(self.buffer, width, height, framebuf.MONO_VLSB)
        self.init_display()

    def write_cmd(self, cmd):
        self.i2c.writeto(self.addr, b'\x00' + bytes([cmd]))

    def write_data(self, buf):
        self.i2c.writeto(self.addr, b'\x40' + buf)

    def init_display(self):
        for cmd in (
            SET_DISP,
            SET_MEM_ADDR, 0x00,
            SET_DISP_START_LINE,
            SET_SEG_REMAP,
            SET_MUX_RATIO, self.height - 1,
            SET_COM_OUT_DIR,
            SET_DISP_OFFSET, 0x00,
            SET_COM_PIN_CFG, 0x12,
            SET_DISP_CLK_DIV, 0x80,
            SET_PRECHARGE, 0xF1,
            SET_VCOM_DESEL, 0x30,
            SET_CONTRAST, 0xFF,
            SET_ENTIRE_ON,
            SET_NORM_INV,
            SET_CHARGE_PUMP, 0x14,
            SET_DISP_ON
        ):
            self.write_cmd(cmd)

        self.fill(0)
        self.show()

    def fill(self, col):
        self.framebuf.fill(col)

    def text(self, string, x, y):
        self.framebuf.text(string, x, y)

    def show(self):
        self.write_cmd(SET_COL_ADDR)
        self.write_cmd(0)
        self.write_cmd(self.width - 1)
        self.write_cmd(SET_PAGE_ADDR)
        self.write_cmd(0)
        self.write_cmd(self.pages - 1)
        self.write_data(self.buffer)