package org.sciborgs1155.dashboard;

import java.io.IOException;

import org.opencv.core.Core;

import edu.wpi.first.cscore.CameraServerJNI;
import edu.wpi.first.math.jni.WPIMathJNI;
import edu.wpi.first.networktables.NetworkTable;
import edu.wpi.first.networktables.NetworkTableInstance;
import edu.wpi.first.networktables.NetworkTablesJNI;
import edu.wpi.first.util.CombinedRuntimeLoader;
import edu.wpi.first.util.WPIUtilJNI;

/** Class for communicating with WPILib's {@link NetworkTablesJNI}. */
public class Network {
    /** The {@link NetworkTableInstance} used to communicate with networktables. */
    private static NetworkTableInstance networkTables;

    /** The {@link NetworkTable} refrencing the 'Dashboard' table on the server. */
    private static NetworkTable dashboardTable;

    /**
     * Used in the {@link Network#connect()} method to refrence specific servers.
     */
    public enum Server {
        /** Server Name: localhost Port: 5810 */
        SIMULATION,
        /** Server Team: 1155 */
        ROBOT;
    }

    /** Extracts and loads JNI's, and starts Network client. */
    public static void start() {
        try {
            NetworkTablesJNI.Helper.setExtractOnStaticLoad(false);
            WPIUtilJNI.Helper.setExtractOnStaticLoad(false);
            WPIMathJNI.Helper.setExtractOnStaticLoad(false);
            CameraServerJNI.Helper.setExtractOnStaticLoad(false);

            CombinedRuntimeLoader.loadLibraries(Network.class, "wpiutiljni", "wpimathjni", "ntcorejni",
                    Core.NATIVE_LIBRARY_NAME, "cscorejni");
        } catch (IOException e) {
            System.err.println("Failed to Load Libraries!");
        }
    }

    /** Extracts and loads JNI's, and starts Network client. */
    public static void connect(Server server) {
        try {
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

            if (!isConnected()) {
                throw new IOException();
            }
        } catch (IOException e) {
            System.err.println("Failed to connect to Server!");
        }
    }

    /** Checks to if the application is connected to NetworkTables. */
    public static boolean isConnected() {
        if (dashboardTable.getEntry("robotTick").getInteger(-1111155555) == -1111155555) {
            return false;
        }
        return true;
    }

    /** Returns the 'robotTick' value from the {@link #dashboardTable}. */
    public static int getTick() {
        return (int)dashboardTable.getEntry("robotTick").getInteger(0);
    }
}
