import board, time, digitalio, busio
from lcd.lcd import LCD, CursorMode
from lcd.i2c_pcf8574_interface import I2CPCF8574Interface

def main():
    # game logic
    numDeaths = 0
    clicked = False
    
    # pins for button and LED and setup
    clickerButton = digitalio.DigitalInOut(board.GP0)
    clickerButton.direction = digitalio.Direction.INPUT
    clickerButton.pull = digitalio.Pull.UP
    led = digitalio.DigitalInOut(board.GP13)
    led.direction = digitalio.Direction.OUTPUT
    
    # LCD Screen pins and setup
    i2c_scl = board.GP9
    i2c_sda = board.GP8
    i2c_address = 0x27 #obtained from Freenove documentation, most boards have this address
    lcd_rows = 2
    lcd_cols = 16
    
    i2c = busio.I2C(scl=i2c_scl, sda=i2c_sda)
    interface = I2CPCF8574Interface(i2c, i2c_address)
    lcd = LCD(interface, num_rows=lcd_rows, num_cols=lcd_cols)
    lcd.set_cursor_mode(CursorMode.HIDE)
    lcd.clear()
    lcd.print(f"Deaths:\n{numDeaths}")
    
    
    while True:
        if clickerButton.value:
            #print('button not pressed')
            led.value = False
            clicked = False
        else:
            if clicked == False:
                numDeaths += 1
                print (f'deaths: {numDeaths}')
                lcd.clear()
                lcd.print(f"Deaths:\n{numDeaths}")
                clicked = True
            #print ('button pressed')
            led.value = True

        time.sleep(0.01)
            

main()
        