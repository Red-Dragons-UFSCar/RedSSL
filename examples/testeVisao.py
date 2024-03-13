from communication.vision import Vision
import time

visao = Vision()

while True:
    t1 = time.time()

    visao.update()
    frame = visao.get_last_frame()

    try:
        print("Robots: ", frame["robots_blue"])
    except:
        pass

    t2 = time.time()

    if( (t2-t1) < 1/300 ):
        time.sleep(1/300 - (t2-t1))
