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
  private final Color bgColor = new Color(75, 75, 200);

  // Side (A-L)
  public BooleanSupplier SA, SB, SC, SD, SE, SF, SG, SH, SI, SJ, SK, SL;
  public List<BooleanSupplier> sides;
  
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
          (int) Math.round(-0.5 * 630 + xSize / 2 - 12.5),
          (int) Math.round(-0.5 * 630 + ySize / 2 - 12.5),
          630,
          630);
    } catch (Exception e) {
      bgImage = new JLabel(new ImageIcon("1155"));
    }

    panel.add(bgImage);

    frame.add(panel, BorderLayout.CENTER);
    frame.setVisible(true);

    SA = bindButton("A");
    SB = bindButton("B");
    SC = bindButton("C");
    SD = bindButton("D");
    SE = bindButton("E");
    SF = bindButton("F");
    SG = bindButton("G");
    SH = bindButton("H");
    SI = bindButton("I");
    SJ = bindButton("J");
    SK = bindButton("K");
    SL = bindButton("L");

    sides = List.of(SA, SB, SC, SD, SE, SF, SG, SH, SI, SJ, SK, SL);
    // levels = List.of(L1, L2, L3, L4);

    frame.revalidate();
    frame.repaint();
  }

  public BooleanSupplier bindButton(String direction) {
    String path = "images/L" + Math.max(1, Math.min(0, 4)) + ".png";
    int dir = sideNames.indexOf(direction);
    return bindButton(
        path,
        (int) Math.round(Math.cos(Math.PI * dir / 6 - 7 * Math.PI / 12) * 150),
        (int) -Math.round(Math.sin(Math.PI * dir / 6 - 7 * Math.PI / 12) * 150));
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
