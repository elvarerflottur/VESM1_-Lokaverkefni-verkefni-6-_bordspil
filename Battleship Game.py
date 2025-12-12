from machine import Pin, ADC, PWM 
import neopixel
import time

#variables
pos = 0
Name = 0
choose = False
choose_pos = ""
hit = False
num = 1
rotate = "up"
i = 0
pase = 1



#player 1
player_choose_listi_1 = []
player_hit_listi_1 = []
player_miss_listi_1 = []
player_storage_listi_1 = []

#player 2
player_choose_listi_2 = []
player_hit_listi_2 = []
player_miss_listi_2 = []
player_storage_listi_2 = []

#pins
np_pin = Pin(3 , Pin.OUT)
max_np = 100
np = neopixel.NeoPixel(np_pin, max_np)	# 8 x RGB Leds
red_btn = Pin(10, Pin.IN, Pin.PULL_UP)
red_led = Pin(18, Pin.OUT)
speaker = PWM(Pin(15))
speaker.duty(0)

#lines
def stuff():
    global pase
    global pos
    
    # 1. Calculate the 'line' number (1 through 9)
    if pos >= 0 and pos < 90:
        line = (pos // 10) + 1
    else:
        # For pos >= 90 or pos < 0
        line = 0 

    # We only proceed if 'line' is valid (1 through 9)
    if 1 <= line <= 9:
        
        # 2. Calculate the step count within the current line (0 to 9)
        line_start_pos = (line - 1) * 10
        line_step = pos - line_start_pos
        
        # 3. Calculate 'pase' based on Odd/Even lines and the specific sequences:
        
        if line % 2 == 1:
            # Formula for ODD lines (1, 3, 5, 7, 9): Counts DOWN by 2s: 19, 17, 15, ..., 1
            # Starts at 19 because line_step * 2 is 0 when line_step is 0
            pase = 19 - (line_step * 2)
        
        else: # line % 2 == 0
            # Formula for EVEN lines (2, 4, 6, 8): Counts UP by 2s: 1, 3, 5, ..., 19
            # Starts at 1 because line_step * 2 is 0, so pase = 1 + 0
            pase = 1 + (line_step * 2)

    else:
        # Case where line is 0 (outside the 0-90 range)
        pase = 0 
        line = 0
        
    # 4. Print the final results
    print(f"Line: {line}")
    print(f"Pase: {pase}")

#rgb
white = [100, 100, 100]
red = [100, 0, 0]
green = [0, 100, 0]
blue = [0, 0, 100]
off = [0, 0, 0]

#joystick pins
x_as = ADC(Pin(14), atten=ADC.ATTN_11DB)
y_as = ADC(Pin(13), atten=ADC.ATTN_11DB)
takki = Pin(12, Pin.IN, Pin.PULL_UP)

# deadzone
radius = 500
x = 2000
x_high = x + radius
x_low = x - radius
y = 1950
y_high = y + radius
y_low = y - radius

#ships
ships = {
    #"1": 5,
    #"2": 4,
    #"3": 3,
    "4": 3,
    "5": 2
    }

#players
player1 = {
    "choose": player_choose_listi_1,
    "hit": player_hit_listi_1,
    "miss": player_miss_listi_1,
    "storage": player_storage_listi_1
    }

player2 = {
    "choose": player_choose_listi_2,
    "hit": player_hit_listi_2,
    "miss": player_miss_listi_2,
    "storage": player_storage_listi_2
    }

players = {
    "1": player1,
    "2": player2
    }


def sounds(power):
    print(f"sounds {power}")
    if power == True:
        speaker.freq(440)
        speaker.duty(512)
    elif power == False:
        speaker.duty(0)
  

#turn system
def turn_system_func():
    global player
    global op
    if num == 1:
        player = players["1"]
        op = players["2"]
    elif num == 2:
        player = players["2"]
        op = players["1"]

def num_func():
    global num
    if num == 1:
        num = 2
    elif num == 2:
        num = 1


#if pos out of range
def position_func():
    global pos
    global choose_pos
    print("\033[31m position func started\033[0m")
    if pos >= max_np:
        pos -= max_np
        position_func()
    if choose_pos >= max_np:
        choose_pos -= max_np
        position_func()
    if pos < 0:
        pos += max_np
        position_func()
    if choose_pos < 0:
        choose_pos += max_np
        position_func()
        
    print(f"\033[34m 	position is: (pos: {pos}), (choose_pos: {choose_pos})\033[0m")
    print("\033[32m position func ended\033[0m")
    

#blinker
def blink_func(nr, color):
    print("\033[31m blink func started\033[0m")
    global pos
    global choose_pos
    global ship
    global i
    np.fill(off)
    np.write()
    time.sleep_ms(250)
    for a in range(nr):
        if choose == True:
            sounds(True)
            for i in range(ship):
                rotate_func()
                choose_pos = pos + i
                position_func()
                np[choose_pos] = color
            print(f"\033[34m 	(ship) - blink nr: {a+1}\033[0m")
            np.write()
            time.sleep_ms(250)
            sounds(False)
            np.fill(off)
            np.write()
            time.sleep_ms(250)
        if hit == True:
            print(f"\033[34m(normal) - blink nr: {a+1}\033[0m")
            sounds(True)
            np.fill(off)
            np[pos] = color      # Use the index 'i' to set the single pixel
            np.write()
            time.sleep_ms(250)
            sounds(False)
            np.fill(off)
            np.write()
            time.sleep_ms(250)
            
    print("\033[32m blink func ended\033[0m")

#rotation
def rotate_func():
    global i
    global rotate
    print("rotate func started")
    if rotate == "up":
        i = 1 * i
    elif rotate == "right":
        i = 10 * i
    elif rotate == "down":
        i = -1 * i
    elif rotate == "left":
        i = -10 * i
    print("rotate func ended")

#choose system
def choose_func():
    print("\033[31m choose func started\033[0m")
    global choose
    global ship
    global pos
    global ship_range
    global rotate
    global i
    choose = True
    for Name, player in players.items():
        print(f"player: {Name}")
        print(player)
        turn_system_func()
        for name, ship in sorted(ships.items(), key=lambda x: x[1], reverse=True):
            pos = 0
            print(f"\033[34m 	ship nr: {name}\033[0m")
            rotate = "up"
            def ship_range():
                global choose_pos
                global i
                np.fill(off)
                for i in range(ship):
                    rotate_func()
                    choose_pos = pos + i
                    position_func()
                    np[choose_pos] = green
                np.write()
                sounds(False)
                    
            ship_range()
            
            while_func()
            
            for i in range(ship):
                global choose_pos
                rotate_func()
                choose_pos = pos + i
                position_func()
                player["choose"].append(choose_pos)
                print(f"\033[34m 	list: {player}\033[0m")
            
            time.sleep_ms(500)
            np.fill(off)
            np.write()
        
        num_func()
        
        
    choose = False
    print("\033[32m choose func ended\033[0m")

#hit system
def hit_func():
    print("\033[31m hit func started\033[0m")
    global a
    global pos
    global hit
    global num
    global player
    global op
    nr = 0
    
            
    turn_system_func()
    
    # makes sure you don't click the same spots you have chosen
    for storage in player["storage"]:
        if storage == pos:
            sounds(True)
            np[pos] = red
            np.write()
            print("can't do that")
            time.sleep_ms(250)
            sounds(False)
            return while_func()
    
    # range
    for i in op["choose"]:
        nr += 1
        
        # checks if the position is the same as in storage
        if i == pos:
            print("\033[33m hit\033[0m")
            nr -= 1
            player["hit"].append(pos)
            player["storage"].append(pos)
            blink_func(2, red)
            np.fill(off)
            np[0] = blue
            np.write()
            
        # win
    if len(player["hit"]) == len(op["choose"]):
        print(f"player {player}: wins")
        print(f"op {op}: lost")
        np.fill(off)
        np.write()
        for i in range(8):
            sounds(True)
            np[i] = green
            np.write()
            time.sleep_ms(250)
            sounds(False)
        np.fill(off)
        np.write()
        for i in range(2):
            time.sleep_ms(250)
            sounds(True)
            for i in range(8):
                np[i] = green
            np.write()
            time.sleep_ms(250)
            sounds(False)
            np.fill(off)
            np.write()
        hit = False
                
    elif nr == len(op["choose"]):
        print("\033[33m miss\033[0m")
        blink_func(2, white)
        player["miss"].append(pos)
        player["storage"].append(pos)
            
    num_func()
            
    if hit == True:
        np.fill(off)
        led_func()
        pos = 0
        np[pos] = blue
        np.write()
        while_func()
        time.sleep_ms(250)
    
    print("\033[32m hit func ended\033[0m")
    
#turn leds on
def led_func():
    print("\033[31m led func started\033[0m")
    turn_system_func()
    
    for i in player["miss"]:
        np[i] = white
    for i in player["hit"]:
        np[i] = red
        
    print("\033[32m choose func ended\033[0m")


#movement loop
def while_func():
    print("\033[31m while func started\033[0m")
    global pos
    global xvalue, yvalue, btnValue
    global choose
    run = True
    pos = 0
    if hit == True:
        np.fill(off)
        led_func()
        np[pos] = blue
        np.write()
        
    while run:
        x_Value = x_as.read()
        y_Value = y_as.read()
        btnValue = takki.value()
            
        if x_Value < x_high  and x_Value > x_low:
            xvalue = 1
            direction = "center"
        elif x_Value > x_high:
            xvalue = 0
            direction = "right"
        elif x_Value < x_low:
            xvalue = 2
            direction = "left"
            
        if y_Value < y_high  and y_Value > y_low:
            yvalue = 1
            direction = "center"
        elif y_Value > y_high:
            yvalue = 2
            direction = "down"
        elif y_Value < y_low:
            yvalue = 0
            direction = "up"

        #print(f"X: {x_as.read()}, Y: {y_as.read()}, Takki: {takki.value()}, direction: {direction}")
        
        if red_btn.value() == 0:
            print("green button pressed")
            global rotate
            sounds(True)
            red_led.value(1)
            if rotate == "up":
                rotate = "right"
            elif rotate == "right":
                rotate = "down"
            elif rotate =="down":
                rotate = "left"
            elif rotate == "left":
                rotate = "up"
            ship_range()
            print(rotate)
            time.sleep_ms(250)
            red_led.value(0)
            time.sleep_ms(250)
            
             
        if btnValue == 0:
            global villa
            global player
            global i
            global choose_pos
            villa = False
            print("\033[33m button down\033[0m")
            if choose == True:
                for i in range(ship):
                    rotate_func()
                    choose_pos = pos + i
                    position_func()
                    for b in player["choose"]:
                        if choose_pos == b:
                            print("\033[32m villa\033[0m")
                            villa = True
                        
                if villa == False:
                    blink_func(2, green)
                    print("\033[34m 	position chosen\033[0m")
                    run = False
                else:
                    print("\033[32m wrong position chosen\033[0m")
                    blink_func(2, red)
                    pos = 0
                    ship_range()
                        
                        
                time.sleep_ms(250)
            elif hit == True:
                hit_func()
                run = False

# Right
        if xvalue == 0:
            print("\033[33m right\033[0m")
            if choose == True:
                sounds(True)
                pos += 1
                ship_range()
                time.sleep_ms(250)
            elif hit == True:
                sounds(True)
                pos += 1
                np.fill(off)
                position_func()
                led_func()
                np[pos] = blue
                np.write()
                sounds(False)
                time.sleep_ms(250)

# left
        elif xvalue == 2:
            print("\033[33m left\033[0m")
            if choose == True:
                sounds(True)
                pos -= 1
                ship_range()
                time.sleep_ms(250)
            elif hit == True:
                sounds(True)
                pos -= 1
                np.fill(off)
                position_func()
                led_func()
                np[pos] = blue
                np.write()
                sounds(False)
                time.sleep_ms(250)

# Up
        if yvalue == 0:
            print("\033[33m up\033[0m")
            if choose == True:
                sounds(True)
                stuff()
                pos += pase
                ship_range()
                time.sleep_ms(250)
            elif hit == True:
                sounds(True)
                stuff()
                pos += pase
                np.fill(off)
                position_func()
                led_func()
                np[pos] = blue
                np.write()
                sounds(False)
                time.sleep_ms(250)

# Down 
        elif yvalue == 2:
            print("\033[33m down\033[0m")
            if choose == True:
                sounds(True)
                stuff()
                pos -= pase
                ship_range()
                time.sleep_ms(250)
            elif hit == True:
                sounds(True)
                stuff()
                pos -= pase
                np.fill(off)
                position_func()
                led_func()
                np[pos] = blue
                np.write()
                sounds(False)
                time.sleep_ms(250)
                
                
    print("\033[32m while func ended\033[0m")


choose_func()
hit = True
while_func()
print("ended")
