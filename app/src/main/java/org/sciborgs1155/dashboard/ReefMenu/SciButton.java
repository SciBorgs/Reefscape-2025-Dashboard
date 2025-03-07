package org.sciborgs1155.dashboard.ReefMenu;

import edu.wpi.first.networktables.NetworkTable;
import javafx.scene.Cursor;
import javafx.scene.control.Button;
import javafx.scene.image.Image;
import javafx.scene.layout.Background;
import javafx.scene.layout.BackgroundImage;
import javafx.scene.layout.BackgroundPosition;
import javafx.scene.layout.BackgroundRepeat;
import javafx.scene.layout.BackgroundSize;
import javafx.scene.shape.Circle;
import javafx.stage.Stage;
import javafx.util.Duration;
import org.sciborgs1155.dashboard.Styles;

/**
 * Button used to send the {@link ReefMenu} commands to {@link NetworkTable NetworkTables}. Directly
 * in the center of all the branches. 115`5.
 */
public class SciButton extends Button {
  /**
   * The Constructor.
   *
   * @param stage Passed into the {@link #bind(Stage)} method, which keeps it at the center.
   */
  public SciButton(Stage stage, ReefMenu reefMenu) {
    this.setShape(new Circle(1));
    this.setCursor(Cursor.HAND);

    this.setBackground(
        new Background(
            new BackgroundImage(
                new Image(ClassLoader.getSystemResourceAsStream("SciborgIcons/sciborg.png")),
                BackgroundRepeat.NO_REPEAT,
                BackgroundRepeat.NO_REPEAT,
                BackgroundPosition.CENTER,
                new BackgroundSize(
                    this.getPrefWidth(), this.getPrefHeight(), false, false, true, true))));

    Styles.applyHoverScaleAnimation(1, 1.2, Duration.millis(100), this);
    Styles.applyHoverOpacityAnimation(0.7, 1, Duration.millis(100), this);
    Styles.applyClickScaleAnimation(1.2, 1.1, Duration.millis(100), this);

    this.bind(stage, reefMenu);
  }

  /**
   * The Constructor. You should probably call {@link #bind(Stage)} as well.
   *
   * <p>{@code NOTE: PROBABLY WON'T DISPLAY WITHOUT USING BINDING IT TO A STAGE FIRST}
   */
  public SciButton() {
    this.setShape(new Circle(1));
    this.setCursor(Cursor.HAND);

    this.setBackground(
        new Background(
            new BackgroundImage(
                new Image(ClassLoader.getSystemResourceAsStream("SciborgIcons/sciborg.png")),
                BackgroundRepeat.NO_REPEAT,
                BackgroundRepeat.NO_REPEAT,
                BackgroundPosition.CENTER,
                new BackgroundSize(
                    this.getPrefWidth(), this.getPrefHeight(), false, false, true, true))));

    Styles.applyHoverScaleAnimation(1, 1.2, Duration.millis(100), this);
    Styles.applyHoverOpacityAnimation(0.7, 1, Duration.millis(100), this);
    Styles.applyClickScaleAnimation(1.2, 1.1, Duration.millis(100), this);
  }

  /**
   * Binds properties of button to stage(width/height and x/y).
   *
   * @param stage The stage to bind the button properties to.
   */
  public void bind(Stage stage, ReefMenu reefMenu) {
    this.clipProperty().bind(reefMenu.clipProperty());
    this.prefWidthProperty().bind(reefMenu.heightProperty().divide(3));
    this.prefHeightProperty().bind(reefMenu.heightProperty().divide(3));

    this.layoutXProperty()
        .bind(reefMenu.prefWidthProperty().divide(2).subtract(this.prefWidthProperty().divide(2)).add(reefMenu.layoutXProperty()));
    this.layoutYProperty()
        .bind(reefMenu.prefHeightProperty().divide(2).subtract(this.prefHeightProperty().divide(2)).add(reefMenu.layoutYProperty()));
    this.layoutXProperty().bind(reefMenu.prefWidthProperty().divide(2));
    this.layoutYProperty().bind(reefMenu.prefHeightProperty().divide(2));
  }
}
