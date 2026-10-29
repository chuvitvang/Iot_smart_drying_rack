# Driver MicroPython thu gọn cho module ADS1115 (16-bit I2C ADC)
# Tối ưu hóa bộ nhớ cho ESP8266 (WeMos D1)
import time

_ADS1115_ADDR = 0x48
_REG_CONV = 0x00
_REG_CONFIG = 0x01

# Cấu hình MUX cho single-ended inputs
# A0: 0x4000, A1: 0x5000, A2: 0x6000, A3: 0x7000
_MUX_SINGLE = [0x4000, 0x5000, 0x6000, 0x7000]

class ADS1115:
    """
    Driver ADS1115 giao tiếp I2C.
    Hỗ trợ đọc giá trị raw ADC (0-32767) theo kênh single-ended.
    """
    def __init__(self, i2c, address=_ADS1115_ADDR, gain=1):
        self.i2c = i2c
        self.address = address
        # Gain 1: +/- 4.096V (Phù hợp với điện áp 3.3V của ESP8266)
        # Gain bits [11:9]: 1 -> 0x0200
        self.gain_config = 0x0200
        self.buf = bytearray(2)

    def read_raw(self, channel):
        """Đọc giá trị số nguyên 16-bit từ kênh channel (0 -> 3)."""
        if channel < 0 or channel > 3:
            raise ValueError("Kenh phai trong khoang 0-3")

        # 0x8000: Bat dau chuyen doi (OS = 1)
        # _MUX_SINGLE[channel]: Kenh ADC
        # self.gain_config: Dai do dien ap
        # 0x0100: Che do Single-shot
        # 0x0080: Toc do lay mau 128 SPS
        # 0x0003: Vo hieu hoa comparator
        config = 0x8000 | _MUX_SINGLE[channel] | self.gain_config | 0x0100 | 0x0080 | 0x0003

        self.buf[0] = (config >> 8) & 0xFF
        self.buf[1] = config & 0xFF
        self.i2c.writeto_mem(self.address, _REG_CONFIG, self.buf)

        # Cho chuyen doi hoan tat (128 SPS mat ~8ms)
        time.sleep_ms(10)

        # Doc ket qua tu Conversion Register
        self.i2c.readfrom_mem_into(self.address, _REG_CONV, self.buf)
        val = (self.buf[0] << 8) | self.buf[1]

        # Chuyen doi sang so co dau 16-bit
        if val > 32767:
            val -= 65536

        # Doi voi single-ended, gia tri luon >= 0
        return max(0, val)
