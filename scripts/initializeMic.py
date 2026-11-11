from machine import PDM_PCM
import time

# Configure PDM microphone pins
clk_pin = "P8_5"
data_pin = "P8_6"

# sampling rate 16KHz
# bits depth: 16 bit
# Sound channel: Mono
# Gain: 0dB

pdm_pcm = PDM_PCM(
    0,
    sck=clk_pin,
    data=data_pin,
    sample_rate=16000,
    bits=PDM_PCM.BITS_16,
    format=PDM_PCM.MONO_LEFT,
    gain=0,
)

buffer = bytearray(3200)

for i in range(32):

    size = mic.readinto(buffer)

    print("Audio Bytes:", size)

    time.sleep_ms(100)
