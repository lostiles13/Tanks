import arcade
import numpy as np
import random

import tanks


class Enemy(arcade.Sprite):
    def __init__(self, texture):
        super().__init__(texture)
        # Set initial values
        self.speed = 0
        self.change_angle = 0
        self.cur_direction = np.array([np.cos(self.radians), np.sin(self.radians)])

        self.spawning = True
        self.alpha = 0

        self.fire_cooldown = 0
        self.point_value = 0

        self.sound_death = arcade.Sound("Sounds/explosion.mp3")

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
            self.fire_cooldown -= 1

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
            chance = 30
        return random.randint(0, 100) <= chance - self.fire_cooldown / 2

    def fire(self):
        """
        Creates and returns a Bullet object fired by this enemy.

        Returns:
            Bullet: one bullet object originating from the enemy and moving
                    in the proper direction.
        """
        self.fire_cooldown = 120 # 120 frame cooldown
        bullet = tanks.Bullets("Sprites/barrelRed_top.png", 0.5)
        bullet.angle = self.angle
        bullet.position = (self.center_x, self.center_y)
        direction = np.array([np.cos(bullet.radians), np.sin(bullet.radians)])
        bullet.velocity = 2 * tanks.MOVEMENT_SPEED * direction

        return bullet

    def destroy(self):
        self.sound_death.play(0.5)
        self.kill()
        return DeadEnemy(
            "Sprites/tank_dead1.png", self.center_x, self.center_y, self.angle
        )

    def get_point_value(self):
        return self.point_value


class RedEnemy(Enemy):
    """
    Enemy which just spins in circles and fires.
    """

    def __init__(self, angle_rate: float = 1.0):
        super().__init__("Sprites/tank_red.png")
        self.change_angle = angle_rate
        # Give chance to rotate opposite direction
        if random.randint(0, 1):
            self.change_angle *= -1
        self.point_value = 1


class GreenEnemy(Enemy):
    """
    Enemy which spins and occasionally flips rotation direction.
    """

    def __init__(self, angle_rate: float = 1.0):
        super().__init__("Sprites/tank_green.png")
        self.change_angle = angle_rate
        self.point_value = 2

    def update(self):
        super().update()
        if random.random() < 0.01:
            self.change_angle *= -1


class SandEnemy(Enemy):
    """
    Enemy which moves straight, bouncing off walls.
    """

    def __init__(self, speed: float=2):
        super().__init__("Sprites/tank_sand.png")
        self.speed = speed
        self.point_value = 3


class WobblerEnemy(GreenEnemy):
    """
    Combination of Green and Sand, which moves and
    occassionally flips rotating direction.
    """

    def __init__(self, angle_rate: float=1.0, speed: float=2.0):
        Enemy.__init__(self, "Sprites/tank_bigRed.png")
        self.change_angle = angle_rate
        self.speed = speed
        self.point_value = 4

    def destroy(self):
        self.sound_death.play(0.5)
        self.kill()
        return DeadEnemy(
            "Sprites/tank_dead2.png", self.center_x, self.center_y, self.angle
        )


class DeadEnemy(tanks.Obstacle):
    def __init__(self, texture, x, y, r):
        super().__init__()
        self.texture = arcade.load_texture(texture)
        self.center_x = x
        self.center_y = y
        self.angle = r
        self.health = 50
        self.should_die = False
        self.texture_smoke = arcade.make_soft_circle_texture(40, arcade.color.GRAY)
        self.emitter = None

    def generate_smoke(self):
        """
        Particle generator to create smoking wreck
        """
        offset = random.randint(-10, 10)
        smoke = arcade.Emitter(
            center_xy=(self.center_x + offset, self.center_y + offset),
            emit_controller=arcade.EmitMaintainCount(50),
            particle_factory=lambda emitter: arcade.FadeParticle(
                filename_or_texture=self.texture_smoke,
                change_xy=arcade.rand_vec_spread_deg(90, 20, 2),
                lifetime=random.random() * 2,
            ),
        )
        self.emitter = smoke
        return smoke
