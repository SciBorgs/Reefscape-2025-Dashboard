import time

from settings import COMMS

if COMMS:
    import ntcore

from settings import *


class Comms:
    '''Handles communication between the program and network tables'''
    def __init__(self) -> None:
        # Selected stuff
        self.mode = None
        self.selectedLevel = -1
        self.selectedAlgae = -1
        self.selectedProcessor = False
        if COMMS:
            instance = ntcore.NetworkTableInstance.getDefault()
            instance.startClient4(identity="Dashboard")

            self.dashboardNT = instance.getTable(key="Dashboard")
            self.cameraNT = instance.getTable(key="Robot").getSubTable(key="vision")

            if REAL:
                instance.setServerTeam(team=1155, port=5810)
                instance.startDSClient()
            else:
                instance.setServer(server_name="localhost")

            # Entry for the available branches to score on
            self.entryAvailableBranches = self.dashboardNT.getEntry(key="availableBranches")
            self.entryAvailableBranches.setString(value="ABCDEFGHIJKL")

            # Entry for the target level to score on
            self.entryTargetLevel = self.dashboardNT.getEntry(key="level")
            self.entryTargetLevel.setInteger(value=4)

            # Entry for whether to score processor or not
            self.entryScoringProcessor = self.dashboardNT.getEntry(key="processor")
            self.entryScoringProcessor.setBoolean(value=False)
            
            # Entry for the target algae to obtain
            self.entryTargetAlgae = self.dashboardNT.getEntry(key="algae")
            self.entryTargetAlgae.setInteger(value=-1)

            # Entry for the target elevator height
            self.entryTargetElevator = self.dashboardNT.getEntry(key="targetElevator")
            self.entryTargetElevator.setDouble(value=0)
            
            # Entry for the current elevator height
            self.entryCurrentElevator = self.dashboardNT.getEntry(key="currentElevator")
            self.entryCurrentElevator.getDouble(defaultValue=0)

            # Entry for each of the cameras and their enabled state
            self.entryCameraFL = self.dashboardNT.getEntry(key="cameraFL")
            self.entryCameraFL.getBoolean(defaultValue=True)

            self.entryCameraFR = self.dashboardNT.getEntry(key="cameraFR")
            self.entryCameraFR.getBoolean(defaultValue=True)

            self.entryCameraBL = self.dashboardNT.getEntry(key="cameraBL")
            self.entryCameraBL.getBoolean(defaultValue=True)

            self.entryCameraBR = self.dashboardNT.getEntry(key="cameraBR")
            self.entryCameraBR.getBoolean(defaultValue=True)

            self.entryCameraBM = self.dashboardNT.getEntry(key="cameraBM")
            self.entryCameraBM.getBoolean(defaultValue=True)

            # # Entry for each of our beambreaks
            # self.entryBeambreakSCLCurrent = instance.getTable("Robot/scoraling/scoral/beambreak").getEntry("get")
            # self.entryBeambreakSCLCurrent.getBoolean(defaultValue = True)
            # self.entryBeambreakSCLInvert = self.dashboardNT.getEntry("invertBeambreakSCL")
            # self.entryBeambreakSCLInvert.setBoolean(value=False)

            # self.entryBeambreakHPICurrent = instance.getTable("Robot/scoraling/hopper/beambreak").getEntry("get")
            # self.entryBeambreakHPICurrent.getBoolean(defaultValue = True)
            # self.entryBeambreakHPIInvert = self.dashboardNT.getEntry("invertBeambreakHPI")
            # self.entryBeambreakHPIInvert.setBoolean(value=False)

            # Entry for the status of the connection
            self.entryRobotTick = self.dashboardNT.getEntry(key="robotTick")
            self.entryRobotTick.setInteger(value=0)
            self.previousRobotTick = self.entryRobotTick.getInteger(defaultValue=0)
            self.lastRobotTickDetection = time.time()

            # Entry for new requests to the robot
            self.entryRequest = self.dashboardNT.getEntry(key="request")
            self.entryRequest.setString(value="")

            # Entry for the robot's alliance
            self.entryBlueAlliance = self.dashboardNT.getEntry(key="blueAlliance")
            self.entryBlueAlliance.getBoolean(defaultValue="")

            # Entry for the current match
            self.entryMatch = self.dashboardNT.getEntry(key="match")

            # Entry for the current match time
            self.entryMatchTime = self.dashboardNT.getEntry(key="matchTime")

            # Tracks update ticks
            self.entryDashboardTick = self.dashboardNT.getEntry(key="dashboardTick")
            self.entryDashboardTick.setInteger(value=0)
            self.dashboardTick = 0

    def tick(self) -> None:
        '''Meant to be called periodically'''
        if COMMS:
            self.dashboardTick += 1
            self.entryDashboardTick.setInteger(value=self.dashboardTick)

    def getCurrentElevator(self) -> float:
        if COMMS: return self.entryCurrentElevator.getDouble(defaultValue=1.0)
        else: return 1.0

    def setCameraFL(self, state:bool) -> bool:
        if COMMS: self.entryCameraFL.setBoolean(value=state)

    def setCameraFR(self, state:bool) -> bool:
        if COMMS: self.entryCameraFR.setBoolean(value=state)

    def setCameraBL(self, state:bool) -> bool:
        if COMMS: self.entryCameraBL.setBoolean(value=state)

    def setCameraBR(self, state:bool) -> bool:
        if COMMS: self.entryCameraBR.setBoolean(value=state)

    def setCameraBM(self, state:bool) -> bool:
        if COMMS: self.entryCameraBM.setBoolean(value=state)
    
    def getCameraEstimates(self, id) -> float:
        if COMMS: return self.cameraNT.getEntry("estimates present " + str(id)).getBoolean(defaultValue=False)
        else: return False
    
    # def getBeambreakSCL(self) -> bool:
    #     if COMMS: return self.entryBeambreakSCLCurrent.getBoolean(defaultValue=False)
    #     else: return False

    # def getBeambreakHPI(self) -> bool:
    #     if COMMS: return self.entryBeambreakHPICurrent.getBoolean(defaultValue=False)
    #     else: return False
    
    # def setBeambreakSCLInvert(self, invert) -> bool:
    #     if COMMS: self.entryBeambreakSCLInvert.setBoolean(value=invert)

    # def setBeambreakHPIInvert(self, invert) -> bool:
    #     if COMMS: self.entryBeambreakHPIInvert.setBoolean(value=invert)

    def getMatch(self) -> str:  
        if COMMS: return self.entryMatch.getString(defaultValue="@ None / M0")
        else: return "@ None / M0"
    
    def getMatchTime(self) -> float:
        if COMMS: return self.entryMatchTime.getDouble(defaultValue=0.0)
        else: return 0.0
        
    def getRequest(self) -> str:
        if COMMS: return self.entryRequest.getString(defaultValue="")
        else: return False

    def getRobotTick(self) -> int:
        if COMMS: return self.entryRobotTick.getInteger(defaultValue=0)
        else: return 0

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
    
    def setAvailableBranches(self, branch:str) -> None:
        self.entryAvailableBranches.setString(branch)

    def setSelectedLevel(self, level:int) -> None:
        self.entryTargetLevel.setInteger(level)
    
    def setProcessor(self) -> None:
        self.selectedProcessor = not(self.selectedProcessor)
        self.selectedAlgae = -1
        self.selectedElevator = 0
        self.mode = "processor"
    
    def setSelectedAlgae(self, algae:int) -> None:
        self.selectedAlgae = algae
        self.selectedElevator = 0
        self.mode = "algae"

    def setElevator(self, elevator:float) -> None:
        self.selectedAlgae = -1
        self.selectedElevator = elevator
        self.mode = "elevator"

    def transmitRequest(self, request:str) -> None:
        self.entryRequest.setString(value="")
        robotTick = self.getRobotTick()
        start = time.time()
        while abs(self.getRobotTick()-robotTick) < 10:
            time.sleep(0.05)
            if abs(time.time() - start) > 0.2:
                break
        self.entryRequest.setString(value=request)

    def transmit(self) -> None:
        if COMMS:
            if self.mode == "processor":
                self.entryScoringProcessor.setBoolean(value=True)
                self.entryTargetAlgae.setInteger(value=-1)
                self.entryTargetElevator.setDouble(value=0)
                self.transmitRequest("processor")
                self.lastNewRequest = time.time()
                self.resetDashboard()
            elif self.mode == "algae":
                self.entryScoringProcessor.setBoolean(value=False)
                self.entryTargetAlgae.setInteger(value=self.selectedAlgae)
                self.entryTargetElevator.setDouble(value=0)
                self.transmitRequest("algae")
                self.lastNewRequest = time.time()
                self.resetDashboard()
            elif self.mode == "elevator":
                self.entryScoringProcessor.setBoolean(value=False)
                self.entryTargetAlgae.setInteger(value=-1)
                self.entryTargetElevator.setDouble(value=self.selectedElevator)
                self.transmitRequest("elevator")
                self.lastNewRequest = time.time()
                self.resetDashboard()
            elif self.mode == "reset":
                self.entryScoringProcessor.setBoolean(value=False)
                self.entryTargetAlgae.setInteger(value=-1)
                self.entryRequest.setString(value="")
                self.lastNewRequest = time.time()
                self.resetDashboard()
            else: pass
    
    def resetDashboard(self) -> None:
        self.selectedAlgae = -1
        self.selectedProcessor = False
        self.mode = None