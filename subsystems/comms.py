import time

from settings import COMMS

if COMMS:
    import ntcore

from settings import *


class Comms:
    '''Handles communication between the program and network tables'''
    def __init__(self) -> None:
        if COMMS:
            instance = ntcore.NetworkTableInstance.getDefault()
            instance.startClient4(identity="Dashboard")

            self.networkTable = instance.getTable(key="Dashboard")

            if REAL:
                instance.setServerTeam(team=1155, port=5810)
                instance.startDSClient()
            else:
                instance.setServer(server_name="localhost")

            # Selected stuff
            self.mode = None
            self.selectedBranch = " "
            self.selectedLevel = -1
            self.selectedAlgae = -1
            self.selectedProcessor = False

            # Entry for the target branch to score on
            self.entryTargetBranch = self.networkTable.getEntry(key="branch")
            self.entryTargetBranch.setString(value="")

            # Entry for the target level to score on
            self.entryTargetLevel = self.networkTable.getEntry(key="level")
            self.entryTargetLevel.setInteger(value=0)

            # Entry for whether to score processor or not
            self.entryScoringProcessor = self.networkTable.getEntry(key="processor")
            self.entryScoringProcessor.setBoolean(value=False)
            
            # Entry for whether to score processor or not
            self.entryTargetAlgae = self.networkTable.getEntry(key="algae")
            self.entryTargetAlgae.setInteger(value=-1)

            # Entry for the status of the connection
            self.entryRobotTick = self.networkTable.getEntry(key="robotTick")
            self.entryRobotTick.setInteger(value=0)
            self.previousRobotTick = self.entryRobotTick.getInteger(defaultValue=0)
            self.lastRobotTickDetection = time.time()

            # Entry for the robot's alliance
            self.entryBlueAlliance = self.networkTable.getEntry(key="blueAlliance")
            self.entryBlueAlliance.setBoolean(value=True)


            '''add match things here'''

            # Tracks update ticks
            self.entryDashboardTick = self.networkTable.getEntry(key="dashboardTick")
            self.entryDashboardTick.setInteger(value=0)
            self.dashboardTick = 0

            # Entry for the closest branch
            self.entryClosestBranch = self.networkTable.getEntry(key="closestBranch")
            self.entryClosestBranch.setString(value="")

    def tick(self) -> None:
        '''Meant to be called periodically'''
        if COMMS:
            self.dashboardTick += 1
            self.entryDashboardTick.setInteger(value=self.dashboardTick)
        


    def getNearest(self) -> str:
        if COMMS: return self.entryClosestBranch.getString(defaultValue="")
        else: return ""
        
    def getIsConnected(self) -> bool:
        if COMMS:
            fetch = self.entryRobotTick.getInteger(defaultValue=0)
            if fetch != self.previousRobotTick:
                self.lastRobotTickDetection = time.time()
                self.previousRobotTick = fetch
                return True
            elif abs(time.time() - self.lastRobotTickDetection) < 0.25:
                return True
            else: return False
        else: return True
    
    def getBlueAlliance(self) -> bool:
        if COMMS: return self.entryBlueAlliance.getBoolean(defaultValue=True)
        else: return False
    
    def setSelectedBranch(self, branch:str) -> None:
        if self.selectedBranch != branch:
            self.selectedBranch = branch
        else:
            self.selectedBranch = " "
        self.selectedAlgae = -1
        self.selectedProcessor = False
        self.mode = "reef"

    def setSelectedLevel(self, level:int) -> None:
        if self.selectedLevel != level:
            self.selectedLevel = level
        else:
            self.selectedLevel = -1
        self.selectedAlgae = -1
        self.selectedProcessor = False
        self.mode = "reef"
    
    def setProcessor(self) -> None:
        self.selectedProcessor = not(self.selectedProcessor)
        self.selectedBranch = " "
        self.selectedLevel = 0
        self.selectedAlgae = -1
        self.mode = "processor"
    
    def setSelectedAlgae(self, algae:int) -> None:
        self.selectedBranch = " "
        self.selectedLevel = 0
        self.selectedAlgae = algae
        self.mode = "algae"

    def transmit(self) -> None:
        if COMMS:
            if self.mode == "reef":
                if self.selectedBranch != " " and self.selectedLevel != -1:
                    self.entryTargetBranch.setString(value=self.selectedBranch)
                    self.entryTargetLevel.setInteger(value=self.selectedLevel)
                    self.entryScoringProcessor.setBoolean(value=False)
                    self.entryTargetAlgae.setInteger(value=-1)
                    self.resetDashboard()
            elif self.mode == "processor":
                self.entryTargetBranch.setString(value=" ")
                self.entryTargetLevel.setInteger(value=-1)
                self.entryScoringProcessor.setBoolean(value=True)
                self.entryTargetAlgae.setInteger(value=-1)
                self.resetDashboard()
            elif self.mode == "algae":
                self.entryTargetBranch.setString(value=" ")
                self.entryTargetLevel.setInteger(value=-1)
                self.entryScoringProcessor.setBoolean(value=False)
                self.entryTargetAlgae.setInteger(value=self.selectedAlgae)
                self.resetDashboard()
            elif self.mode == "reset":
                self.entryTargetBranch.setString(value=" ")
                self.entryTargetLevel.setInteger(value=-1)
                self.entryScoringProcessor.setBoolean(value=False)
                self.entryTargetAlgae.setInteger(value=-1)
                self.resetDashboard()
                
            else: pass
    
    def resetDashboard(self) -> None:
        self.selectedBranch = " "
        self.selectedLevel = -1
        self.selectedAlgae = -1
        self.selectedProcessor = False
        self.mode = None