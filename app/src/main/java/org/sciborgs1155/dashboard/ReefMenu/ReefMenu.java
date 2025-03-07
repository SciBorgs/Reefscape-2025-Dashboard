package org.sciborgs1155.dashboard.ReefMenu;

import java.util.HashMap;
import java.util.Map;

import javafx.scene.layout.Border;
import javafx.scene.layout.Pane;
import javafx.scene.paint.Color;
import javafx.stage.Stage;

import org.sciborgs1155.dashboard.ReefMenu.AlgayButton.InterBranch;
import org.sciborgs1155.dashboard.ReefMenu.BranchButton.Branch;
import org.sciborgs1155.dashboard.TitleBar.TitleBar;

/** The menu for selecting branches/Algays */
public class ReefMenu extends Pane {
  /** The central button, used for sending commands to the robot. */
  private final SciButton sciButton = new SciButton();

  /** Maps {@link Branch} to {@link BranchButton}. */
  private final Map<Branch, BranchButton> branches = new HashMap<>();

  /** Maps {@link InterBranch} to {@link AlgayButton}. */
  private final Map<InterBranch, AlgayButton> interBranches = new HashMap<>();

  /**
   * Constructs a new {@link ReefMenu} that is binded to a {@link Stage}.
   *
   * @param stage The stage binded to this {@link ReefMenu}.
   */
  public ReefMenu(String id, Stage stage, TitleBar titleBar, Pane root) {
    this.setId(id);
    this.setBorder(Border.stroke(Color.gray(0.5)));

    for (Branch branch : BranchButton.branches) {
      this.branches.put(branch, new BranchButton(sciButton, branch));
      this.getChildren().add(this.branches.get(branch));
    }

    for (InterBranch interBranch : AlgayButton.interBranches) {
      this.interBranches.put(interBranch, new AlgayButton(sciButton, interBranch));
      this.getChildren().add(this.interBranches.get(interBranch));
    }

    this.getChildren().add(sciButton);
    this.bind(stage, titleBar, root);
  }

  /**
   * Constructs a new {@link ReefMenu}.
   *
   * <p>{@code NOTE: PROBABLY WON'T WORK WITHOUT CALLING BIND.}
   *
   * <p>{@link #bind(Stage, Pane) The Bind Method.}
   */
  public ReefMenu(String id) {
    this.setId(id);
    this.setBorder(Border.stroke(Color.gray(0.5)));

    for (Branch branch : BranchButton.branches) {
      this.branches.put(branch, new BranchButton(sciButton, branch));
      this.getChildren().add(this.branches.get(branch));
    }

    for (InterBranch interBranch : AlgayButton.interBranches) {
      this.interBranches.put(interBranch, new AlgayButton(sciButton, interBranch));
      this.getChildren().add(this.interBranches.get(interBranch));
    }

    this.getChildren().add(sciButton);
  }

  /** Binds this {@link ReefMenu} to the {@link Stage} and the {@link Pane}. */
  public void bind(Stage stage, TitleBar titleBar ,Pane root) {
    this.prefHeightProperty().bind(stage.heightProperty().subtract(titleBar.prefHeightProperty()));
    this.prefWidthProperty().bind(stage.widthProperty().divide(1));

    sciButton.bind(stage,this);
  }
}
