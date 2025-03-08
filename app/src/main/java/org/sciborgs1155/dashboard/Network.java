package org.sciborgs1155.dashboard;

import edu.wpi.first.cameraserver.CameraServer;
import edu.wpi.first.cscore.CameraServerJNI;
import edu.wpi.first.cscore.UsbCamera;
import edu.wpi.first.math.jni.WPIMathJNI;
import edu.wpi.first.networktables.NetworkTable;
import edu.wpi.first.networktables.NetworkTableInstance;
import edu.wpi.first.networktables.NetworkTablesJNI;
import edu.wpi.first.util.CombinedRuntimeLoader;
import edu.wpi.first.util.WPIUtilJNI;
import java.io.IOException;
import java.time.Duration;
import java.util.ArrayList;
import java.util.function.Consumer;
import java.util.function.Supplier;
import javafx.application.Platform;
import javafx.scene.image.Image;
import javafx.stage.Stage;
import org.opencv.core.Core;
import org.sciborgs1155.dashboard.ReefMenu.BranchButton;
import org.sciborgs1155.dashboard.ReefMenu.BranchButton.Branch;

/** Class for communicating with WPILib's {@link NetworkTablesJNI}. */
public class Network {
  /** The {@link NetworkTableInstance} used to communicate with networktables. */
  private static NetworkTableInstance networkTables;

  /** The {@link NetworkTable} refrencing the 'Dashboard' table on the server. */
  private static NetworkTable dashboardTable;

  /** An {@link ArrayList} of tasks to run each tick(stored in {@link Stage} consumers). */
  private static ArrayList<Consumer<Stage>> stageTasks;

  /** The {@link Duration} inbetween network table updates. */
  private static final Duration taskUpdateDelay = Duration.ofMillis(1000);

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

    // Get the UsbCamera from CameraServer
    UsbCamera camera = CameraServer.startAutomaticCapture();
    // Set the resolution
    camera.setResolution(640, 480);
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

  /**
   * Starts a seperate thread for {@link Network} communications.
   *
   * @param stage The stage that will be passed into the {@link #stageTasks}.
   */
  public static void startNetworkThread(Stage stage) {
    stageTasks = new ArrayList<>();

    addIconSwitching(stage);

    final Thread taskThread =
        new Thread(
            () -> {
              while (true) {
                try {
                  for (Consumer<Stage> task : stageTasks) {
                    task.accept(stage);
                  }

                  Thread.sleep(taskUpdateDelay);
                } catch (InterruptedException e) {
                  System.err.println("Network Task Thread Canceled!");
                }
              }
            },
            "Network Task Thread");

    Thread.startVirtualThread(taskThread);
  }

  /**
   * Turns on icon switching depending on the connection status.
   *
   * @param stage The stage to control the icon switching of.
   */
  public static void addIconSwitching(Stage stage) {
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

          // This supresses VSCode unused warnings.
          s.getWidth();
        });
  }

  /**
   * Adds a task that runs periodically every tick.
   *
   * @param task The task to run.
   */
  public static void addStageTask(Consumer<Stage> task) {
    stageTasks.add(task);
  }

  /**
   * Adds a task that runs periodically every tick whenever the listener returns true.
   *
   * @param task The task to run.
   * @param listener Determines whether the task will run or not.
   */
  public static void addStageTask(Consumer<Stage> task, Supplier<Boolean> listener) {
    stageTasks.add(
        stage -> {
          if (listener.get()) {
            task.accept(stage);
          }
        });
  }

  /**
   * Removes a task that runs periodically every tick.
   *
   * @param task The task to remove.
   */
  public static void removeStageTask(Consumer<Stage> task) {
    stageTasks.remove(task);
  }

  /**
   * Activates a specified Branch in the {@link #dashboardTable Dashboard Network Table}.
   * 
   * 
   * @param branch The branch to activate.
   */
  public static void activateBranch(Branch branch) {
    dashboardTable.getEntry("Branch").setString(BranchButton.branchToString.get(branch));
  }

  /**
   * Deactivates the branch field in the {@link #dashboardTable Dashboard Network Table}.
   */
  public static void deactivateBranch() {
    dashboardTable.getEntry("Branch").setString("");
  }
}
