package org.sciborgs1155.dashboard;

import static org.sciborgs1155.dashboard.Constants.*;

import edu.wpi.first.cscore.CameraServerJNI;
import edu.wpi.first.math.WPIMathJNI;
import edu.wpi.first.networktables.NetworkTable;
import edu.wpi.first.networktables.NetworkTableEntry;
import edu.wpi.first.networktables.NetworkTableInstance;
import edu.wpi.first.networktables.NetworkTablesJNI;
import edu.wpi.first.util.CombinedRuntimeLoader;
import edu.wpi.first.util.WPIUtilJNI;
import java.io.IOException;
import java.util.function.BooleanSupplier;

/**
 * An operator dashboard that utilizes NetworkTables to send information to the robot, which can
 * then be used by the robot as Triggers.
 */
public class Main {
  public static void main(String[] args) throws IOException {
    // setup libraries
    NetworkTablesJNI.Helper.setExtractOnStaticLoad(false);
    WPIUtilJNI.Helper.setExtractOnStaticLoad(false);
    WPIMathJNI.Helper.setExtractOnStaticLoad(false);
    CameraServerJNI.Helper.setExtractOnStaticLoad(false);
    CombinedRuntimeLoader.loadLibraries(Main.class, "wpiutiljni", "wpimathjni", "ntcorejni");
    new Main().run();
  }

  public void run() {
    // start gui
    final Dashboard dashboard = new Dashboard();

    // connect
    NetworkTableInstance inst = NetworkTableInstance.getDefault();
    inst.startClient4("Dashboard");
    if (REAL) {
      inst.setServerTeam(1155, 5810);
      inst.startDSClient();
    } else {
      inst.setServer("localhost");
    }

    // setup network table and entries
    NetworkTable table = inst.getTable("Dashboard");

    NetworkTableEntry entryTick = table.getEntry("tick");
    int tick = 0;
    entryTick.setInteger(tick);

    NetworkTableEntry entryTargetBranch = table.getEntry("branch");
    String selectedBranch = "";
    entryTargetBranch.setString(selectedBranch);
    NetworkTableEntry entryTargetLevel = table.getEntry("level");
    int selectedLevel = 0;
    entryTargetLevel.setInteger(selectedLevel);
    NetworkTableEntry entryProcessor = table.getEntry("processor");
    Boolean selectedProcessor = false;
    entryProcessor.setBoolean(selectedProcessor);

    // loop
    while (true) {
      try {
        Thread.sleep(20);
      } catch (InterruptedException ex) {
        System.out.println("interrupted");
        return;
      }
      // check branches
      for (BooleanSupplier s : dashboard.branches) {
        if (s.getAsBoolean()) {
          selectedBranch = branchNames.get(dashboard.branches.indexOf(s));
        }
      }
      // check levels
      for (BooleanSupplier s : dashboard.levels) {
        if (s.getAsBoolean()) {
          selectedLevel = dashboard.levels.indexOf(s) + 1;
        }
      }
      if (dashboard.processor.getAsBoolean()) {
        selectedProcessor = true;
      }
      // check go button
      if (dashboard.GO.getAsBoolean()) {
        if (selectedBranch != "" && selectedLevel != 0) {
          entryTargetBranch.setString(selectedBranch);
          entryTargetLevel.setInteger(selectedLevel);
        }
      }
      // check reset button
      if (dashboard.RESET) {
        entryTargetBranch.setString("");
        entryTargetLevel.setInteger(0);
      }

      // send tick information
      entryTick.setInteger(tick);
      tick++;
    }
  }
}
