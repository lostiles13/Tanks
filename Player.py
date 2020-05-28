import arcade
import numpy as np
import random

import tanks


class Player(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__("Sprites/tank_blue.png")
        self.fire_noise = arcade.Sound("Sounds/tank_fire.mp3")
        self.center_x = x
        self.center_y = y
        self.cur_keys_pressed = []
        self.turn_rate = 5
        self.distance_traveled = 0
        self.force_max = 5
        self.torque_max = 5
        self.force_cur = 0
        self.torque_cur = 0
        self.mass = 1
        self.topspeed = tanks.MOVEMENT_SPEED
        self.toprot = 3

        self.friction_base = 0.2
        self.friction_current = self.friction_base

        self.precise_mode = False

    def set_precise_mode(self, value: bool):
        """ 
        Sets a special turning mode that decreases the turning radius
        by half. This helps when trying to line up tricky shots, without
        killing the tank manuverability.

        Inputs:
            value (boolean): where to turn precise mode on (true) or off (false)
        """
        self.precise_mode = value

    def turn_left(self):
        """ Turn tank to the left """
        if self.precise_mode:
            # self.change_angle = self.turn_rate / 2
            self.torque_cur = self.torque_max / 10
        else:
            # self.change_angle = self.turn_rate
            self.torque_cur = self.torque_max

    def turn_right(self):
        """ Turn tank to the right """
        if self.precise_mode:
            # self.change_angle = -self.turn_rate / 2
            self.torque_cur = -self.torque_max / 10
        else:
            # self.change_angle = -self.turn_rate
            self.torque_cur = -self.torque_max

    def forward(self, speed: float):
        """ 
        Set tank speed forward in facing direction

        Input:
            speed (float): speed to move forward
        """
        # self.change_x = speed * np.cos(self.radians)
        # self.change_y = speed * np.sin(self.radians)
        self.force_cur = self.force_max

    def reverse(self, speed: float):
        """
        Set tank moving backwards at some speed

        Input:
            speed (float): speed to move backwards
        """
        # self.forward(-speed)
        self.force_cur = -self.force_max

    def fire(self):
        """
        Fire a bullet object. Creates a new bullet object with
        the necessary parameters and returns it.

        Output:
            (Bullet): a new bullet object
        """
        bullet = tanks.Bullets("Sprites/specialBarrel6.png")
        bullet.texture_transform = arcade.Matrix3x3().rotate(-90)
        bullet.width, bullet.height = bullet.height, bullet.width
        bullet.center_x = self.center_x
        bullet.center_y = self.center_y
        bullet.radians = self.radians
        bullet.change_x = 2 * tanks.MOVEMENT_SPEED * np.cos(self.radians)
        bullet.change_y = 2 * tanks.MOVEMENT_SPEED * np.sin(self.radians)
        self.fire_noise.play(0.25)

        return bullet

    def add_key(self, key: int):
        """
        Setter function to add a key to the list of currently
        pressed keys.

        Inputs:
            key (int): arcade key code
        """
        self.cur_keys_pressed.append(key)

    def remove_key(self, key: int):
        """
        Setter function to remove a key from the list of currently pressed
        keys, presumably when that key stops being held down.

        Inputs:
            key (int): arcade key code
        """
        if key in self.cur_keys_pressed:
            self.cur_keys_pressed.remove(key)

    def get_distance_traveled(self):
        return self.distance_traveled

    def reset_distance(self):
        self.distance_traveled = 0

    def update_friction(self, oil_list):
        if arcade.check_for_collision_with_list(self, oil_list):
            self.friction_current = self.friction_base / 5
        else:
            self.friction_current = self.friction_base

    def update_movement(self):
        """
        Updating the velocity and turning of the tank based on keys currently pressed
        and a small and very rudimentary physics engine. Allows for a bit of 'slop'
        in movement as friction slows it to a stop. Governing values are set as data
        attributes and can be tweaked in __init__.

        This is a touch sloppy due to half working with vectors, have not. Probably
        could be cleaned up.
        """

        # Current Velocity vector
        velocity = np.array([self.change_x, self.change_y])
        vhat = velocity
        vmag = np.linalg.norm(velocity)
        if vmag:
            vhat = velocity / vmag
        # Engine force
        vec_force_engine = np.array(
            [
                self.force_cur * np.cos(self.radians),
                self.force_cur * np.sin(self.radians),
            ]
        )
        # Friction force
        if vmag:
            vec_friction = -self.friction_current * vhat
        else:
            vec_friction = np.array([0, 0])
        # Total force
        vec_force = vec_force_engine + vec_friction
        # Acceleration
        vec_accel = vec_force / self.mass
        # Velocity
        velocity = velocity + vec_accel
        vmag = np.linalg.norm(velocity)
        if vmag > self.topspeed:
            velocity = velocity / vmag * self.topspeed
        self.change_x, self.change_y = velocity[0], velocity[1]

        # Engine torque
        tor_engine = self.torque_cur
        # Rotation friction
        if self.change_angle != 0:
            fric = -self.friction_current * self.change_angle / abs(self.change_angle)
        else:
            fric = 0
        self.change_angle += tor_engine + fric
        if abs(self.change_angle) > self.toprot:
            self.change_angle = self.change_angle / abs(self.change_angle) * self.toprot

    def update(self):
        super().update()

        self.force_cur = 0
        self.torque_cur = 0

        for key in self.cur_keys_pressed:
            if key == arcade.key.LEFT:
                self.turn_left()
            if key == arcade.key.RIGHT:
                self.turn_right()
            if key == arcade.key.DOWN:
                self.reverse(tanks.MOVEMENT_SPEED)
            if key == arcade.key.UP:
                self.forward(tanks.MOVEMENT_SPEED)

        self.update_movement()
        self.distance_traveled += self.change_x ** 2 + self.change_y ** 2

        # keep player on the screen
        if self.left < 0:
            self.change_x = 0
            self.left = 0
        elif self.right > tanks.WIDTH:
            self.change_x = 0
            self.right = tanks.WIDTH
        elif self.bottom < 0:
            self.change_y = 0
            self.bottom = 0
        elif self.top > tanks.HEIGHT:
            self.change_y = 0
            self.top = tanks.HEIGHT
