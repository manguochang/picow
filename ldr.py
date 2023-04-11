from machine import ADC, Pin
import utime

ldr = ADC(Pin(28))

readDelay = 1.0

min = 1000
max = 0

while True:
    x = ldr.read_u16()
    if x < min:
        min = x
        continue
    if x > max:
        max = x
    print(f"Current: {x}, Min: {min}, Max: {max}")
    utime.sleep(readDelay)
