package org.sciborgs1155.dashboard;

import edu.wpi.first.networktables.NetworkTable;
import edu.wpi.first.networktables.NetworkTableEntry;
import edu.wpi.first.networktables.NetworkTableInstance;
import edu.wpi.first.networktables.NetworkTablesJNI;
import edu.wpi.first.util.CombinedRuntimeLoader;
import java.io.IOException;
import java.util.function.BooleanSupplier;

import edu.wpi.first.cscore.CameraServerJNI;
import edu.wpi.first.math.WPIMathJNI;
import edu.wpi.first.util.WPIUtilJNI;

import static org.sciborgs1155.dashboard.Constants.*;

public class Main {
    public static void main(String[] args) throws IOException {
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
            inst.setServerTeam(1155,5810);
            inst.startDSClient();
        } else {
            inst.setServer("localhost");
        }

        NetworkTable table = inst.getTable("Dashboard");

        NetworkTableEntry entryTick = table.getEntry("tick");
        int tick = 0;
        NetworkTableEntry entryTarget = table.getEntry("target");

        while (true) {
            try {
              Thread.sleep(20);
            } catch (InterruptedException ex) {
                System.out.println("interrupted");
                return;
            }

            for (BooleanSupplier s: dashboard.sides){
                if (s.getAsBoolean()){
                    entryTarget.setString("" + sideNames.get(dashboard.sides.indexOf(s)));
                }
            }
            
            

            
            entryTick.setInteger(tick);
            tick++;
        }
    }
}