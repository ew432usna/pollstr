import network
import time
import urequests
import ubinascii
import badger2040
from badger2040 import WIDTH, HEIGHT
import json

badger = badger2040.Badger2040()

badger.set_update_speed(badger2040.UPDATE_FAST)

badger.set_pen(15) #white
badger.clear() # set the background white

badger.set_pen(0) #black
#try to join WRCE
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('WRCE', None)

mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
print(mac)


while not wlan.isconnected() and wlan.status() >=0:
    print("waiting....")
    time.sleep(1)
    
print(wlan.ifconfig()) # IP, Subnet Mask, Default Gateway, DNS Server

idd = 0
opt = ""
resp= 0
    
def vote(idd, opt):
    print("button pressed!")
    response = urequests.post(f"https://pollstr.usna.wattsworth.net/poll/{idd}.json", json = {'option': opt})
    print("vote submitted!")
    if response.status_code==200:
        success = True
    else:
        success = False
    response.close()
    return success

def show_message(msg):
    # clear the display and show a message on the screen
    badger.set_pen(15) #white
    badger.clear() # set the background white
    badger.set_pen(0)
    badger.text(msg, 10, 20)
    badger.update()
    

show_message("Pollstr booting...")

while True:
    
    r = urequests.get('https://pollstr.usna.wattsworth.net/poll.json')
    
    poll = r.content
    string = poll.decode()
    print(string)
    parsed_data = json.loads(string)
    print(parsed_data)
    
    print(poll)
    
    
    
    idd = parsed_data['id']
    question = parsed_data['question']
    opt1 = "A)" + parsed_data['options'][0]
    opt2 = "B)" + parsed_data['options'][1]
    opt3 = "C)" + parsed_data['options'][2]
    
    print(idd)
    print(question)
    print(opt1)
    print(opt2)
    print(opt3)
    badger.set_pen(15) #white
    badger.clear() # set the background white
    badger.set_pen(0)
    badger.text(question, 10, 20)
    badger.text(opt1, 10, 40)
    badger.text(opt2, 10, 60)
    badger.text(opt3, 10, 80)
    badger.update()

    
    
    selected_option = None # whether the vote succeeded
    while True:
        #wait for button press
        if badger.pressed(badger2040.BUTTON_A):            
            selected_option='A'
            break
        elif badger.pressed(badger2040.BUTTON_B):        
            selected_option='B'
            break
        elif badger.pressed(badger2040.BUTTON_C):
            selected_option='C'
            break
        time.sleep(0.5)
     
    show_message("Submitting your vote...")
    
    success=vote(idd,selected_option)
    
    if success:
        show_message("Thanks for voting!")
    else:
        show_message("Something went wrong :(")
    
    time.sleep(2)


    
  
