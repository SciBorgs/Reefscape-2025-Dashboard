package org.sciborgs1155.dashboard.TitleBar;

import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.geometry.Dimension2D;
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
import javafx.scene.layout.StackPane;
import javafx.scene.paint.Color;
import javafx.scene.shape.Rectangle;
import javafx.stage.Stage;
import javafx.util.Duration;
import org.sciborgs1155.dashboard.Styles;

/** Template for {@link CloseButton}, {@link MinimizeButton}, and {@link MaximizeButton}. */
public class TitleBarButtons extends StackPane {
  /** Is used for hover-effect animations. */
  private final Rectangle backgroundLayer;

  /** Is what the user interacts with. */
  private final Button buttonLayer;

  /** The color of the background. */
  private final Color backgroundColor;

  /** The amount that the button is scaled down when it's clicked over. */
  private final double clickScaleFactor;

  /** The amount that the button is brightened up when it's hovered over. */
  private final double hoverBrightnessFactor;

  /** The dimensions of the whole stack pane. */
  private final Dimension2D size;

  /** The icon displayed on the button, shrunk down to half the size of the button itself. */
  private final Image icon;

  /** Customs insets(useful for corner buttons that need rounded corners). */
  private final CornerRadii corners;

  /**
   * A generic close button that appears at the corner of a {@link TitleBar}.
   *
   * @param stage The stage to close on click.
   * @return The button.
   */
  public static TitleBarButtons closeButton(Stage stage) {
    return new TitleBarButtons(
        "Close Button",
        event -> {
          stage.close();
          event.consume();
        },
        stage,
        new Image(ClassLoader.getSystemResourceAsStream("TitleBarResources/closeButton.png")),
        new Dimension2D(50, 50),
        Color.BLACK,
        new CornerRadii(0, 18, 0, 0, false),
        0.9,
        3.0);
  }

  /**
   * A generic maximize button that appears 2nd from the corner of a {@link TitleBar}.
   *
   * @param stage The stage to maximize on click.
   * @return The button.
   */
  public static TitleBarButtons maximizeButton(Stage stage) {
    EventHandler<ActionEvent> action =
        event -> {
          if (stage.isMaximized()) {
            stage.setMaximized(false);
          } else {
            stage.setMaximized(true);
          }
          event.consume();
        };

    return new TitleBarButtons(
        "Maximize Button",
        action,
        stage,
        new Image(ClassLoader.getSystemResourceAsStream("TitleBarResources/maximizeButton.png")),
        new Dimension2D(50, 50),
        Color.BLACK,
        CornerRadii.EMPTY,
        0.9,
        3.0);
  }

  /**
   * A generic minimize button that appears 3rd from the corner of a {@link TitleBar}.
   *
   * @param stage The stage to minimize on click.
   * @return The button.
   */
  public static TitleBarButtons minimizeButton(Stage stage) {
    return new TitleBarButtons(
        "Minimize Button",
        event -> {
          stage.setIconified(true);
          event.consume();
        },
        stage,
        new Image(ClassLoader.getSystemResourceAsStream("TitleBarResources/minimizeButton.png")),
        new Dimension2D(50, 50),
        Color.BLACK,
        CornerRadii.EMPTY,
        0.9,
        3.0);
  }

  /**
   * The Constructor.
   *
   * @param action The action to do on the click of this button.
   * @param stage The stage to act upon on the click of this button.
   * @param icon The icon of the button.
   * @param size The size of the button(pixels).
   * @param backgroundColor The color of the background.
   * @param clickScaleFactor The factor by which the size of the button is scaled on-click.
   * @param hoverBrightnessFactor The factor by which the brightness of the background is scaled
   *     on-hover.
   */
  public TitleBarButtons(
      String id,
      EventHandler<ActionEvent> action,
      Stage stage,
      Image icon,
      Dimension2D size,
      Color backgroundColor,
      CornerRadii corners,
      double clickScaleFactor,
      double hoverBrightnessFactor) {
    this.corners = corners;
    this.size = size;
    this.icon = icon;
    this.clickScaleFactor = clickScaleFactor;
    this.hoverBrightnessFactor = hoverBrightnessFactor;
    this.backgroundColor = backgroundColor;

    this.configurePane(
        this.icon,
        id,
        this.size,
        new Background(new BackgroundFill(this.backgroundColor, this.corners, Insets.EMPTY)));

    backgroundLayer = backgroundLayer();
    buttonLayer = buttonLayer(stage, this.icon, action);

    this.addChildren(buttonLayer, backgroundLayer);
  }

  /**
   * The Constructor.
   *
   * @param action The action to do on the click of this button.
   * @param stage The stage to act upon on the click of this button.
   */
  public TitleBarButtons(String id, EventHandler<ActionEvent> action, Stage stage) {
    this.corners = new CornerRadii(0, 18, 0, 0, false);
    this.size = new Dimension2D(50, 50);
    this.icon = new Image(ClassLoader.getSystemResourceAsStream("sciborg.png"));
    this.clickScaleFactor = 1.2;
    this.hoverBrightnessFactor = 3;
    this.backgroundColor = Color.gray(0.1);

    this.configurePane(
        icon, id, size, new Background(new BackgroundFill(backgroundColor, corners, Insets.EMPTY)));

    backgroundLayer = backgroundLayer();
    buttonLayer =
        buttonLayer(
            stage,
            icon,
            event -> {
              System.out.println("1155!");
              event.consume();
            });

    this.addChildren(buttonLayer, backgroundLayer);
  }

  /** Creates a stylized button-layer template for the {@link TitleBar}. */
  private Button buttonLayer(Stage stage, Image icon, EventHandler<ActionEvent> action) {
    final Button buttonLayer = new Button();
    buttonLayer.setId(this.getId() + " Interactable");

    buttonLayer.setPrefSize(this.getWidth(), this.getHeight());
    buttonLayer.setClip(this.getClip());

    buttonLayer.setBackground(
        new Background(
            new BackgroundImage(
                icon,
                BackgroundRepeat.NO_REPEAT,
                BackgroundRepeat.NO_REPEAT,
                BackgroundPosition.CENTER,
                new BackgroundSize(
                    this.getWidth() / 2, this.getHeight() / 2, false, false, false, false))));
    buttonLayer.setOnAction(action);

    return buttonLayer;
  }

  /** Creates a stylized background-layer template for the {@link TitleBar}. */
  private Rectangle backgroundLayer() {
    final Rectangle backgroundLayer =
        new Rectangle(this.getWidth(), this.getHeight(), backgroundColor);
    backgroundLayer.setId(this.getId() + " Background");
    backgroundLayer.prefWidth(backgroundLayer.getWidth());
    backgroundLayer.prefHeight(backgroundLayer.getHeight());
    backgroundLayer.setBlendMode(BlendMode.SRC_ATOP);
    backgroundLayer.setClip(this.getClip());

    return backgroundLayer;
  }

  /** Configures the properties of the {@link StackPane}. */
  private void configurePane(Image icon, String id, Dimension2D dimensions, Background background) {
    this.setId(id);

    this.prefWidth(dimensions.getWidth());
    this.prefHeight(dimensions.getHeight());

    this.setWidth(dimensions.getWidth());
    this.setHeight(dimensions.getHeight());

    this.setAlignment(Pos.CENTER);
    this.setBackground(background);
  }

  /** Applies transition animations to children and adds them to the {@link StackPane} */
  private void addChildren(Button buttonLayer, Rectangle backgroundLayer) {
    // TODO: Add Opacity factor to constructor.
    Styles.applyHoverOpacityAnimation(0.7, 1, Duration.millis(100), buttonLayer);
    Styles.applyHoverFillAnimation(
        backgroundColor,
        backgroundColor.deriveColor(1, 1, hoverBrightnessFactor, 1),
        Duration.millis(100),
        buttonLayer,
        backgroundLayer);
    Styles.applyClickScaleAnimation(1, clickScaleFactor, Duration.millis(100), buttonLayer);

    this.getChildren().add(backgroundLayer);
    this.getChildren().add(buttonLayer);
  }
}
