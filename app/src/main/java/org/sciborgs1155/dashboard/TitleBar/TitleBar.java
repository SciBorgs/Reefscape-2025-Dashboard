package org.sciborgs1155.dashboard.TitleBar;

import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.layout.Background;
import javafx.scene.layout.BackgroundFill;
import javafx.scene.layout.CornerRadii;
import javafx.scene.layout.HBox;
import javafx.scene.paint.Color;
import javafx.stage.Stage;

/** A simple custom modern Title Bar. */
public class TitleBar extends HBox {
  /** Used for controlling window drag behaviour. */
  private double mouseXOffset = 0;

  /** Used for controlling window drag behaviour. */
  private double mouseYOffset = 0;

  /**
   * Constructs a new {@link TitleBar} that is binded to a {@link Stage}.
   *
   * @param stage The stage binded to this {@link TitleBar}.
   */
  public TitleBar(Stage stage) {
    this.setId("Title Bar");
    this.setBackground(
        new Background(
            new BackgroundFill(Color.BLACK, new CornerRadii(18, 18, 0, 0, false), Insets.EMPTY)));
    this.setSpacing(5);
    this.setFillHeight(false);
    this.setAlignment(Pos.CENTER_RIGHT);

    this.getChildren().add(TitleBarButtons.minimizeButton(stage));
    this.getChildren().add(TitleBarButtons.maximizeButton(stage));
    this.getChildren().add(TitleBarButtons.closeButton(stage));

    this.setOnMousePressed(
        event -> {
          mouseXOffset = event.getSceneX();
          mouseYOffset = event.getSceneY();
        });

    this.setOnMouseDragged(
        event -> {
          stage.setX(event.getScreenX() - mouseXOffset);
          stage.setY(event.getScreenY() - mouseYOffset);
        });
  }
}
