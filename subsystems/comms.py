import time

import ntcore

from settings import *


class Comms:
    '''Handles communication between the program and network tables'''
    def __init__(self) -> None:
        instance = ntcore.NetworkTableInstance.getDefault()
        instance.startClient4(identity="Dashboard")

        self.networkTable = instance.getTable(key="Dashboard")

        if REAL:
            instance.setServerTeam(team=1155, port=5810)
            instance.startDSClient()
        else:
            instance.setServer(server_name="localhost")

        # Entry for the target branch to score on
        self.entryTargetBranch = self.networkTable.getEntry(key="branch")
        self.entryTargetBranch.setString(value="")

        # Entry for the target level to score on
        self.entryTargetLevel = self.networkTable.getEntry(key="level")
        self.entryTargetLevel.setInteger(value=0)

        # Entry for the robot's alliance
        self.entryBlueAlliance = self.networkTable.getEntry(key="blueAlliance")
        self.entryBlueAlliance.setBoolean(value=True)

        # Entry for whether to score processor or not
        self.entryScoringProcessor = self.networkTable.getEntry(key="processor")
        self.entryScoringProcessor.setBoolean(value=False)

        # Entry for the closest branch
        self.entryClosestBranch = self.networkTable.getEntry(key="closestBranch")
        self.entryClosestBranch.setString(value="")

        # Entry for the status of the connection
        self.entryRobotTick = self.networkTable.getEntry(key="robotTick")
        self.entryRobotTick.setInteger(value=0)
        self.previousRobotTick = self.entryRobotTick.getInteger(defaultValue=0)
        self.lastRobotTickDetection = time.time()

        # Tracks update ticks
        self.entryDashboardTick = self.networkTable.getEntry(key="dashboardTick")
        self.entryDashboardTick.setInteger(value=0)
        self.dashboardTick = 0

    def tick(self) -> None:
        '''Meant to be called periodically'''
        self.dashboardTick += 1
        self.entryDashboardTick.setInteger(value=self.dashboardTick)
        
    def setBranch(self, branch:str) -> None:
        self.entryTargetBranch.setString(value=branch)

    def setLevel(self, level:int) -> None:
        self.entryTargetLevel.setInteger(value=level)
    
    def setProcessor(self, boolean:bool) -> None:
        self.entryScoringProcessor.setBoolean(value=boolean)

    def getNearest(self) -> str:
        return self.entryClosestBranch.getString(defaultValue="")
        
    def getIsConnected(self) -> bool:
        fetch = self.entryRobotTick.getInteger(defaultValue=0)
        if fetch != self.previousRobotTick:
            self.lastRobotTickDetection = time.time()
            self.previousRobotTick = fetch
            return True
        elif abs(time.time() - self.lastRobotTickDetection) < 0.2:
            return True
        else: return False
    
    def getBlueAlliance(self) -> bool:
        return self.entryBlueAlliance.getBoolean(defaultValue=True)
    