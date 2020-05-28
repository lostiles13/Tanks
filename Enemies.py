import arcade
import numpy as np
import random

import tanks


class Enemy(arcade.Sprite):
    def __init__(self, texture):
        super().__init__(texture)
        # Correcting for tanks facing downwards
        self.texture_transform = arcade.Matrix3x3().rotate(90)
        # Fixing distortion caused by texture rotation
        # Or get rid of for fat little tanks which are also cute
        self.width, self.height = self.height, self.width
        # Set initial values
        self.speed = 0
        self.change_angle = 0
        self.cur_direction = np.array([np.cos(self.radians), np.sin(self.radians)])

        self.spawning = True
        self.alpha = 0

    def draw_direction(self, length: float = 40, color=arcade.color.RED):
        """
        Helper function to draw a currently facing line if needed
        to help troubleshoot movement.

        Inputs:
            length (float): length of line
            color (3-tuple): arcade color or tuple for line color
        """
        arcade.draw_line(
            self.center_x,
            self.center_y,
            self.center_x + length * self.cur_direction[0],
            self.center_y + length * self.cur_direction[1],
            color,
            2,
        )

    def forward(self, speed: float = 1.0):
        """
        The built-in forward method seems to do INSANE things by
        _incrementing_ the current speed by the angle and speed, which 
        seems entirely counter-intuitive. This here seems much more 
        intuitive. Sets the velocity according to the desired speed and
        current facing direction.

        Inputs:
            speed (float): desired pixel speed
        """
        self.change_x = np.cos(self.radians) * speed
        self.change_y = np.sin(self.radians) * speed

    def update(self):
        if self.spawning:
            self.alpha += 3
            if self.alpha >= 254:
                self.spawning = False
        else:
            super().update()

            # Bounce top and bottom
            if self.center_y > tanks.HEIGHT or self.center_y < 0:
                # Reset to wall edge
                if abs(self.center_y - tanks.HEIGHT) < abs(self.center_y - 0):
                    self.center_y = tanks.HEIGHT
                else:
                    self.center_y = 0
                # mirror angle
                self.change_y *= -1
                # Update sprite facing direction
                self.radians = np.arctan2(self.change_y, self.change_x)

            # Bounce left and right
            if self.center_x > tanks.WIDTH or self.center_x < 0:
                # Reset to wall edge
                if abs(self.center_x - tanks.WIDTH) < abs(self.center_x - 0):
                    self.center_x = tanks.WIDTH
                else:
                    self.center_x = 0
                # Mirror angle
                self.change_x *= -1
                # Update facingc direction
                self.radians = np.arctan2(self.change_y, self.change_x)

            # Reset velocity to new forward direction
            self.forward(self.speed)
            # Update current direction
            self.cur_direction = np.array([np.cos(self.radians), np.sin(self.radians)])

    def will_fire(self):
        """
        Determines whether an enemy will fire during a frame. 
        Higher values make it much more likely.

        Returns:
            boolean: if a projectile will be fired
        """
        if self.spawning:
            chance = -1
        else:
            chance = 2
        return random.randint(0, 100) <= chance

    def fire(self):
        """
        Creates and returns a Bullet object fired by this enemy.

        Returns:
            Bullet: one bullet object originating from the enemy and moving
                    in the proper direction.
        """
        bullet = tanks.Bullets("Sprites/barrelRed_top.png", 0.5)
        bullet.angle = self.angle
        bullet.position = (self.center_x, self.center_y)
        direction = np.array([np.cos(bullet.radians), np.sin(bullet.radians)])
        bullet.velocity = 2 * tanks.MOVEMENT_SPEED * direction

        return bullet


class RedEnemy(Enemy):
    """
    Enemy which just spins in circles and fires.
    """

    def __init__(self, angle_rate: float):
        super().__init__("Sprites/tank_red.png")
        self.change_angle = angle_rate
        # Give chance to rotate opposite direction
        if random.randint(0, 1):
            self.change_angle *= -1


class GreenEnemy(Enemy):
    """
    Enemy which spins and occasionally flips rotation direction.
    """

    def __init__(self, angle_rate: float):
        super().__init__("Sprites/tank_green.png")
        self.change_angle = angle_rate

    def update(self):
        super().update()
        if random.random() < 0.01:
            self.change_angle *= -1


class SandEnemy(Enemy):
    """
    Enemy which moves straight, bouncing off walls.
    """

    def __init__(self, speed: float):
        super().__init__("Sprites/tank_sand.png")
        self.speed = 2


class WobblerEnemy(GreenEnemy):
    """
    Combination of Green and Sand, which moves and
    occassionally flips rotating direction.
    """

    def __init__(self, angle_rate: float, speed: float):
        Enemy.__init__(self, "Sprites/tank_bigRed.png")
        self.change_angle = angle_rate
        self.speed = speed
