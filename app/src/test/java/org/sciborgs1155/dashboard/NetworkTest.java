package org.sciborgs1155.dashboard;

import java.io.IOException;

import org.junit.jupiter.api.Test;
import org.opencv.core.Core;

import edu.wpi.first.cscore.CameraServerJNI;
import edu.wpi.first.math.jni.WPIMathJNI;
import edu.wpi.first.networktables.NetworkTablesJNI;
import edu.wpi.first.util.CombinedRuntimeLoader;
import edu.wpi.first.util.WPIUtilJNI;

public class NetworkTest {
    @Test public void loadTest() {
        NetworkTablesJNI.Helper.setExtractOnStaticLoad(false);
        WPIUtilJNI.Helper.setExtractOnStaticLoad(false);
        WPIMathJNI.Helper.setExtractOnStaticLoad(false);
        CameraServerJNI.Helper.setExtractOnStaticLoad(false);

        try {
            System.out.println(Network.class.getResourceAsStream("/ResourceInformation.json"));
            CombinedRuntimeLoader.loadLibraries(Network.class, "wpiutiljni", "wpimathjni", "ntcorejni",
                Core.NATIVE_LIBRARY_NAME, "cscorejni");
        } catch (IOException e) {
            System.err.println("Failed to Load Libraries!");
        }
    }
}
