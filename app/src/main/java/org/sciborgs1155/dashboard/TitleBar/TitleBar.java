package org.sciborgs1155.dashboard.TitleBar;

import javafx.beans.property.Property;
import javafx.beans.value.ObservableValue;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.layout.Background;
import javafx.scene.layout.BackgroundFill;
import javafx.scene.layout.CornerRadii;
import javafx.scene.layout.HBox;
import javafx.scene.layout.Pane;
import javafx.scene.paint.Color;
import javafx.stage.Stage;

/**
 * Collection of 3 {@link TitleBarButton TitleBarButtons} ({@link #minimizeButton minimize}, {@link
 * #maximizeButton maximize}, and {@link #closeButton close}) at the top of the window.
 */
public class TitleBar extends HBox {
  /** Used for controlling window drag behaviour. */
  private double mouseXOffset = 0;

  /** Used for controlling window drag behaviour. */
  private double mouseYOffset = 0;

  /** Used to minimize the window. */
  private final TitleBarButton minimizeButton = TitleBarButton.minimizeButton();

  /** Used to maximize the window. */
  private final TitleBarButton maximizeButton = TitleBarButton.maximizeButton();

  /** Used to close the window. */
  private final TitleBarButton closeButton = TitleBarButton.closeButton();

  /**
   * Constructs a new {@link TitleBar} that is {@link #bind(Stage, Pane) binded} to a {@link Stage}.
   *
   * @param id The CSS id.
   * @param stage The stage {@link #bind(Stage, Pane) binded} to this {@link TitleBar}.
   */
  public TitleBar(String id, Stage stage, Pane root) {
    this.setId(id);
    this.setBackground(
        new Background(
            new BackgroundFill(Color.BLACK, new CornerRadii(18, 18, 0, 0, false), Insets.EMPTY)));
    this.setSpacing(5);
    this.setFillHeight(false);
    this.setAlignment(Pos.CENTER_RIGHT);

    this.getChildren().add(minimizeButton);
    this.getChildren().add(maximizeButton);
    this.getChildren().add(closeButton);

    this.bind(stage, root);
  }

  /**
   * Constructs a new {@link TitleBar}.
   *
   * <p>{@code NOTE: PROBABLY WON'T WORK WITHOUT CALLING BIND.}
   *
   * <p>{@link #bind(Stage, Pane) The Bind Method.}
   *
   * @param id The CSS id.
   */
  public TitleBar(String id) {
    this.setId(id);
    this.setBackground(
        new Background(
            new BackgroundFill(Color.BLACK, new CornerRadii(18, 18, 0, 0, false), Insets.EMPTY)));
    this.setSpacing(5);
    this.setFillHeight(false);
    this.setAlignment(Pos.CENTER_RIGHT);

    this.getChildren().add(minimizeButton);
    this.getChildren().add(maximizeButton);
    this.getChildren().add(closeButton);
  }

  /**
   * {@link Property#bind(ObservableValue) Binds} properties of the {@link TitleBar} to the {@link
   * Stage} and {@link Pane scene root}.
   *
   * @param stage The {@link Stage} that is {@link TitleBarButton#bind(Stage, TitleBar) binded} to
   *     the {@link TitleBarButton TitleBarButtons}.
   * @param root The {@link Pane} {@link Property#bind(javafx.beans.value.ObservableValue) binded}
   *     to the {@link #widthProperty() width} and {@link #backgroundProperty() background}
   *     properties of this {@link TitleBar}.
   */
  public void bind(Stage stage, Pane root) {
    this.prefWidthProperty().bind(root.widthProperty());
    this.minHeightProperty().bind(this.prefWidthProperty().divide(20));
    this.backgroundProperty().bind(root.backgroundProperty());
    
    this.setViewOrder(-1);

    this.minimizeButton.bind(stage, this);
    this.maximizeButton.bind(stage, this);
    this.closeButton.bind(stage, this);

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
