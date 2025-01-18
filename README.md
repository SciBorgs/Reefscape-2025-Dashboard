# Reefscape 2025 - 1155 Dashboard
A (currently experimental) dashboard to control bits of FRC Team 1155's 2025 robot.

## Structure
The code is centered around [Main.java](src/main/java/org/sciborgs1155/dashboard/Main.java).

- `Main.java` loads the libraries, creates the Dashboard GUI, and runs the NetworkTable data.
- `Dashboard.java` consists of the Dashboard GUI.
- `Contants.java` consists of constants, which should be updated as necessary.

It *appears* that you **MUST** build with `./gradlew build` before running. Additionally, do **NOT** update the project version!