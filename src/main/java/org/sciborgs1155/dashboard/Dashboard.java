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

public class Dashboard {
  private final JFrame frame;
  private final JPanel panel;
  private final int xSize = 680;
  private final int ySize = 680;
  private final Color bgColor = new Color(75, 75, 200);
  private final List<String> track =
      List.of("A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L");

  // there are definitely ways to make this better and not create 48 booleansuppliers like this
  // (since theres probably a smarter way then to write command for 48 different booleansuppliers
  // differently)
  public BooleanSupplier A1, B1, C1, D1, E1, F1, G1, H1, I1, J1, K1, L1;
  public BooleanSupplier A2, B2, C2, D2, E2, F2, G2, H2, I2, J2, K2, L2;
  public BooleanSupplier A3, B3, C3, D3, E3, F3, G3, H3, I3, J3, K3, L3;
  public BooleanSupplier A4, B4, C4, D4, E4, F4, G4, H4, I4, J4, K4, L4;

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

    
    // sorry
    A1 = bindButton("A", 1);
    A2 = bindButton("A", 2);
    A3 = bindButton("A", 3);
    A4 = bindButton("A", 4);
    B1 = bindButton("B", 1);
    B2 = bindButton("B", 2);
    B3 = bindButton("B", 3);
    B4 = bindButton("B", 4);
    C1 = bindButton("C", 1);
    C2 = bindButton("C", 2);
    C3 = bindButton("C", 3);
    C4 = bindButton("C", 4);
    D1 = bindButton("D", 1);
    D2 = bindButton("D", 2);
    D3 = bindButton("D", 3);
    D4 = bindButton("D", 4);
    E1 = bindButton("E", 1);
    E2 = bindButton("E", 2);
    E3 = bindButton("E", 3);
    E4 = bindButton("E", 4);
    F1 = bindButton("F", 1);
    F2 = bindButton("F", 2);
    F3 = bindButton("F", 3);
    F4 = bindButton("F", 4);
    G1 = bindButton("G", 1);
    G2 = bindButton("G", 2);
    G3 = bindButton("G", 3);
    G4 = bindButton("G", 4);
    H1 = bindButton("H", 1);
    H2 = bindButton("H", 2);
    H3 = bindButton("H", 3);
    H4 = bindButton("H", 4);
    I1 = bindButton("I", 1);
    I2 = bindButton("I", 2);
    I3 = bindButton("I", 3);
    I4 = bindButton("I", 4);
    J1 = bindButton("J", 1);
    J2 = bindButton("J", 2);
    J3 = bindButton("J", 3);
    J4 = bindButton("J", 4);
    K1 = bindButton("K", 1);
    K2 = bindButton("K", 2);
    K3 = bindButton("K", 3);
    K4 = bindButton("K", 4);
    L1 = bindButton("L", 1);
    L2 = bindButton("L", 2);
    L3 = bindButton("L", 3);
    L4 = bindButton("L", 4);

    frame.revalidate();
    frame.repaint();
  }

  public BooleanSupplier bindButton(String direction, int level) {
    String path = "images/L" + Math.max(1, Math.min(level, 4)) + ".png";
    int dir = track.indexOf(direction);
    return bindButton(
        path,
        (int) Math.round(Math.cos(Math.PI * dir / 6 - 7 * Math.PI / 12) * (level + 1) * 55),
        (int) -Math.round(Math.sin(Math.PI * dir / 6 - 7 * Math.PI / 12) * (level + 1) * 55));
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
