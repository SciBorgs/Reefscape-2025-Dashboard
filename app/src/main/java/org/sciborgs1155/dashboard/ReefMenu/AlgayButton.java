package org.sciborgs1155.dashboard.ReefMenu;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Map;

import org.sciborgs1155.dashboard.Styles;
import org.sciborgs1155.dashboard.ReefMenu.BranchButton.Branch;

import javafx.geometry.Pos;
import javafx.scene.control.Button;
import javafx.scene.layout.Background;
import javafx.scene.layout.Border;
import javafx.scene.paint.Color;
import javafx.scene.shape.Circle;
import javafx.scene.shape.Shape;
import javafx.util.Duration;

public class AlgayButton extends Button {
  /** All of the possible InterBranch names. */
  public static enum InterBranch {
    AB,
    CD,
    EF,
    GH,
    IJ,
    KL,
  }

  /** All of the possible InterBranch names, in an iterable strings. */
  public static final ArrayList<InterBranch> interBranches =
      new ArrayList<>(
          Arrays.asList(
              InterBranch.AB, InterBranch.CD, InterBranch.EF, InterBranch.GH, InterBranch.IJ, InterBranch.KL));

  /**
   * Converts {@link InterBranch} to {@link Integer}.
   *
   * <p>Used for angle calculation.
   */
  public static final Map<InterBranch, Integer> interBranchToInt =
      Map.ofEntries(
          Map.entry(InterBranch.AB, 0),
          Map.entry(InterBranch.CD, 1),
          Map.entry(InterBranch.EF, 2),
          Map.entry(InterBranch.GH, 3),
          Map.entry(InterBranch.IJ, 4),
          Map.entry(InterBranch.KL, 5));

  /** Converts {@link InterBranch} to {@link String}. */
  public static final Map<InterBranch, String> interBranchToString =
      Map.ofEntries(
          Map.entry(InterBranch.AB, "AB"),
          Map.entry(InterBranch.CD, "CD"),
          Map.entry(InterBranch.EF, "EF"),
          Map.entry(InterBranch.GH, "GH"),
          Map.entry(InterBranch.IJ, "IJ"),
          Map.entry(InterBranch.KL, "KL"));

    /** The shape of the button. */
    private static final Shape buttonShape = new Circle(1);

    /** The background of the button. */
    private static final Background background = Background.fill(Color.BLUE.deriveColor(1, 1, 2, 1));

    /** The size of the button relative to the {@link SciButton} in {@link #BranchButton(SciButton, Branch) The Constructor}. */
    private static final double relativeSize = 0.3;

    /** The distance of the button from the {@link SciButton orgin} in terms of the radius of the {@link SciButton}. */
    private static final double positionScale = 0.67;

    /** The each +1 equates to 30 extra degrees of rotation about the {@link SciButton orgin}. */
    private static final double rotationOffset = 0.5;

    /** The size that the button scales up to as it's being hovered over relative to original size. */
    private static final double hoverScaleFactor = 1.1;

    /** The size that the button scales down to as it's being click relative to original size. */
    private static final double clickScaleFactor = 0.9;

    /** The time it takes for animations to run. */
    private static final Duration animationDuration = Duration.millis(50);

  public AlgayButton(SciButton sciButton, InterBranch interBranch) {
    this.setShape(buttonShape);
    this.setBackground(background);
    this.setBorder(Border.stroke(Color.DARKBLUE));

    this.setAlignment(Pos.CENTER);

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
                        .multiply(Math.cos(Math.toRadians(60 * (interBranchToInt.get(interBranch) + rotationOffset)))).multiply(positionScale))
                .add(sciButton.prefWidthProperty().divide(2))
                .subtract(this.prefWidthProperty().divide(2)));
    this.layoutYProperty()
        .bind(
            sciButton
                .layoutYProperty()
                .add(
                    sciButton
                        .prefHeightProperty()
                        .multiply(Math.sin(Math.toRadians(60 * (interBranchToInt.get(interBranch) + rotationOffset)))).multiply(positionScale))
                .add(sciButton.prefHeightProperty().divide(2))
                .subtract(this.prefHeightProperty().divide(2)));

    Styles.applyClickScaleAnimation(hoverScaleFactor, clickScaleFactor, animationDuration, this);
    Styles.applyHoverScaleAnimation(1, hoverScaleFactor, animationDuration,this);
    // Styles.applyHoverOpacityAnimation(0.7, 1, Duration.millis(50), this);
  }
}

