import ntcore
import time
from settings import *

class Comms:
    def __init__(self):
        
        inst = ntcore.NetworkTableInstance.getDefault()
        table = inst.getTable("Dashboard")

        entryTick = table.getEntry("tick")
        tick = 0

        inst.startClient4("Dashboard")

        if REAL:
            inst.setServerTeam(team=1155, port=5810)
            inst.startDSClient()
        else:
            inst.setServer("localhost")


        while True:
            time.sleep(0.02)
            entryTick.setInteger(tick)
            tick+=1
            print("boop")
