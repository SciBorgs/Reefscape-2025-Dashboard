# Reefscape 2025 - 1155 Dashboard
An operator dashboard to control bits of FRC Team 1155's 2025 robot.

Big thanks to [this repository](https://github.com/wpilibsuite/StandaloneAppSamples/tree/main) and [this CD post](https://www.chiefdelphi.com/t/problems-with-importing-wpilib-java/424464) for being starting points for researching!

## Structure
The code is centered around [Main.java](src/main/java/org/sciborgs1155/dashboard/Main.java).

- `Main.java` loads the libraries, creates the Dashboard GUI, and runs the NetworkTable data.
- `Dashboard.java` consists of the Dashboard GUI.
- `Constants.java` consists of constants, which should be updated as necessary. `REAL` should be set

It *appears* that you **should** build with `./gradlew build` before running. Additionally, do **NOT** update the project version!

If this doesn't work, try a random combination of:
- `./gradlew build`
- `./gradlew clean build`
- `Restart Java Language Server`
- `Reopen VSCode`
