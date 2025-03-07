package org.sciborgs1155.dashboard.ReefMenu;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Map;

import org.sciborgs1155.dashboard.Network;
import org.sciborgs1155.dashboard.Styles;

import javafx.geometry.Pos;
import javafx.scene.control.Button;
import javafx.scene.layout.Background;
import javafx.scene.paint.Color;
import javafx.scene.shape.Circle;
import javafx.scene.shape.Shape;
import javafx.scene.text.Font;
import javafx.scene.text.TextAlignment;
import javafx.util.Duration;

/** This button changes the target branch of the robot for scoring. There are 12. */
public class BranchButton extends Button {
  /** All of the possible branch names. */
  public static enum Branch {
    A,
    B,
    C,
    D,
    E,
    F,
    G,
    H,
    I,
    J,
    K,
    L
  }

  /** All of the possible branches, in an iterable list. */
  public static final ArrayList<Branch> branches =
      new ArrayList<>(
          Arrays.asList(
              Branch.A, Branch.B, Branch.C, Branch.D, Branch.E, Branch.F, Branch.G, Branch.H,
              Branch.I, Branch.J, Branch.K, Branch.L));

  /**
   * Converts {@link Branch Branches} to {@link Integer Integers}.
   *
   * <p>Used for angle calculation.
   */
  public static final Map<Branch, Integer> branchToInt =
      Map.ofEntries(
          Map.entry(Branch.A, 0),
          Map.entry(Branch.B, 1),
          Map.entry(Branch.C, 2),
          Map.entry(Branch.D, 3),
          Map.entry(Branch.E, 4),
          Map.entry(Branch.F, 5),
          Map.entry(Branch.G, 6),
          Map.entry(Branch.H, 7),
          Map.entry(Branch.I, 8),
          Map.entry(Branch.J, 9),
          Map.entry(Branch.K, 10),
          Map.entry(Branch.L, 11));

  /** Converts {@link Branch Branches} to {@link String Strings}. */
  public static final Map<Branch, String> branchToString =
      Map.ofEntries(
          Map.entry(Branch.A, "A"),
          Map.entry(Branch.B, "B"),
          Map.entry(Branch.C, "C"),
          Map.entry(Branch.D, "D"),
          Map.entry(Branch.E, "E"),
          Map.entry(Branch.F, "F"),
          Map.entry(Branch.G, "G"),
          Map.entry(Branch.H, "H"),
          Map.entry(Branch.I, "I"),
          Map.entry(Branch.J, "J"),
          Map.entry(Branch.K, "K"),
          Map.entry(Branch.L, "L"));

    /** The shape of the button. */
    private static final Shape buttonShape = new Circle(1);

    /** The background of the button. */
    private static final Background background = Background.fill(Color.PURPLE.deriveColor(1, 1, 2, 1));

    /** The font of the button. */
    private static final Font font = new Font(30);

    /** The size of the button relative to the {@link SciButton} in {@link #BranchButton(SciButton, Branch) The Constructor}. */
    private static final double relativeSize = 1 / 2.5;

    /** The distance of the button from the {@link SciButton orgin} in terms of the radius of the {@link SciButton}. */
    private static final double positionScale = 1;

    /** The each +1 equates to 30 extra degrees of rotation about the {@link SciButton orgin}. */
    private static final double rotationOffset = 0.5;
    
    /** The size that the button scales up to as it's being hovered over relative to original size. */
    private static final double hoverScaleFactor = 1.1;

    /** The size that the button scales down to as it's being click relative to original size. */
    private static final double clickScaleFactor = 0.9;

    /** The opacity that the button scales down to when it isn't being interacted with. */
    private static final double opacityScaleFactor = 0.7;

    /** The time it takes for animations to run. */
    private static final Duration animationDuration = Duration.millis(50);

  public BranchButton(SciButton sciButton, Branch branch) {
    this.setShape(buttonShape);
    this.setBackground(background);
    this.setOpacity(opacityScaleFactor);

    this.setText(branchToString.get(branch));
    this.setFont(font);

    this.setTextAlignment(TextAlignment.CENTER);
    this.setAlignment(Pos.CENTER);
    this.setTextFill(Color.WHITE);

    this.clipProperty().bind(sciButton.clipProperty());
    this.prefWidthProperty().bind(sciButton.prefWidthProperty().multiply(relativeSize));
    this.prefHeightProperty().bind(sciButton.prefHeightProperty().multiply(relativeSize));

    this.layoutXProperty()
        .bind(
            sciButton
                .layoutXProperty()
                .add(
                    sciButton
                        .prefWidthProperty()
                        .multiply(Math.cos(Math.toRadians(30 * (branchToInt.get(branch) + rotationOffset)))).divide(positionScale))
                .add(sciButton.prefWidthProperty().divide(2))
                .subtract(this.prefWidthProperty().divide(2)));
    this.layoutYProperty()
        .bind(
            sciButton
                .layoutYProperty()
                .add(
                    sciButton
                        .prefHeightProperty()
                        .multiply(Math.sin(Math.toRadians(30 * (branchToInt.get(branch) + rotationOffset)))).divide(positionScale))
                .add(sciButton.prefHeightProperty().divide(2))
                .subtract(this.prefHeightProperty().divide(2)));

    Styles.applyClickScaleAnimation(hoverScaleFactor, clickScaleFactor, animationDuration, this);
    Styles.applyHoverScaleAnimation(1, hoverScaleFactor, animationDuration,this);
    Styles.applyHoverOpacityAnimation(opacityScaleFactor, 1, animationDuration, this);

    // TODO: Add network connection.
    // this.setOnAction(action -> {
    //     Network.activateBranch(branch);
    // });
  }
}
