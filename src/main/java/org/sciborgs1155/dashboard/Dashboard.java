package org.sciborgs1155.dashboard;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.image.BufferedImage;
import java.util.List;
import java.util.function.BooleanSupplier;

import javax.imageio.ImageIO;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;

import static org.sciborgs1155.dashboard.Constants.*;

public class Dashboard {
  private final JFrame frame;
  private final JPanel panel;
  private final int xSize = 680;
  private final int ySize = 680;
  private final Color bgColor = new Color(50, 50, 100);

  // Side (A-L)
  public BooleanSupplier SA, SB, SC, SD, SE, SF, SG, SH, SI, SJ, SK, SL;
  public List<BooleanSupplier> branches;
  
  // Level (1-4)
  // public BooleanSupplier L1, L2, L3, L4;
  // public List<BooleanSupplier> levels;

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
    panel.setVisible(true);

    JLabel bgImage;
    try {
      BufferedImage buffer = ImageIO.read(getClass().getResource("images/bg.png"));
      bgImage = new JLabel(new ImageIcon(buffer));
      bgImage.setBounds(
          (int) Math.round(-0.5 * 474 + xSize / 2 - 12.5),
          (int) Math.round(-0.5 * 409 + ySize / 2 - 12.5),
          474,
          409);
    } catch (Exception e) {
      bgImage = new JLabel(new ImageIcon("1155"));
    }

    panel.add(bgImage);

    frame.add(panel, BorderLayout.CENTER);
    frame.setVisible(true);

    SA = bindButton("A", "images/branch.png");
    SB = bindButton("B", "images/branch.png");
    SC = bindButton("C", "images/branch.png");
    SD = bindButton("D", "images/branch.png");
    SE = bindButton("E", "images/branch.png");
    SF = bindButton("F", "images/branch.png");
    SG = bindButton("G", "images/branch.png");
    SH = bindButton("H", "images/branch.png");
    SI = bindButton("I", "images/branch.png");
    SJ = bindButton("J", "images/branch.png");
    SK = bindButton("K", "images/branch.png");
    SL = bindButton("L", "images/branch.png");

    branches = List.of(SA, SB, SC, SD, SE, SF, SG, SH, SI, SJ, SK, SL);
    // levels = List.of(L1, L2, L3, L4);

    frame.revalidate();
    frame.repaint();
  }

  public BooleanSupplier bindButton(String direction, String imgPath) {
    int dir = branchNames.indexOf(direction);
    return bindButton(
        imgPath,
        (int) Math.round(Math.cos(Math.PI * dir / 6 - 7 * Math.PI / 12) * 125),
        (int) -Math.round(Math.sin(Math.PI * dir / 6 - 7 * Math.PI / 12) * 125));
  }

  public BooleanSupplier bindButton(String path, int x, int y) {
    try {
      BufferedImage buffer = ImageIO.read(getClass().getResource(path));
      JButton button = new JButton(new ImageIcon(buffer));
      button.setBounds(
          (int) Math.round(x - 25 + xSize / 2 - 12.5),
          (int) Math.round(y - 25 + ySize / 2 - 12.5),
          50,
          50);
      button.setOpaque(true);
      panel.add(button);
      return () -> button.getModel().isPressed();
    } catch (Exception e) {
      JButton button = new JButton(path);
      button.setOpaque(true);
      panel.add(button);
      return () -> button.getModel().isPressed();
    }
  }

  public void close() {
    frame.dispose();
  }
}
