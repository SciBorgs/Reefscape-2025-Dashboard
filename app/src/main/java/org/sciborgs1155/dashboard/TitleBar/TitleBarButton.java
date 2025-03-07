package org.sciborgs1155.dashboard.TitleBar;

import java.util.function.Consumer;
import javafx.beans.property.Property;
import javafx.beans.value.ChangeListener;
import javafx.beans.value.ObservableValue;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.control.Button;
import javafx.scene.effect.BlendMode;
import javafx.scene.image.Image;
import javafx.scene.layout.Background;
import javafx.scene.layout.BackgroundFill;
import javafx.scene.layout.BackgroundImage;
import javafx.scene.layout.BackgroundPosition;
import javafx.scene.layout.BackgroundRepeat;
import javafx.scene.layout.BackgroundSize;
import javafx.scene.layout.CornerRadii;
import javafx.scene.layout.Pane;
import javafx.scene.layout.StackPane;
import javafx.scene.paint.Color;
import javafx.scene.shape.Rectangle;
import javafx.stage.Stage;
import javafx.util.Duration;
import org.sciborgs1155.dashboard.Styles;

// TODO: Make corner actually clickable on maximize.
/**
 * Factory for {@link #minimizeButton() minimize}, {@link #maximizeButton() maximize}, and {@link
 * #closeButton() close} buttons for use in the {@link TitleBar}.
 */
public class TitleBarButton extends StackPane {
  /** Is used for hover-effect animations. */
  private final Rectangle backgroundLayer = new Rectangle();

  /** Is what the user interacts with. */
  private final Button buttonLayer = new Button();

  /** The color of the background(when it is hovered over, transparent otherwise). */
  private final Color backgroundColor;

  /** The amount that the button is scaled when it's clicked relative to original size. */
  private final double clickScaleFactor;

  /** The amount that the button is brightened up when it's hovered over relative to original. */
  private final double hoverBrightnessFactor;

  /** The opacity of the button when it isn't being hovered over relative to original. */
  private final double hoverOpacityFactor;

  /** The icon displayed on the button. */
  private final Image icon;

  /** Customs insets(useful for corner buttons that need rounded corners). */
  private final CornerRadii corners;

  /** What the button does on-click. */
  private final Consumer<Stage> action;

  /** CSS id. Probably useless but whatever. */
  private final String id;

  /**
   * A {@link TitleBarButton} that appears at the corner of a {@link TitleBar}. {@link Stage#close()
   * Closes} the {@link Stage stage} that it is binded to.
   *
   * <p>{@code NOTE: PROBABLY WON'T WORK WITHOUT CALLING BIND.}
   *
   * <p>{@link #bind(Stage, TitleBar) The Bind Method.}
   *
   * @param stage The stage to {@link Stage#close() close} on click.
   * @param titleBar The {@link TitleBar} binded to the {@link #prefWidthProperty() width} and
   *     {@link #prefHeightProperty() height} properties of this {@link TitleBarButton}.
   * @return The {@link TitleBarButton}.
   */
  public static TitleBarButton closeButton(Stage stage, TitleBar titleBar) {
    return new TitleBarButton(
        "Close Button",
        stag -> stag.close(), // Yes, Typo is intentional.
        stage,
        titleBar,
        new Image(ClassLoader.getSystemResourceAsStream("TitleBarResources/closeButton.png")),
        Color.RED,
        new CornerRadii(0, 0, 0, 0, false),
        0.9,
        3.0,
        0.7);
  }

  /**
   * A {@link TitleBarButton} that appears at the corner of a {@link TitleBar}. {@link Stage#close()
   * Closes} the {@link Stage stage} that it is binded to.
   *
   * <p>{@code NOTE: PROBABLY WON'T WORK WITHOUT CALLING BIND.}
   *
   * <p>{@link #bind(Stage, TitleBar) The Bind Method.}
   *
   * @return The {@link TitleBarButton}.
   */
  public static TitleBarButton closeButton() {
    return new TitleBarButton(
        "Close Button",
        stag -> stag.close(), // Yes, Typo is intentional.
        new Image(ClassLoader.getSystemResourceAsStream("TitleBarResources/closeButton.png")),
        Color.RED,
        CornerRadii.EMPTY,
        0.9,
        3.0,
        0.7);
  }

  /**
   * A {@link TitleBarButton} that appears 2nd from the corner of a {@link TitleBar}. {@link
   * Stage#setMaximized(boolean) Maximizes} the {@link Stage stage} that it is binded to.
   *
   * <p>{@code NOTE: PROBABLY WON'T WORK WITHOUT CALLING BIND.}
   *
   * <p>{@link #bind(Stage, TitleBar) The Bind Method.}
   *
   * @param stage The stage to {@link Stage#setMaximized(boolean) maximize} on click.
   * @param titleBar The {@link TitleBar} binded to the {@link #prefWidthProperty() width} and
   *     {@link #prefHeightProperty() height} properties of this {@link TitleBarButton}.
   * @return The {@link TitleBarButton}.
   */
  public static TitleBarButton maximizeButton(Stage stage, TitleBar titleBar) {
    Consumer<Stage> action = // Yes, Typo is intentional.
        stag -> {
          if (stag.isMaximized()) {
            stag.setMaximized(false);
          } else {
            stag.setMaximized(true);
          }
        };

    return new TitleBarButton(
        "Maximize Button",
        action,
        stage,
        titleBar,
        new Image(ClassLoader.getSystemResourceAsStream("TitleBarResources/maximizeButton.png")),
        Color.BLACK,
        CornerRadii.EMPTY,
        0.9,
        3.0,
        0.7);
  }

  /**
   * A {@link TitleBarButton} that appears 2nd from the corner of a {@link TitleBar}. {@link
   * Stage#setMaximized(boolean) Maximizes} the {@link Stage stage} that it is binded to.
   *
   * <p>{@code NOTE: PROBABLY WON'T WORK WITHOUT CALLING BIND.}
   *
   * <p>{@link #bind(Stage, TitleBar) The Bind Method.}
   *
   * @return The {@link TitleBarButton}.
   */
  public static TitleBarButton maximizeButton() {
    Consumer<Stage> action = // Yes, Typo is intentional.
        stag -> {
          if (stag.isMaximized()) {
            stag.setMaximized(false);
          } else {
            stag.setMaximized(true);
          }
        };

    return new TitleBarButton(
        "Maximize Button",
        action,
        new Image(ClassLoader.getSystemResourceAsStream("TitleBarResources/maximizeButton.png")),
        Color.BLACK,
        CornerRadii.EMPTY,
        0.9,
        3.0,
        0.7);
  }

  /**
   * A {@link TitleBarButton} that appears 3rd from the corner of a {@link TitleBar}. {@link
   * Stage#setIconified(boolean) Minimizes} the {@link Stage stage} that it is binded to.
   *
   * <p>{@code NOTE: PROBABLY WON'T WORK WITHOUT CALLING BIND.}
   *
   * <p>{@link #bind(Stage, TitleBar) The Bind Method.}
   *
   * @param stage The stage to {@link Stage#setIconified(boolean) minimize} on click.
   * @param titleBar The {@link TitleBar} binded to the {@link #prefWidthProperty() width} and
   *     {@link #prefHeightProperty() height} properties of this {@link TitleBarButton}.
   * @return The {@link TitleBarButton}.
   */
  public static TitleBarButton minimizeButton(Stage stage, TitleBar titleBar) {
    return new TitleBarButton(
        "Minimize Button",
        stag -> stag.setIconified(true), // Yes, Typo is intentional
        stage,
        titleBar,
        new Image(ClassLoader.getSystemResourceAsStream("TitleBarResources/minimizeButton.png")),
        Color.BLACK,
        CornerRadii.EMPTY,
        0.9,
        3.0,
        0.7);
  }

  /**
   * A {@link TitleBarButton} that appears 3rd from the corner of a {@link TitleBar}. {@link
   * Stage#setIconified(boolean) Minimizes} the {@link Stage stage} that it is binded to.
   *
   * <p>{@code NOTE: PROBABLY WON'T WORK WITHOUT CALLING BIND.}
   *
   * <p>{@link #bind(Stage, TitleBar) The Bind Method.}
   *
   * @return The {@link TitleBarButton}.
   */
  public static TitleBarButton minimizeButton() {
    return new TitleBarButton(
        "Minimize Button",
        stag -> stag.setIconified(true), // Yes, Typo is intentional
        new Image(ClassLoader.getSystemResourceAsStream("TitleBarResources/minimizeButton.png")),
        Color.BLACK,
        CornerRadii.EMPTY,
        0.9,
        3.0,
        0.7);
  }

  /**
   * The Constructor.
   *
   * @param id The CSS id.
   * @param action The action to do on the click of this button.
   * @param stage The stage to act upon on the click of this button.
   * @param titleBar The TitleBar that this button is a part of.
   * @param icon The icon of the button.
   * @param size The size of the button(pixels).
   * @param backgroundColor The color of the background.
   * @param clickScaleFactor The factor by which the size of the button is scaled on-click.
   * @param hoverBrightnessFactor The factor by which the brightness of the background is scaled
   *     on-hover.
   */
  private TitleBarButton(
      String id,
      Consumer<Stage> action,
      Stage stage,
      TitleBar titleBar,
      Image icon,
      Color backgroundColor,
      CornerRadii corners,
      double clickScaleFactor,
      double hoverBrightnessFactor,
      double hoverOpacityFactor) {
    this.id = id;
    this.corners = corners;
    this.icon = icon;
    this.action = action;
    this.clickScaleFactor = clickScaleFactor;
    this.hoverBrightnessFactor = hoverBrightnessFactor;
    this.hoverOpacityFactor = hoverOpacityFactor;
    this.backgroundColor = backgroundColor;

    this.bind(stage, titleBar);
  }

  /**
   * The Constructor.
   *
   * <p>{@code NOTE: PROBABLY WON'T WORK WITHOUT CALLING BIND.}
   *
   * <p>{@link #bind(Stage) The Bind Method.}
   *
   * @param id The CSS id.
   * @param action The action to do on the click of this button.
   * @param icon The icon of the button.
   * @param size The size of the button(pixels).
   * @param backgroundColor The color of the background.
   * @param clickScaleFactor The factor by which the size of the button is scaled on-click.
   * @param hoverBrightnessFactor The factor by which the brightness of the background is scaled
   *     on-hover.
   */
  private TitleBarButton(
      String id,
      Consumer<Stage> action,
      Image icon,
      Color backgroundColor,
      CornerRadii corners,
      double clickScaleFactor,
      double hoverBrightnessFactor,
      double hoverOpacityFactor) {
    this.id = id;
    this.corners = corners;
    this.icon = icon;
    this.action = action;
    this.clickScaleFactor = clickScaleFactor;
    this.hoverBrightnessFactor = hoverBrightnessFactor;
    this.hoverOpacityFactor = hoverOpacityFactor;
    this.backgroundColor = backgroundColor;
  }

  /**
   * {@link Property#bind(ObservableValue) Binds} properties of the {@link TitleBar} to the {@link
   * Stage} and {@link Pane scene root}.
   *
   * @param stage The stage {@link #bind(Stage, TitleBar) binded} to the {@link #buttonLayer
   *     button}.
   * @param titleBar The {@link TitleBar} binded to the {@link #prefWidthProperty() width} and
   *     {@link #prefHeightProperty() height} properties of this {@link TitleBarButton}.
   */
  public void bind(Stage stage, TitleBar titleBar) {
    buttonLayer.setOnAction(
        event -> {
          action.accept(stage);
          event.consume();
        });

    this.idProperty().bind(titleBar.idProperty().concat(" " + id));

    this.prefHeightProperty().bind(titleBar.prefWidthProperty().divide(20));
    this.prefWidthProperty().bind(titleBar.prefWidthProperty().divide(20));

    this.minWidthProperty().bind(titleBar.prefWidthProperty().divide(20));
    this.minHeightProperty().bind(titleBar.prefWidthProperty().divide(20));

    this.setAlignment(Pos.CENTER);

    this.setBackground(
        new Background(
            new BackgroundFill(
                titleBar.backgroundProperty().get().getFills().get(0).getFill(),
                this.corners,
                Insets.EMPTY)));

    this.configureBackground();
    this.configureButton();

    this.addChildren();
  }

  /** Binds {@link #buttonLayer button} properties to the {@link TitleBarButton}. */
  private void configureButton() {
    buttonLayer.idProperty().bind(this.idProperty().concat(" Button"));

    buttonLayer.prefHeightProperty().bind(this.prefHeightProperty());
    buttonLayer.prefWidthProperty().bind(this.prefWidthProperty());

    buttonLayer.clipProperty().bind(this.clipProperty());

    buttonLayer.setBackground(
        new Background(
            new BackgroundImage(
                icon,
                BackgroundRepeat.NO_REPEAT,
                BackgroundRepeat.NO_REPEAT,
                BackgroundPosition.CENTER,
                new BackgroundSize(
                    buttonLayer.getPrefWidth() / 2,
                    buttonLayer.getPrefHeight() / 2,
                    false,
                    false,
                    false,
                    false))));

    buttonLayer.setOpacity(hoverOpacityFactor);
  }

  /** Binds {@link #backgroundLayer background} properties to the {@link TitleBarButton}. */
  private void configureBackground() {
    backgroundLayer.idProperty().bind(this.idProperty().concat(" Background"));
    backgroundLayer.setBlendMode(BlendMode.SRC_ATOP);

    backgroundLayer.widthProperty().bind(this.prefWidthProperty());
    backgroundLayer.heightProperty().bind(this.prefHeightProperty());

    this.backgroundProperty()
        .addListener(
            new ChangeListener<Background>() {
              @Override
              public void changed(
                  ObservableValue<? extends Background> observable,
                  Background oldValue,
                  Background newValue) {
                backgroundLayer.setFill(newValue.getFills().get(0).getFill());
              }
            });

    backgroundLayer.clipProperty().bind(this.clipProperty());
  }

  /**
   * Applies {@link Styles#applyHoverOpacityAnimation(double, double, Duration, javafx.scene.Node)
   * opacity}, {@link Styles#applyHoverFillAnimation(Color, Color, Duration, javafx.scene.Node,
   * javafx.scene.shape.Shape) fill}, {@link Styles#applyClickScaleAnimation(double, double,
   * Duration, Button) and click} animations to {@link #buttonLayer The Button} and {@link
   * #backgroundLayer The Background}.
   */
  private void addChildren() {
    Styles.applyHoverOpacityAnimation(hoverOpacityFactor, 1, Duration.millis(100), buttonLayer);
    Styles.applyHoverFillAnimation(
        backgroundColor.deriveColor(1, 1, 1, 0),
        backgroundColor.deriveColor(1, 1, hoverBrightnessFactor, 1),
        Duration.millis(100),
        buttonLayer,
        backgroundLayer);
    Styles.applyClickScaleAnimation(1, clickScaleFactor, Duration.millis(100), buttonLayer);

    this.getChildren().add(backgroundLayer);
    this.getChildren().add(buttonLayer);
  }
}
