# Reefscape 2025 - 1155 Dashboard

![](</image.png>)

An operator dashboard to control bits of FRC Team 1155's 2025 robot, Sciduck!

Big thanks to [wpilibsuite/StandaloneAppSamples](https://github.com/wpilibsuite/StandaloneAppSamples/tree/main) and [this CD post](https://www.chiefdelphi.com/t/problems-with-importing-wpilib-java/424464) for being starting points for the start of research for the Java version!

Also, thanks to [HenryLi-0/ivo](https://github.com/HenryLi-0/ivo/tree/main) for being the rendering system, which this dashboard uses a modified version of!

## Setup

After you've obtained this code locally, run [`setup.bat`](</setup.bat>) for to quickly install modules! Alternatively, see [`requirements.txt`](</requirements.txt>) for the necessary modules to install.

## Usage

Run [`main.py`](</main.py>)! Visit [`settings.py`](</settings.py>) to modify settings (very important, get familiar with it and double check before running!)

## Structure

The code is centered around [`subsystems/`](</subsystems/>)! The NetworkTables system is in [`subsystems/comms.py`](</subsystems/comms.py>), while the interface is in [`interface.py`](</subsystems/interface.py>). The logic is also located in `interface.py`, under `tick()`. Checkout the [`resources/`](</resources/>) directory to view image files. 

All other files, such as those under [`subsystems/lib/`](</subsystems/lib/>) contain the code needed to run IVO, and changes are not recommended to these.
