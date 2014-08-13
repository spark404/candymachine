#!/usr/bin/python

import logging
import random
import time
import threading

#import RPi.GPIO as GPIO

class Ports():
    RELAY_1 = 18
    RELAY_2 = 23
    BUBBLE_MACHINE = 25
    
    def __init__(self):
        # Initialize GPIO
        GPIO.setmode(GPIO.BCM)
        
        # Setup IO direction
        GPIO.setup(Ports.BUBBLE_MACHINE, GPIO.OUT)
        GPIO.setup(Ports.RELAY_1, GPIO.OUT)
        GPIO.setup(Ports.RELAY_2, GPIO.OUT)
    
    def __del__(self):
        GPIO.cleanup()

    def activate(self, port):
        GPIO.output(port, GPIO.HIGH)

    def deactivate(self, port):
        GPIO.output(port, GPIO.LOW)

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
    def __init__(self, ports, stop_event):
        self.ports = ports
        self.stop_event = stop_event

    def perform(self):
        logging.info("BubbleMachine started")
        
        self.ports.activate(Ports.BUBBLE_MACHINE)
        time.sleep(5)
        self.ports.deactivate(Ports.BUBBLE_MACHINE)

        logging.info("BubbleMachine stopped")

class SmokeMachine(Action):
    def __init__(self, ports, stop_event):
        self.ports = ports
        self.stop_event = stop_event
    
    def perform(self):
        logging.info("SmokeMachine started")
        
        self.ports.activate(Ports.RELAY_1)
        stop_event.wait(10)
        self.ports.deactivate(Ports.RELAY_1)
        
        logging.info("SmokeMachine stopped")

class Kahuna(Action):
    def __init__(self, ports):
        self.ports = ports;

    def perform(self):
        logging.info("Kahuna started")
        stop_event.wait(10)
        logging.info("Kahuna stopped")

if __name__ == "__main__":
    #logging.basicConfig(filename='/var/log/snoepjesmachine.log',
    #                    level=logging.DEBUG,
    #                    format='%(asctime)s %(message)s')
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(message)s')
    
    gpioPorts = FakePorts()
    random.seed()
    
    stop_event = threading.Event()

    randomActions = []
    randomActions.append(BubbleMachine(gpioPorts, stop_event))
    randomActions.append(SmokeMachine(gpioPorts, stop_event))
    
    lastAction = 0
    randomDeltaTime = 30 # Seconds
    kahunaFlag = False

    while True:
        currentTime = time.time()
        logging.debug("ping")
        if ((currentTime - lastAction) > randomDeltaTime):
            lastAction = time.time()
            logging.info("Time for a random action")
            action = random.randint(0, len(randomActions)-1)
            actionThread = threading.Thread(target=randomActions[action].perform)
            actionThread.start()
        else:
            if not actionThread == None:
                actionThread.join(1)
                if not actionThread.isAlive():
                    actionThread = None
            else:
                time.sleep(1)

