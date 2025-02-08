package org.sciborgs1155.dashboard;

import org.junit.jupiter.api.Test;

/** JUnit {@link Test} for the {@link App} class. */
class AppTest {
    /** Calls the {@link App#main()} method on a new thread. */
    @Test void appCanStart() {
        Thread thread = new Thread(new Runnable() {
            @Override
            public void run() {
                App.main(new String[]{});
            }
        });

        thread.start();
    }
}
