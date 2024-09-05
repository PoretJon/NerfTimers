import board, time, digitalio, busio
from lcd.lcd import LCD, CursorMode
from lcd.i2c_pcf8574_interface import I2CPCF8574Interface

# init pins
redButton = digitalio.DigitalInOut(board.GP21)
blueButton = digitalio.DigitalInOut(board.GP22)
resetButton = digitalio.DigitalInOut(board.GP16)
modeButton = digitalio.DigitalInOut(board.GP18)
timeUpButton = digitalio.DigitalInOut(board.GP15)
timeDownButton = digitalio.DigitalInOut(board.GP13)
redLED = digitalio.DigitalInOut(board.GP28)
blueLED = digitalio.DigitalInOut(board.GP27)
i2c_scl = board.GP9
i2c_sda = board.GP8

# set pins
redButton.direction = digitalio.Direction.INPUT
blueButton.direction = digitalio.Direction.INPUT
resetButton.direction = digitalio.Direction.INPUT
modeButton.direction = digitalio.Direction.INPUT
timeUpButton.direction = digitalio.Direction.INPUT
timeDownButton.direction = digitalio.Direction.INPUT
redButton.pull = digitalio.Pull.UP
blueButton.pull = digitalio.Pull.UP
resetButton.pull = digitalio.Pull.UP
modeButton.pull = digitalio.Pull.UP
timeUpButton.pull = digitalio.Pull.UP
timeDownButton.pull = digitalio.Pull.UP

redLED.direction = digitalio.Direction.OUTPUT
blueLED.direction = digitalio.Direction.OUTPUT


# set screen
i2c = busio.I2C(scl=i2c_scl, sda=i2c_sda)
i2c_address = 0x27 #obtained from Freenove documentation, most boards have this address
interface = I2CPCF8574Interface(i2c, i2c_address)
lcd_rows = 2
lcd_cols = 16
lcd = LCD(interface, num_rows=lcd_rows, num_cols=lcd_cols)
lcd.set_cursor_mode(CursorMode.HIDE)
lcd.clear()
lcd.print('Death Clicks')

# general setup vars
kothTimeSecs = 60
modeSelected = 0 #0 for death click, 1 for KOTH
modeButtonClicked = False

# control button vars
timeButtonClicked = False

# vars used across 2+ games
redButtonClicked = False
blueButtonClicked = False
resetButtonClicked = False

# Death clicker logic
numDeaths = 0
deathClickerText = 'Death Count:\n'

# KOTH logic
redActive = False
blueActive = False
redTime = kothTimeSecs
blueTime = kothTimeSecs
blueTimeMins = 0
blueTimeSecs = 0
redTimeMins = 0
redTimeSecs = 0
lastBlueTimeSecs = 0
lastRedTimeSecs = 0
activateTick = 0
curTick = 0
timeLeft = kothTimeSecs
lastTimeLeft = 0
firstLayer = 'Blue        Red\n'

def main():
    global modeSelected
    global modeButtonClicked
    global redActive
    global blueActive
    while True:
        if modeSelected == 0:
            deathClickerLogic()
        elif modeSelected == 1:
            KOTHLogic()
        
        if not modeButton.value:
            if modeButtonClicked or redActive or blueActive or numDeaths > 0:
                continue
            redActive = False
            blueActive = False
            modeButtonClicked = True
            modeSelected = (modeSelected + 1) % 2
            lcd.clear()
            if modeSelected == 0:
                lcd.print('Death Clicks')
            elif modeSelected == 1:
                lcd.print('KOTH')
        else:
            modeButtonClicked = False
        time.sleep(0.1)

# death clicker code
def deathClickerLogic():
    global redLED
    global blueLED
    global numDeaths
    global redButtonClicked
    global blueButtonClicked
    global resetButtonClicked
    if not redButton.value:
        if not redButtonClicked:
            redLED.value = True
            redButtonClicked = True
            numDeaths += 1
            lcd.clear()
            lcd.print(f'{deathClickerText} {numDeaths}')
    else:
        redLED.value = False
        redButtonClicked = False
            
    if not blueButton.value:
        if not blueButtonClicked:
            blueLED.value = True
            blueButtonClicked = True
            numDeaths += 1
            lcd.clear()
            lcd.print(f'{deathClickerText} {numDeaths}')
    else:
        blueLED.value = False
        blueButtonClicked = False
            
    if not resetButton.value:
        if not resetButtonClicked:
            resetButtonClicked = True
            numDeaths = 0
            lcd.clear()
            lcd.print(f'{deathClickerText} {numDeaths}')
    else:
        resetButtonClicked = False

def KOTHLogic():
    global redActive
    global blueActive
    global timeButtonClicked
    global redButtonClicked
    global blueButtonClicked
    global kothTimeSecs
    global secsControlled
    global curTick
    global activateTick
    global blueTime
    global redTime
    global timeLeft
    global resetButtonClicked
    global secsControlled
    global lastTimeLeft
    global lastRedTimeSecs
    global lastBlueTimeSecs
    curTick = time.time()
    if not redActive and not blueActive:
        # pregame stuff
        if not timeUpButton.value:
            if not timeButtonClicked:
                timeButtonClicked = True
                kothTimeSecs += 30
                if kothTimeSecs > 300:
                    kothTimeSecs = 30
                redTime = kothTimeSecs
                blueTime = kothTimeSecs
                redTimeSecs = redTime % 60
                redTimeMins = redTime // 60
                blueTimeSecs = blueTime % 60
                blueTimeMins = blueTime // 60
                timeLeft = kothTimeSecs
                secondLayerText = f'{blueTimeMins}:{'{:02}'.format(blueTimeSecs)}        {redTimeMins}:{'{:02}'.format(redTimeSecs)}'
                lcd.clear()
                lcd.print(f'{firstLayer}{secondLayerText}')
        elif not timeDownButton.value:
            if not timeButtonClicked:
                timeButtonClicked = True
                kothTimeSecs -= 30
                if kothTimeSecs <=0:
                    kothTimeSecs = 300
                redTime = kothTimeSecs
                blueTime = kothTimeSecs
                redTimeSecs = redTime % 60
                redTimeMins = redTime // 60
                blueTimeSecs = blueTime % 60
                blueTimeMins = blueTime // 60
                timeLeft = kothTimeSecs
                secondLayerText = f'{blueTimeMins}:{'{:02}'.format(blueTimeSecs)}        {redTimeMins}:{'{:02}'.format(redTimeSecs)}'
                lcd.clear()
                lcd.print(f'{firstLayer}{secondLayerText}')
        else:
            timeButtonClicked = False
            
            
    curTick = time.time()
    
    
    if redActive:
        secsControlled = curTick - activateTick
        timeLeft = redTime - secsControlled
        timeLeftSecs = timeLeft % 60
        if timeLeftSecs != lastRedTimeSecs:
            redTimeSecs = timeLeft % 60
            redTimeMins = timeLeft // 60
            blueTimeSecs = blueTime % 60
            blueTimeMins = blueTime // 60
            secondLayerText = f'{blueTimeMins}:{'{:02}'.format(blueTimeSecs)}        {redTimeMins}:{'{:02}'.format(redTimeSecs)}'
            lcd.clear()
            lcd.print(f'{firstLayer}{secondLayerText}')
            lastRedTimeSecs = redTimeSecs
        lastTimeLeft = timeLeft
        if timeLeft <= 0:
            # Game over
            redActive = False
            lcd.clear()
            lcd.print('Red Wins!')
            blueLED.value = True
            redLED.value = True
    elif blueActive:
        secsControlled = curTick - activateTick
        timeLeft = blueTime - secsControlled
        timeLeftSecs = timeLeft % 60
        if timeLeftSecs != lastBlueTimeSecs:
            redTimeSecs = redTime % 60
            redTimeMins = redTime // 60
            blueTimeSecs = timeLeft % 60
            blueTimeMins = timeLeft // 60
            secondLayerText = f'{blueTimeMins}:{'{:02}'.format(blueTimeSecs)}        {redTimeMins}:{'{:02}'.format(redTimeSecs)}'
            lcd.clear()
            lcd.print(f'{firstLayer}{secondLayerText}')
            lastBlueTimeSecs = blueTimeSecs
        lastTimeLeft = timeLeft
        if timeLeft <= 0:
            # Game over
            blueActive = False
            lcd.clear()
            lcd.print('Blue Wins!')
            blueLED.value = True
            redLED.value = True
            
    if not redActive and not redButton.value:
        if not redButtonClicked:
            activateTick = curTick
            redButtonClicked = True
            blueActive = False
            redActive = True
            redLED.value = True
            blueLED.value = False
            blueTime = timeLeft
    elif redButton.value:
        redButtonClicked = False
    
    if not blueActive and not blueButton.value:
        if not blueButtonClicked:
            activateTick = curTick
            blueButtonClicked = True
            redActive = False
            blueActive = True
            blueLED.value = True
            redLED.value = False
            redTime = timeLeft
    elif blueButton.value:
        blueButtonClicked = False
        
    if not resetButton.value:
        if not resetButtonClicked:
            resetButtonClicked = True
            redLED.value = False
            blueLED.value = False
            redActive = False
            blueActive = False
            redTime = kothTimeSecs
            blueTime = kothTimeSecs
            blueTimeMins = blueTime // 60
            blueTimeSecs = blueTime % 60
            redTimeMins = redTime // 60
            redTimeSecs = redTime % 60
            lastBlueTimeSecs = 0
            lastRedTimeSecs = 0
            activateTick = 0
            curTick = 0
            timeLeft = kothTimeSecs
            lastTimeLeft = 0
            secondLayerText = f'{blueTimeMins}:{'{:02}'.format(blueTimeSecs)}        {redTimeMins}:{'{:02}'.format(redTimeSecs)}'
            lcd.clear()
            lcd.print(f'{firstLayer}{secondLayerText}')
    else:
        resetButtonClicked = False


    
    
main()
