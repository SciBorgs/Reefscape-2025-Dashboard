import ntcore
import time
if __name__ == "__main__":
    inst = ntcore.NetworkTableInstance.getDefault()
    table = inst.getTable("Dashboard")

    entryTick = table.getEntry("tick")
    tick = 0

    inst.startClient4("example client")
    inst.setServer("localhost")
    # inst.setServerTeam(team=1155)
    # inst.startDSClient()
    while True:
        time.sleep(0.02)
        entryTick.setInteger(tick)
        tick+=1

