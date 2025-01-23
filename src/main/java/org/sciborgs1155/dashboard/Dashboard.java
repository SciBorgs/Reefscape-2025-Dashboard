package org.sciborgs1155.dashboard;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Font;
import java.awt.image.BufferedImage;
import java.util.List;
import javax.imageio.ImageIO;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;

public class Dashboard {
  private final JFrame frame;
  private final JPanel panel;
  private final int xSize = 1500;
  private final int ySize = 865;
  private Color bgColor = new Color(0, 131, 174);
  private JButton goButton, redButton, blueButton;
  private JLabel bgImage;

  // Side (A-L)
  public JButton SA, SB, SC, SD, SE, SF, SG, SH, SI, SJ, SK, SL;
  public List<JButton> branches;

  // Level (1-4)
  public JButton L1, L2, L3, L4;
  public List<JButton> levelsButtons;
  public List<JButton> levels;

  private JButton processorButton;
  public JButton processor;

  public JButton RESET, RED, BLUE;
  public JButton GO;

  public JLabel displayLabel;

  private String selectedBranch;
  private String selectedLevel;

  /** The GUI of the operator dashboard. */
  public Dashboard() {
    frame = new JFrame("JFrame");
    frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    frame.setSize(xSize, ySize);
    frame.setLayout(null);

    frame.getContentPane().setBackground(bgColor);

    panel = new JPanel();
    panel.setSize(xSize, ySize);
    panel.setLayout(null);
    panel.setBackground(bgColor);

    displayLabel = new JLabel(" ");
    displayLabel.setBounds(10, 10, 140, 80);
    displayLabel.setOpaque(true);
    displayLabel.setBackground(Color.BLACK);
    displayLabel.setForeground(bgColor);
    displayLabel.setFont(new Font("Arial", Font.BOLD, 65));
    panel.add(displayLabel);

    selectedBranch = "";
    selectedLevel = "";

    JLabel bgImage;
    try {
      BufferedImage buffer = ImageIO.read(getClass().getResource("images/bg_blue.png"));
      bgImage = new JLabel(new ImageIcon(buffer));
      bgImage.setBounds(-20, -15, 1498, 861);
    } catch (Exception e) {
      bgImage = new JLabel(new ImageIcon("1155"));
    }
    this.bgImage = bgImage;

    SA = bindButtonWithBranch("A", "images/br_As.png", 602, 647, 126, 153);
    SB = bindButtonWithBranch("B", "images/br_Bm.png", 742, 647, 126, 153);
    SC = bindButtonWithBranch("C", "images/br_Ct.png", 915, 573, 124, 151);
    SE = bindButtonWithBranch("D", "images/br_Dw.png", 1048, 421, 126, 152);
    SF = bindButtonWithBranch("E", "images/br_Ev.png", 1010, 251, 124, 152);
    SD = bindButtonWithBranch("F", "images/br_Fg.png", 917, 97, 126, 151);
    SG = bindButtonWithBranch("G", "images/br_Go.png", 742, 31, 122, 152);
    SH = bindButtonWithBranch("H", "images/br_Hl.png", 601, 31, 126, 151);
    SI = bindButtonWithBranch("I", "images/br_Ik.png", 420, 97, 126, 152);
    SJ = bindButtonWithBranch("J", "images/br_Jp.png", 328, 254, 125, 152);
    SK = bindButtonWithBranch("K", "images/br_Ks.png", 278, 421, 124, 152);
    SL = bindButtonWithBranch("L", "images/br_Lp.png", 411, 573, 124, 152);

    branches = List.of(SA, SB, SC, SD, SE, SF, SG, SH, SI, SJ, SK, SL);
    processor = bindButton("images/processor.png", 1309, 6, 147, 185);
    processorButton = (JButton) panel.getComponent(panel.getComponentCount() - 1);
    processorButton.addActionListener(
        e -> {
          if (processorButton.isSelected()) {
            processorButton.setSelected(false);
            goButton.setEnabled(false);
            displayLabel.setText("");
            levelsButtons.forEach(levelButton -> levelButton.setEnabled(true));
          } else {
            processorButton.setSelected(true);
            goButton.setEnabled(true);
            displayLabel.setHorizontalAlignment(JLabel.CENTER);
            displayLabel.setFont(new Font("Arial", Font.BOLD, 38));
            displayLabel.setText("PCSR" + selectedBranch + selectedLevel);
            levelsButtons.forEach(levelButton -> levelButton.setEnabled(false));
          }
        });

    L1 = bindButton("images/lb_L1.png", 1333, 532, 103, 99);
    JButton l1Button = (JButton) panel.getComponent(panel.getComponentCount() - 1);
    L2 = bindButton("images/lb_L2.png", 1333, 428, 103, 99);
    JButton l2Button = (JButton) panel.getComponent(panel.getComponentCount() - 1);
    L3 = bindButton("images/lb_L3.png", 1333, 322, 103, 99);
    JButton l3Button = (JButton) panel.getComponent(panel.getComponentCount() - 1);
    L4 = bindButton("images/lb_L4.png", 1333, 219, 103, 99);
    JButton l4Button = (JButton) panel.getComponent(panel.getComponentCount() - 1);
    levels = List.of(L1, L2, L3, L4);

    levelsButtons = List.of(l1Button, l2Button, l3Button, l4Button);
    levelsButtons.forEach(
        e -> {
          e.setEnabled(true);
          e.setBorderPainted(false);
        });
    levelsButtons.forEach(
        levelButton ->
            levelButton.addActionListener(
                e -> {
                  selectedLevel = " " + (levelsButtons.indexOf(levelButton) + 1);
                  displayLabel.setHorizontalAlignment(JLabel.CENTER);
                  displayLabel.setText(selectedBranch + selectedLevel);
                  goButton.setEnabled(!selectedBranch.isEmpty() && !selectedLevel.isEmpty());
                }));

    GO = bindButton("images/goo.png", 1333, 660, 100, 99);
    goButton = (JButton) panel.getComponent(panel.getComponentCount() - 1);
    goButton.setEnabled(false);
    goButton.setBorderPainted(false);
    goButton.addActionListener(
        e -> {
          goButton.setEnabled(false);
          selectedBranch = "";
          selectedLevel = "";
          displayLabel.setText(selectedBranch + selectedLevel);
          processorButton.setEnabled(true);
          levelsButtons.forEach(levelButton -> levelButton.setEnabled(true));
        });

    RESET = bindButton("images/reset_b.png", 16, 513, 100, 100);
    JButton resetButton = (JButton) panel.getComponent(panel.getComponentCount() - 1);
    resetButton.setBorderPainted(false);

    changeBackground("images/bg_blue.png");

    panel.setVisible(true);
    panel.add(bgImage);
    frame.add(panel, BorderLayout.CENTER);
    frame.setVisible(true);
  }

  // private void resetAll() {
  //   scoredBranches.clear(); // Clear scored branches map
  //   cbxAction(); // Reset levels and GO button
  //   if (selectedBranchButton != null) {
  //     selectedBranchButton.setBorder(null); // Remove border from selected branch button
  //     selectedBranchButton = null;
  //   }
  //   if (selectedLevelButton != null) {
  //     selectedLevelButton.setBorder(null); // Remove border from selected level button
  //     selectedLevelButton = null;
  //   }
  // }

  public JButton bindButtonWithBranch(String branch, String imgPath, int x, int y, int w, int h) {
    JButton buttonB = bindButton(imgPath, x, y, w, h);
    // Enable level buttons when any branch button is pressed
    JButton button = (JButton) panel.getComponent(panel.getComponentCount() - 1);
    button.addActionListener(
        e -> {
          if (selectedBranch.equals(branch)) {
            selectedBranch = "";
            selectedLevel = "";
            button.setSelected(false);
            levelsButtons.forEach(levelButton -> levelButton.setSelected(false));
          } else {
            selectedBranch = branch;
            button.setSelected(true);
          }
          displayLabel.setHorizontalAlignment(JLabel.CENTER);
          displayLabel.setText(selectedBranch + " " + selectedLevel);
          goButton.setEnabled(!selectedBranch.isEmpty() && !selectedLevel.isEmpty());
          processorButton.setEnabled(selectedBranch.isEmpty());
        });
    return buttonB;
  }

  public JButton bindButton(String path, int x, int y, int w, int h) {
    try {
      BufferedImage buffer = ImageIO.read(getClass().getResource(path));
      JButton button = new JButton(new ImageIcon(buffer));
      button.setBounds(x, y, w, h);
      button.setOpaque(true);
      panel.add(button);
      return button;
    } catch (Exception e) {
      JButton button = new JButton(path);
      button.setOpaque(true);
      panel.add(button);
      return button;
    }
  }

  public void changeBackground(String imgPath) {
    try {
      BufferedImage buffer = ImageIO.read(getClass().getResource(imgPath));
      bgImage.setIcon(new ImageIcon(buffer));
      if (imgPath.contains("bg_blue")) {
        bgColor = new Color(0, 131, 174); // Blue background
        displayLabel.setForeground(bgColor);
        levelsButtons
            .get(0)
            .setIcon(new ImageIcon(ImageIO.read(getClass().getResource("images/lb_L1.png"))));
        levelsButtons
            .get(1)
            .setIcon(new ImageIcon(ImageIO.read(getClass().getResource("images/lb_L2.png"))));
        levelsButtons
            .get(2)
            .setIcon(new ImageIcon(ImageIO.read(getClass().getResource("images/lb_L3.png"))));
        levelsButtons
            .get(3)
            .setIcon(new ImageIcon(ImageIO.read(getClass().getResource("images/lb_L4.png"))));
        goButton.setIcon(new ImageIcon(ImageIO.read(getClass().getResource("images/goo.png"))));
        redButton.setIcon(new ImageIcon(ImageIO.read(getClass().getResource("images/red.png"))));
        blueButton.setIcon(new ImageIcon(ImageIO.read(getClass().getResource("images/blue.png"))));
        ((JButton) panel.getComponent(panel.getComponentCount() - 4))
            .setIcon(
                new ImageIcon(
                    ImageIO.read(getClass().getResource("images/reset_b.png")))); // Reset button
      } else if (imgPath.contains("bg_red")) {
        bgColor = new Color(197, 45, 60); // Red background
        displayLabel.setForeground(bgColor);
        levelsButtons
            .get(0)
            .setIcon(new ImageIcon(ImageIO.read(getClass().getResource("images/lr_L1.png"))));
        levelsButtons
            .get(1)
            .setIcon(new ImageIcon(ImageIO.read(getClass().getResource("images/lr_L2.png"))));
        levelsButtons
            .get(2)
            .setIcon(new ImageIcon(ImageIO.read(getClass().getResource("images/lr_L3.png"))));
        levelsButtons
            .get(3)
            .setIcon(new ImageIcon(ImageIO.read(getClass().getResource("images/lr_L4.png"))));
        goButton.setIcon(new ImageIcon(ImageIO.read(getClass().getResource("images/rgoo.png"))));
        redButton.setIcon(new ImageIcon(ImageIO.read(getClass().getResource("images/rred.png"))));
        blueButton.setIcon(new ImageIcon(ImageIO.read(getClass().getResource("images/rblue.png"))));
        ((JButton) panel.getComponent(panel.getComponentCount() - 4))
            .setIcon(
                new ImageIcon(
                    ImageIO.read(getClass().getResource("images/reset_r.png")))); // Reset button
      } else if (imgPath.contains("bg_disconnected")) {
        bgColor = new Color(50, 50, 50);
        displayLabel.setForeground(bgColor);
      }
      panel.setBackground(bgColor);
    } catch (Exception e) {
      e.printStackTrace();
    }
  }

  public void close() {
    frame.dispose();
  }
}
