from communication.actuator import Actuator
import time


actuator = Actuator()

while True:
    t1 = time.time()
    #actuator.send_wheelVelocity_message(1,10301,10,10,10,10)
    #actuator.send_globalVelocity_message(2,10302,5,10,15)
    actuator.send_localVelocity_message(3,10302,5,10,15)
    t2 = time.time()

    if( (t2-t1) < 1/300 ):
        time.sleep(1/300 - (t2-t1))