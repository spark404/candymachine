#!/usr/bin/python

import logging
import random
import time
import threading
import pygame
import subprocess
import sys
from subprocess import PIPE

import RPi.GPIO as GPIO

class Ports():
    OPTO_1         = 17 # OUT
    RELAY_1        = 18 # OUT
    SMOKE_MACHINE  = 18 # OUT
    KAHUNA_SWITCH  = 22 # IN
    RELAY_2        = 23 # OUT
    KAHUNA_SLIDER  = 23 # OUT
    BUBBLE_MACHINE = 25 # OUT
    OPTO_2         = 27 # OUT
    FRONT_LIGHTS   = 27 # OUT
    
    def __init__(self):
        # Initialize GPIO
        GPIO.setmode(GPIO.BCM)
        
        # Setup IO direction
        GPIO.setup(Ports.BUBBLE_MACHINE, GPIO.OUT)
        GPIO.setup(Ports.RELAY_1, GPIO.OUT)
        GPIO.setup(Ports.RELAY_2, GPIO.OUT)
        GPIO.setup(Ports.OPTO_1, GPIO.OUT)
        GPIO.setup(Ports.OPTO_2, GPIO.OUT)
  	GPIO.setup(Ports.KAHUNA_SWITCH, GPIO.IN)
    
    def activate(self, port):
        GPIO.output(port, GPIO.HIGH)

    def deactivate(self, port):
        GPIO.output(port, GPIO.LOW)

    def ishigh(self, port):
        return GPIO.input(port)

class FakePorts():
    def __init__(self):
        logging.debug("Init ports")
    
    def __del__(self):
        logging.debug("Cleanup ports")
    
    def activate(self, port):
        logging.debug("Setting port %s HIGH" % port)

    def deactivate(self, port):
        logging.debug("Setting port %s LOW" % port)

# abstract class for actions
class Action():
    def __init__(self):
        pass

def perform(self):
        pass

class BubbleMachine(Action):
    def __init__(self, ports, stop_event, soundfx):
        self.ports = ports
        self.stop_event = stop_event
        self.soundfx = soundfx

    def perform(self):
        logging.info("BubbleMachine started")
       
        self.soundfx.fx_start(SoundFxGenerator.BUBBLES) 
        self.ports.activate(Ports.BUBBLE_MACHINE)
        stop_event.wait(50)
        self.ports.deactivate(Ports.BUBBLE_MACHINE)
        self.soundfx.fx_stop(SoundFxGenerator.BUBBLES) 

        logging.info("BubbleMachine stopped")

class SmokeMachine(Action):
    def __init__(self, ports, stop_event, soundfx):
        self.ports = ports
        self.stop_event = stop_event
        self.soundfx = soundfx
    
    def perform(self):
        logging.info("SmokeMachine started")
        
        self.soundfx.fx_start(SoundFxGenerator.SIREN) 
        self.ports.activate(Ports.RELAY_1)
        stop_event.wait(30)
        self.ports.deactivate(Ports.RELAY_1)
        self.soundfx.fx_stop(SoundFxGenerator.SIREN) 
        
        logging.info("SmokeMachine stopped")

class Bleeping(Action):
    def __init__(self, ports, stop_event, soundfx):
        self.ports = ports
        self.stop_event = stop_event
        self.soundfx = soundfx
    
    def perform(self):
        logging.info("Bleep started")
        
        self.soundfx.fx_start(SoundFxGenerator.BLEEP) 
        stop_event.wait(10)
        self.soundfx.fx_stop(SoundFxGenerator.BLEEP) 
        stop_event.wait(2)
        self.soundfx.fx_start(SoundFxGenerator.BLEEP) 
        stop_event.wait(10)
        self.soundfx.fx_stop(SoundFxGenerator.BLEEP) 
        stop_event.wait(2)
        self.soundfx.fx_start(SoundFxGenerator.BLEEP) 
        stop_event.wait(10)
        self.soundfx.fx_stop(SoundFxGenerator.BLEEP) 
        
        logging.info("Bleep stopped")

class Kahuna(Action):
    def __init__(self, ports, stop_event, soundfx):
        self.ports = ports;
        self.stop_event = stop_event
        self.soundfx = soundfx

    def perform(self):
        logging.info("Kahuna started")
        self.ports.activate(Ports.FRONT_LIGHTS)
        self.soundfx.fx_play(SoundFxGenerator.HORN) 
        stop_event.wait(10)

        self.ports.activate(Ports.SMOKE_MACHINE)
        self.soundfx.fx_start(SoundFxGenerator.MACHINE) 
        stop_event.wait(5)
 
        self.soundfx.fx_start(SoundFxGenerator.BUBBLES) 
        self.ports.activate(Ports.BUBBLE_MACHINE)
        stop_event.wait(7)
        self.ports.activate(Ports.OPTO_1)
        stop_event.wait(13)

        self.ports.deactivate(Ports.BUBBLE_MACHINE)
        self.soundfx.fx_stop(SoundFxGenerator.BUBBLES) 
        self.soundfx.fx_play(SoundFxGenerator.HYDRAULIC) 
        self.ports.deactivate(Ports.FRONT_LIGHTS)
  
        stop_event.wait(3)
        
        self.ports.activate(Ports.KAHUNA_SLIDER)
        stop_event.wait(1)
        self.ports.deactivate(Ports.KAHUNA_SLIDER)
        stop_event.wait(3)
        self.ports.activate(Ports.KAHUNA_SLIDER)
        stop_event.wait(1)
        self.ports.deactivate(Ports.KAHUNA_SLIDER)

        self.ports.deactivate(Ports.SMOKE_MACHINE)
        self.soundfx.fx_stop(SoundFxGenerator.MACHINE) 
        logging.info("Kahuna stopped")

class SoundFxGenerator():
    BUBBLES = 1
    SIREN = 2
    BLEEP = 3
    HYDRAULIC = 4
    MACHINE = 5
    HORN = 6
    
    def __init__(self):
        # set audio output to the jack
        process = subprocess.Popen(["amixer", "cset", "numid=3", "1"] , stdin=PIPE, stdout=PIPE, stderr=PIPE)
        process = subprocess.Popen(["amixer", "sset", "PCM", "100"] , stdin=PIPE, stdout=PIPE, stderr=PIPE)
        process.wait()
        pygame.mixer.init()
        self.effect_siren = pygame.mixer.Sound("soundeffects/police_s.wav")
        self.effect_bubbles = pygame.mixer.Sound("soundeffects/Bubbling-SoundBible.com-1684132696.wav")
        self.effect_bleep = pygame.mixer.Sound("soundeffects/bleep_01.wav")
        self.effect_hydraulic = pygame.mixer.Sound("soundeffects/12906__swelk__hydraul1.wav") # 8.2 seconds
        self.effect_machine = pygame.mixer.Sound("soundeffects/30315__lg__industrial23.wav") # 1.3 seconds
        self.effect_horn = pygame.mixer.Sound("soundeffects/horn.wav") # 14 sec

    def cleanup(self):
        pygame.mixer.quit()

    def fx_start(self, effect):
        effect = self.__get_effect_by_id(effect)
        effect.play(loops=-1)

    def fx_stop(self, effect):
        effect = self.__get_effect_by_id(effect)
        effect.stop()
     
    def fx_play(self, effect):
        effect = self.__get_effect_by_id(effect)
        effect.play(loops=0)

    def __get_effect_by_id(self, id):
        if id == self.BUBBLES:
            return self.effect_bubbles
        elif id == self.SIREN:
            return self.effect_siren
        elif id == self.BLEEP:
            return self.effect_bleep
        elif id == self.HYDRAULIC:
            return self.effect_hydraulic
        elif id == self.MACHINE:
            return self.effect_machine
        elif id == self.HORN:
            return self.effect_horn


if __name__ == "__main__":
    logging.basicConfig(filename='/var/log/snoepjesmachine.log',
                        level=logging.DEBUG,
                        format='%(asctime)s %(message)s')
    
    gpioPorts = Ports()
    soundfx = SoundFxGenerator()
    stop_event = threading.Event()

    random.seed()
    
    randomActions = []
    randomActions.append(BubbleMachine(gpioPorts, stop_event, soundfx))
    randomActions.append(SmokeMachine(gpioPorts, stop_event, soundfx))
    randomActions.append(Bleeping(gpioPorts, stop_event, soundfx))

    kahuna = Kahuna(gpioPorts, stop_event, soundfx)
    
    lastAction = 0
    randomDeltaTime = 120 # Seconds
    kahunaFlag = False
    kahunaStarted = False
    actionThread = None

    try:
        while True:
            currentTime = time.time()

    	    if not gpioPorts.ishigh(Ports.KAHUNA_SWITCH) and kahunaFlag == False:
                logging.info("Kahuna event starting")
                kahunaFlag = True
                if not actionThread == None and not kahunaStarted:
                    stop_event.set()
                    logging.info("Event set, waiting for action to die")
                    actionThread.join()
                    logging.info("Action died, clearing event")
                    stop_event.clear()
                if not kahunaStarted:
                    actionThread = threading.Thread(target=kahuna.perform)
                    actionThread.start()
                    kahunaStarted = True
            elif gpioPorts.ishigh(Ports.KAHUNA_SWITCH) and kahunaFlag == True:
                if not actionThread == None and actionThread.isAlive():
                    logging.info("Kahuna still running, not clearing the flag")
                else:
                    logging.info("Kahuna event cleared")
                    gpioPorts.deactivate(Ports.OPTO_1)
                    kahunaStarted = False
                    kahunaFlag = False
            elif ((currentTime - lastAction) > randomDeltaTime) and not kahunaFlag:
                lastAction = time.time()
                logging.info("Time for a random action")
                action = random.randint(0, len(randomActions)-1)
                actionThread = threading.Thread(target=randomActions[action].perform)
                actionThread.start()
            
            logging.debug("regular poll, kahunaFlag = %s", kahunaFlag  )
            if not actionThread == None:
                actionThread.join(1)
                if not actionThread.isAlive():
                    actionThread = None
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Interrupted, cleanup and exit")
        if not actionThread == None and actionThread.isAlive():
            stop_event.set()
            actionThread.join()
        gpioPorts = None
        GPIO.cleanup()
        soundfx.cleanup()
        sys.exit(1)
