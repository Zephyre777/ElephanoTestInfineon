# How to work with the infineon board

First of all, connect the board to your laptop
## Install micropython on the board
```python mpy-pse.py device-setup -b KIT_PSE84_AI -v v0.1.0```

## Directly load python on board
### Load python program to PSOC48 using mpremote
```mpremote connect /dev/ttyACM0     fs cp [YOUR_PROGRAM] :[TARGET_FILE_NAME]```

### Run python program on PSOC48
``` mpremote connect /dev/ttyACM0     exec "exec(open('[TARGET_FILE_NAME]').read())"```

## Using Micropython
### Start in the terminal
```minicom -D /dev/ttyACM0 -b 115200``` \
And then press Enter

## Sample program
This program makes the LED on board blinks 10 times [led_blink.python](scripts/led_blink.python)

## running the audio recording program
to record\
```python record-audio.py record -d "connect /dev/ttyACM0" -r 16000 -b 16 -f 2 -m 1 -t 5```
to load the sound from board \ 
```python record-audio.py load```
to play the recorded \ 
```python record-audio.py play```
