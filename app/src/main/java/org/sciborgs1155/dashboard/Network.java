package org.sciborgs1155.dashboard;

import edu.wpi.first.cscore.CameraServerJNI;
import edu.wpi.first.math.jni.WPIMathJNI;
import edu.wpi.first.networktables.NetworkTable;
import edu.wpi.first.networktables.NetworkTableInstance;
import edu.wpi.first.networktables.NetworkTablesJNI;
import edu.wpi.first.util.CombinedRuntimeLoader;
import edu.wpi.first.util.WPIUtilJNI;
import java.io.IOException;
import java.util.ArrayList;
import java.util.function.Consumer;
import javafx.application.Platform;
import javafx.scene.image.Image;
import javafx.stage.Stage;
import org.opencv.core.Core;

/** Class for communicating with WPILib's {@link NetworkTablesJNI}. */
public class Network {
  /** The {@link NetworkTableInstance} used to communicate with networktables. */
  private static NetworkTableInstance networkTables;

  /** The {@link NetworkTable} refrencing the 'Dashboard' table on the server. */
  private static NetworkTable dashboardTable;

  // TODO: Named tasks.
  /** An {@link ArrayList list} of tasks to run each tick(stored in {@link Stage} consumers). */
  private static ArrayList<Consumer<Stage>> stageTasks;

  /** The {@link Runnable} to run every tick. */

  /** Used in the {@link Network#connect()} method to refrence specific servers. */
  public enum Server {
    /** Server Name: localhost Port: 5810 */
    SIMULATION,
    /** Server Team: 1155 */
    ROBOT;
  }

  /** Extracts and loads JNI's. */
  public static void load() {
    try {
      NetworkTablesJNI.Helper.setExtractOnStaticLoad(false);
      WPIUtilJNI.Helper.setExtractOnStaticLoad(false);
      WPIMathJNI.Helper.setExtractOnStaticLoad(false);
      CameraServerJNI.Helper.setExtractOnStaticLoad(false);

      CombinedRuntimeLoader.loadLibraries(
          Network.class,
          "wpiutiljni",
          "wpimathjni",
          "ntcorejni",
          Core.NATIVE_LIBRARY_NAME,
          "cscorejni");
    } catch (IOException e) {
      System.err.println("Failed to Load Libraries!");
    }
  }

  /** Starts Network client and tries connecting to the server. */
  public static void connect(Server server) {
    networkTables = NetworkTableInstance.getDefault();

    networkTables.startClient4("SciBoard");
    networkTables.setServer("localhost", 5810);

    if (server == Server.SIMULATION) {
      networkTables.setServer("localhost", 5810);
    }
    if (server == Server.ROBOT) {
      networkTables.setServerTeam(1155, 5810);
      networkTables.startDSClient();
    }

    dashboardTable = networkTables.getTable("Dashboard");
  }

  /** Checks to if the application is connected to NetworkTables. */
  public static boolean isConnected() {
    if (dashboardTable.getEntry("robotTick").getInteger(-1111155555) == -1111155555) {
      return false;
    }
    return true;
  }

  /** Checks to if the application is connected to a real robot or not. */
  public static boolean isRobotReal() {
    return dashboardTable.getEntry("isReal").getBoolean(true);
  }

  /** Returns the 'robotTick' value from the {@link #dashboardTable}. */
  public static int getTick() {
    return (int) dashboardTable.getEntry("robotTick").getInteger(0);
  }

  /** Starts a seperate thread for {@link Network} communications. */
  public static void startNetworkThread(Stage stage) {
    stageTasks = new ArrayList<>();

    //  Icon Switching.
    addStageTask(
        s -> {
          if (Network.isConnected()) {
            Platform.runLater(
                () -> {
                  stage
                      .getIcons()
                      .set(
                          0,
                          new Image(
                              ClassLoader.getSystemResourceAsStream(
                                  "SciborgIcons/sciborgConnected.png")));
                });
          }

          if (!Network.isConnected()) {
            if (!Network.isRobotReal()) {
              Platform.runLater(
                  () -> {
                    stage
                        .getIcons()
                        .set(
                            0,
                            new Image(
                                ClassLoader.getSystemResourceAsStream(
                                    "SciborgIcons/sciborgConnected.png")));
                  });
            }
            if (!Network.isRobotReal()) {
              Platform.runLater(
                  () -> {
                    stage
                        .getIcons()
                        .set(
                            0,
                            new Image(
                                ClassLoader.getSystemResourceAsStream(
                                    "SciborgIcons/sciborgConnectedSim.png")));
                  });
            }
          }

          // Suppressing VSCode warnings.
          s.getWidth();
        });

    final Thread thread =
        new Thread(
            () -> {
              while (true) {
                try {
                  for (Consumer<Stage> task : stageTasks) {
                    task.accept(stage);
                  }

                  Thread.sleep(1000);
                } catch (InterruptedException e) {
                  System.err.println("Network Thread Canceled!");
                }
              }
            },
            "Network Thread");

    Thread.startVirtualThread(thread);
  }

  /** Adds a task that runs periodically every tick. */
  public static void addStageTask(Consumer<Stage> task) {
    stageTasks.add(task);
  }

  /** Removes a task that runs periodically every tick. */
  public static void removeStageTask(Consumer<Stage> task) {
    stageTasks.remove(task);
  }
}
