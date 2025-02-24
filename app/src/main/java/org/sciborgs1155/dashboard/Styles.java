package org.sciborgs1155.dashboard;

import javafx.animation.FadeTransition;
import javafx.animation.FillTransition;
import javafx.animation.ScaleTransition;
import javafx.scene.Node;
import javafx.scene.control.Button;
import javafx.scene.effect.DropShadow;
import javafx.scene.input.MouseEvent;
import javafx.scene.layout.Background;
import javafx.scene.layout.BackgroundFill;
import javafx.scene.layout.Region;
import javafx.scene.paint.Color;
import javafx.scene.shape.Shape;
import javafx.util.Duration;

/** Contains methods for styling certain {@link Node} objects. */
public class Styles {
    /** 
     * Applies a basic on-hover {@link ScaleTransition Scale Transition} to the {@link Node node}.
     * <p> {@code THIS SHOULD ONLY BE CALLED ONCE PER NODE}
     * 
     * @param notHoveredScale The scaling of the node when it isn't being hovered over.
     * @param isHoveredScale The scaling of the node when it is being hovered over.
     * @param duration The amount of time the transition takes(After the mouse hovers over it).
     * @param node The node to apply the transition to.
      */
    public static Node applyHoverScaleAnimation(double notHoveredScale, double isHoveredScale, Duration duration, Node node) {
        final ScaleTransition scaleTransition = new ScaleTransition(duration);
        scaleTransition.setNode(node);
        scaleTransition.setToX(isHoveredScale);
        scaleTransition.setToY(isHoveredScale);
        scaleTransition.setFromX(notHoveredScale);
        scaleTransition.setFromY(notHoveredScale);

        node.addEventHandler(MouseEvent.MOUSE_ENTERED, _ -> {
            scaleTransition.setRate(1);
            node.setViewOrder(-1);
            node.setEffect(new DropShadow(5, Color.BLACK));
            scaleTransition.play();
        });
        node.addEventHandler(MouseEvent.MOUSE_EXITED, _ -> {
            scaleTransition.setRate(-1);
            node.setViewOrder(0);
            scaleTransition.play();
            node.setEffect(new DropShadow(0, Color.TRANSPARENT));
        });

        return node;
    }

    /** 
     * Applies a basic on-hover {@link ScaleTransition Scale Transition} to the {@link Node node}.
     * In addition, adds a {@link DropShadow} to the node when it is scaled up, removed afterwards.
     * <p> {@code THIS SHOULD ONLY BE CALLED ONCE PER NODE}
     * 
     * @param notHoveredScale The scaling of the node when it isn't being hovered over.
     * @param isHoveredScale The scaling of the node when it is being hovered over.
     * @param duration The amount of time the transition takes(After the mouse hovers over it).
     * @param shadow The shadow to apply on hover.
     * @param node The node to apply the transition to.
      */
      public static Node applyHoverScaleAnimationWithShadow(double notHoveredScale, double isHoveredScale, Duration duration, DropShadow shadow, Node node) {
        final ScaleTransition scaleTransition = new ScaleTransition(duration);
        scaleTransition.setNode(node);
        scaleTransition.setToX(isHoveredScale);
        scaleTransition.setToY(isHoveredScale);
        scaleTransition.setFromX(notHoveredScale);
        scaleTransition.setFromY(notHoveredScale);

        node.addEventHandler(MouseEvent.MOUSE_ENTERED, _ -> {
            scaleTransition.setRate(1);
            node.setViewOrder(-1);
            node.setEffect(shadow);
            scaleTransition.play();
        });
        node.addEventHandler(MouseEvent.MOUSE_EXITED, _ -> {
            scaleTransition.setRate(-1);
            node.setViewOrder(0);
            scaleTransition.play();
            node.setEffect(new DropShadow(0, Color.TRANSPARENT));
        });

        return node;
    }

    /** 
     * Applies a basic on-hover {@link ScaleTransition Scale Transition} to the {@link Node node}.
     * In addition, adds a {@link DropShadow} to the node when it is scaled up, removed afterwards.
     * <p> {@code THIS SHOULD ONLY BE CALLED ONCE PER NODE}
     * 
     * @param notHoveredScale The scaling of the node when it isn't being hovered over.
     * @param isHoveredScale The scaling of the node when it is being hovered over.
     * @param duration The amount of time the transition takes(After the mouse hovers over it).
     * @param shadow The shadow to apply on hover.
     * @param eventListener The node to act as the reciever for the hovering.
     * @param node The node to apply the transition to.
      */
      public static Node applyHoverScaleAnimationWithShadow(double notHoveredScale, double isHoveredScale, Duration duration, DropShadow shadow,Node eventListener, Node node) {
        final ScaleTransition scaleTransition = new ScaleTransition(duration);
        scaleTransition.setNode(node);
        scaleTransition.setToX(isHoveredScale);
        scaleTransition.setToY(isHoveredScale);
        scaleTransition.setFromX(notHoveredScale);
        scaleTransition.setFromY(notHoveredScale);

        eventListener.addEventHandler(MouseEvent.MOUSE_ENTERED, _ -> {
            scaleTransition.setRate(1);
            node.setViewOrder(-1);
            node.setEffect(shadow);
            scaleTransition.play();
        });
        eventListener.addEventHandler(MouseEvent.MOUSE_EXITED, _ -> {
            scaleTransition.setRate(-1);
            node.setViewOrder(0);
            scaleTransition.play();
            node.setEffect(new DropShadow(0, Color.TRANSPARENT));
        });

        return node;
    }

    /** 
     * Applies a basic on-click {@link ScaleTransition Scale Transition} to the {@link Button button}.
     * <p> {@code THIS SHOULD ONLY BE CALLED ONCE PER NODE}
     * 
     * @param beforeClickedScale The scaling of the node when it isn't being hovered over.
     * @param afterClickedScale The scaling of the node when it is being hovered over.
     * @param duration The amount of time the transition takes(After the mouse hovers over it).
     * @param node The node to apply the transition to.
      */
      public static Node applyClickScaleAnimation(double beforeClickedScale, double afterClickedScale, Duration duration, Button button) {
        final ScaleTransition scaleTransition = new ScaleTransition(duration);
        scaleTransition.setNode(button);
        scaleTransition.setToX(afterClickedScale);
        scaleTransition.setToY(afterClickedScale);
        scaleTransition.setFromX(beforeClickedScale);
        scaleTransition.setFromY(beforeClickedScale);

        button.addEventHandler(MouseEvent.MOUSE_PRESSED, _ -> {
            scaleTransition.setRate(1);
            button.setViewOrder(-1);
            scaleTransition.play();
        });
        button.addEventHandler(MouseEvent.MOUSE_RELEASED, _ -> {
            scaleTransition.setRate(-2);
            button.setViewOrder(0);
            scaleTransition.play();
        });

        return button;
    }
    
    /** 
     * Applies a basic on-hover {@link FadeTransition Scale Transition} to the {@link Node node}.
     * <p> {@code THIS SHOULD ONLY BE CALLED ONCE PER NODE}
     * 
     * @param notHoveredOpacity The opacity of the node when it isn't being hov`ered over.
     * @param isHoveredOpacity The opacity of the node when it is being hovered over.
     * @param duration The amount of time the transition takes(After the mouse hovers over it).
     * @param node The node to apply the transition to.
      */
    public static Node applyHoverOpacityAnimation(double notHoveredOpacity, double isHoveredOpacity, Duration duration, Node node) {
        final FadeTransition fadeTransition = new FadeTransition(duration);
        fadeTransition.setNode(node);
        fadeTransition.setFromValue(notHoveredOpacity);
        fadeTransition.setToValue(isHoveredOpacity);

        node.addEventHandler(MouseEvent.MOUSE_ENTERED, _ -> {
            fadeTransition.setRate(1);
            fadeTransition.play();
        });
        node.addEventHandler(MouseEvent.MOUSE_EXITED, _ -> {
            fadeTransition.setRate(-1);
            fadeTransition.play();
        });

        return node;
    }

    /** 
     * Applies a basic on-hover background swap to the {@link Region region}. Use {@link #applyHoverFillAnimation(Color, Color, Duration ,Shape)} for smoother animations.
     * <p> {@code THIS SHOULD ONLY BE CALLED ONCE PER REGION}
     * 
     * @param notHoveredFill The fill color of the region when it isn't being hovered over.
     * @param isHoveredFill The fill color of the region when it is being hovered over.
     * @param region The region to apply the transition to.
      */
    public static Region applyHoverFillAnimation(Color notHoveredFill, Color isHoveredFill, Region region) {
        final BackgroundFill regionBackgroundFill = region.getBackground().getFills().get(0);

        final Background notHoveredBackground = new Background(new BackgroundFill(notHoveredFill,regionBackgroundFill.getRadii(),regionBackgroundFill.getInsets()));
        final Background isHoveredBackground = new Background(new BackgroundFill(isHoveredFill,regionBackgroundFill.getRadii(),regionBackgroundFill.getInsets()));

        region.addEventHandler(MouseEvent.MOUSE_ENTERED, _ -> region.setBackground(isHoveredBackground));
        region.addEventHandler(MouseEvent.MOUSE_EXITED, _ -> region.setBackground(notHoveredBackground));

        return region;
    }

    /** 
     * Applies a basic on-hover background color change animation to the {@link Shape shape}.
     * <p> {@code THIS SHOULD ONLY BE CALLED ONCE PER SHAPE}
     * 
     * @param notHoveredFill The fill color of the shape when it isn't being hovered over.
     * @param isHoveredFill The fill color of the shape when it is being hovered over.
     * @param duration The amount of time the transition takes(After the mouse hovers over it).
     * @param shape The shape to apply the transition to.
      */
      public static Shape applyHoverFillAnimation(Color notHoveredFill, Color isHoveredFill, Duration duration, Shape shape) {
        final FillTransition fillTransition = new FillTransition(duration);
        fillTransition.setShape(shape);
        fillTransition.setFromValue(notHoveredFill);
        fillTransition.setToValue(isHoveredFill);

        shape.addEventHandler(MouseEvent.MOUSE_ENTERED, _ -> {
            fillTransition.setRate(1);
            fillTransition.play();
        });
        shape.addEventHandler(MouseEvent.MOUSE_EXITED, _ -> {
            fillTransition.setRate(-1);
            fillTransition.play();
        });

        return shape;
    }

    /** 
     * Applies a basic on-hover background color change animation to the {@link Shape shape}.
     * <p> {@code THIS SHOULD ONLY BE CALLED ONCE PER SHAPE}
     * 
     * @param notHoveredFill The fill color of the shape when it isn't being hovered over.
     * @param isHoveredFill The fill color of the shape when it is being hovered over.
     * @param duration The amount of time the transition takes(After the mouse hovers over it).
     * @param eventListener The node to act as the reciever for the hovering.
     * @param shape The shape to apply the transition to.
      */
      public static Shape applyHoverFillAnimation(Color notHoveredFill, Color isHoveredFill, Duration duration, Node eventListener, Shape shape) {
        final FillTransition fillTransition = new FillTransition(duration);
        fillTransition.setShape(shape);
        fillTransition.setFromValue(notHoveredFill);
        fillTransition.setToValue(isHoveredFill);

        eventListener.addEventHandler(MouseEvent.MOUSE_ENTERED, _ -> {
            fillTransition.setRate(1);
            fillTransition.play();
        });
        eventListener.addEventHandler(MouseEvent.MOUSE_EXITED, _ -> {
            fillTransition.setRate(-1);
            fillTransition.play();
        });

        return shape;
    }
}
