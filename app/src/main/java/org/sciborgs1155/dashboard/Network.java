package org.sciborgs1155.dashboard;

import java.io.IOException;

import org.opencv.core.Core;

import edu.wpi.first.cscore.CameraServerJNI;
import edu.wpi.first.math.jni.WPIMathJNI;
import edu.wpi.first.networktables.NetworkTableInstance;
import edu.wpi.first.networktables.NetworkTablesJNI;
import edu.wpi.first.util.CombinedRuntimeLoader;
import edu.wpi.first.util.WPIUtilJNI;

public class Network {
    /** The {@link NetworkTableInstance} used to communicate with networktables. */
    private static NetworkTableInstance networkTables;

    /** Extracts and loads JNI's, and starts Network client */
    public static void start() {
        NetworkTablesJNI.Helper.setExtractOnStaticLoad(false);
        WPIUtilJNI.Helper.setExtractOnStaticLoad(false);
        WPIMathJNI.Helper.setExtractOnStaticLoad(false);
        CameraServerJNI.Helper.setExtractOnStaticLoad(false);

        try {
            CombinedRuntimeLoader.loadLibraries(Network.class, "wpiutiljni", "wpimathjni", "ntcorejni",
                    Core.NATIVE_LIBRARY_NAME, "cscorejni");
            
            networkTables = NetworkTableInstance.getDefault();

            networkTables.startClient4("SciBoard");
            networkTables.setServer("localhost", 5810);

            if (networkTables.getTable("Dashboard").getEntry("robotTick").getInteger(-1111155555) == -1111155555) {
                throw new IOException("Failed to Connect!");
            }
        } catch (IOException e) {
            System.err.println("Failed to Load Libraries!");
        }
    }
}
