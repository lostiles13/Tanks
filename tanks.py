import arcade
import numpy as np
import matplotlib.pyplot as plt
import random

MOVEMENT_SPEED = 5
WIDTH = 800
HEIGHT = 800

INSTRUCTIONS = 1
LEVEL_ONE = 2
LEVEL_TWO = 3
LEVEL_THREE = 4
GAME_OVER = 5
YOU_WIN = 6

# game class does tank chooser and then runs the game
# second screen, game runner, that is what has a good tank and bad tanks, run the game


class Game(arcade.Window):
    def __init__(self, width, height, title):

        super().__init__(width, height, title)

        # start the game with instructions
        self.current_state = INSTRUCTIONS
        arcade.set_background_color(color=arcade.color.PINK_LACE)

        self.t_explosion = arcade.load_texture("explosion3.png")
        self.t_tread = arcade.load_texture("tracksSmall.png")
        self.t_shot = arcade.load_texture("shotThin.png")
        self.emitters = []
        arcade.run()

    # define a setup so we can restart game without going back to the instruction screen
    def setup(self):
        """
        Call to reset player_bullet_list, enemy_list, enemy_bullet_list, score, and shots
        """

        self.player_bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.enemy_bullet_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.lives_list = arcade.SpriteList()

        # initialize score
        self.score = 0
        self.shot = 0
        self.coins = 0 
        self.lives = 3

        for i in range(0,self.lives):
            heart = arcade.Sprite("tileRed_48.png",.3)
            heart.center_y = 750
            heart.center_x = i *20 +20
            self.lives_list.append(heart) 

        # set background color

    def graph(self):
        """
        Graph that will be displayed when you win of your shots made vs. shots missed
        """
        f = plt.figure()
        ax1 = f.add_subplot(111)
        data = [self.score, self.shot - self.score]
        ax1.pie(data, labels=["shots hit", "shots missed"])
        ax1.set_title(f"Your final score was {self.score}")
        plt.show()

    def playerZ(self, x, y):
        """
        Inputs: 
            x, y: integers describing where you want the player to start
        Returns: 
            a Player object called self.player in the coordinates provided
        """
        self.player = Player("tank_blue.png")
        self.player.center_x, self.player.center_y = x, y
        return self.player

    def level_one(self):

        arcade.set_background_color(color=arcade.color.GREEN)
        self.player = self.playerZ(WIDTH / 2, HEIGHT / 2)
        self.positions_of_enemies = [(100, 100), (100, 700), (700, 100), (700, 700)]
        self.angles_of_enemies = [
            random.randint(90, 180),
            random.randint(0, 90),
            random.randint(180, 270),
            random.randint(270, 360),
        ]

        for i in range(0, len(self.positions_of_enemies)):
            enemy = RedEnemy(1)  # call the class
            enemy.center_x, enemy.center_y = (
                self.positions_of_enemies[i][0],
                self.positions_of_enemies[i][1],
            )
            enemy.angle = self.angles_of_enemies[i]
            # enemy.change_angle = 1
            self.enemy_list.append(enemy)
    
    def level_two(self):
        arcade.set_background_color(arcade.color.BABY_BLUE)
        self.player = self.playerZ(20, WIDTH / 2)
        self.enemy_list = arcade.SpriteList()

        # FOR LOOP TO PLACE THE TANKS IN RANDOM PLACES
        for i in range(1, 8):
            y_pos = random.randint(40, 760)
            enemy = SandEnemy(2)
            enemy.center_x, enemy.center_y = i * 100, y_pos
            enemy.angle = random.randint(0, 360)
            # enemy.change_angle = 1
            self.enemy_list.append(enemy)
    
    def level_three(self):
        arcade.set_background_color(arcade.color.PASTEL_YELLOW)
        self.player = self.playerZ(WIDTH / 2, HEIGHT / 2)
        self.enemy_list = arcade.SpriteList()
        self.positions_of_enemies3 = [
            (WIDTH / 4, HEIGHT / 4),
            (WIDTH / 4, 3 * HEIGHT / 4),
            (3 * WIDTH / 4, WIDTH / 4),
            (3 * WIDTH / 4, 3 * HEIGHT / 4),
        ]
        for i in self.positions_of_enemies3:
            enemy = WobblerEnemy(2, 3)
            enemy.center_x, enemy.center_y = i[0], i[1]
            enemy.angle = random.randint(0, 360)
            self.enemy_list.append(enemy)
        # movements = [-3, -1, 0, 1, 3]
        # for i in self.enemy_list:
        #     i.change_x = movements[random.randint(0, 4)]
        #     i.change_y = movements[random.randint(0, 4)]

    def you_win(self):
        arcade.set_background_color(arcade.color.LAVENDER)
        arcade.draw_text(
            "YOU ARE A WINNER CONGRATS!!!",
            WIDTH / 2,
            HEIGHT / 2,
            color=arcade.color.BLACK,
            font_size=30,
            anchor_x="center",
        )
        arcade.draw_text(
            "Click to return to the instruction screen",
            WIDTH / 2,
            HEIGHT / 2 - 100,
            color=arcade.color.BLACK,
            font_size=20,
            anchor_x="center",
        )


    def on_draw(self):
        arcade.start_render()
        if self.current_state == INSTRUCTIONS:
            instructions = [
                "Move your character using the arrow keys",
                "Avoid getting shot",
                "Shoot using the space bar",
                "Kill all enemies to pass",
                " To practice level 1: push A, 2: B, 3: C",
                "otherwise push d"
            ]
            for i in range(0, len(instructions)):
                arcade.draw_text(
                    instructions[i],
                    WIDTH / 2,
                    3 * HEIGHT / 4 - i * 50,
                    color=arcade.color.BLACK,
                    font_size=20,
                    anchor_x="center",
                )
            arcade.draw_text(
                "Or q to quit",
                WIDTH / 2,
                HEIGHT / 2 - 200,
                arcade.color.BLACK,
                15,
                anchor_x="center",
            )

        elif (
            self.current_state == LEVEL_ONE
            or self.current_state == LEVEL_TWO
            or self.current_state == LEVEL_THREE
        ):
            for e in self.emitters:
                e.draw()
            self.player.draw()
            self.enemy_list.draw()
            ## Only here to help visualize facing
            # for e in self.enemy_list:
            #     e.draw_direction(40, arcade.color.RED)
            self.player_bullet_list.draw()
            self.enemy_bullet_list.draw()
            self.lives_list = arcade.SpriteList()

            for i in range(0,self.lives):
                heart = arcade.Sprite("tileRed_48.png",.3)
                heart.center_y = 750
                heart.center_x = i *20 +20
                self.lives_list.append(heart) 

            self.lives_list.draw()
            self.coin_list.draw()
            output = f"Score: {self.score}"
            arcade.draw_text(
                output,
                WIDTH / 2,
                HEIGHT - 30,
                arcade.color.BLACK,
                14,
                anchor_x="center",
            )

        elif self.current_state == YOU_WIN:
            self.you_win()
        elif self.current_state == GAME_OVER:
            arcade.set_background_color(color=arcade.color.ORANGE)
            output = f"Your score was {self.score}"
            output2 = f"Click to play again"
            output3 = f"Or click A, B, C to play levels 1, 2, 3 respectively"
            arcade.draw_text(
                output,
                WIDTH / 2,
                HEIGHT / 2 + 100,
                arcade.color.BLACK,
                20,
                anchor_x="center",
            )
            arcade.draw_text(
                output2,
                WIDTH / 2,
                HEIGHT / 2 - 100,
                arcade.color.BLACK,
                15,
                anchor_x="center",
            )
            arcade.draw_text(
                output3,
                WIDTH / 2,
                HEIGHT / 2 - 200,
                arcade.color.BLACK,
                15,
                anchor_x="center",
            )
            arcade.draw_text(
                "Or q to quit",
                WIDTH / 2,
                HEIGHT / 2 - 300,
                arcade.color.BLACK,
                15,
                anchor_x="center",
            )

    def on_update(self, dt):
        if (
            self.current_state == LEVEL_ONE
            or self.current_state == LEVEL_TWO
            or self.current_state == LEVEL_THREE
        ):
            for e in self.emitters:
                e.update()
                if e.can_reap():
                    self.emitters.remove(e)
            self.player.update()
            self.player_bullet_list.update()
            self.enemy_list.update()

            for enemy in self.enemy_list:
                for bullet in self.player_bullet_list:
                    if bullet.collides_with_sprite(enemy):
                        bullet.remove_from_sprite_lists()
                        enemy.remove_from_sprite_lists()
                        self.emitters.append(
                            self.make_explosion(bullet.center_x, bullet.center_y)
                        )
                        self.score += 1

            for bullet in self.enemy_bullet_list:
                if bullet.collides_with_sprite(self.player):
                    bullet.remove_from_sprite_lists()
                    self.lives -= 1
                    if self.lives == 0:
                        self.current_state = GAME_OVER
                    else: 
                        self.lives_list.remove(self.lives_list[-1])

            for i in self.enemy_list:
                # i.update()
                if i.will_fire():
                    self.enemy_bullet_list.append(i.fire())
                if i.collides_with_sprite(self.player) and self.lives == 0:
                    self.current_state = GAME_OVER
                elif i.collides_with_sprite(self.player) and self.lives > 0: 
                    self.lives -= 1
                    self.lives_list.remove(self.lives_list[-1])

            self.lives_list.update()
            self.enemy_bullet_list.update()

        if self.current_state == LEVEL_ONE:

            if len(self.enemy_list) == 0:
                self.level_two()
                self.current_state = LEVEL_TWO

        if self.current_state == LEVEL_TWO:

            if len(self.enemy_list) == 0:
                self.level_three()
                self.current_state = LEVEL_THREE

        if self.current_state == LEVEL_THREE:
            for enemy in self.enemy_list:
                if enemy.center_x < 40:
                    enemy.change_x = 3
                elif enemy.center_x > WIDTH - 40:
                    enemy.change_x = -3

                elif enemy.center_y < 40:
                    enemy.change_y = 3
                elif enemy.center_y > HEIGHT - 40:

                    enemy.change_y = -3

            if len(self.enemy_list) == 0:
                self.you_win()
                self.graph()
                self.current_state = YOU_WIN

    def on_key_press(self, key, modifiers):
        if self.current_state == INSTRUCTIONS:
            if key == arcade.key.D:
                self.setup()
                self.level_one()
                self.current_state = LEVEL_ONE
            elif key == arcade.key.A:
                self.setup()
                self.level_one()
                self.current_state = LEVEL_ONE
            elif key == arcade.key.B:
                self.setup()
                self.level_two()
                self.current_state = LEVEL_TWO
            elif key == arcade.key.C:
                self.setup()
                self.level_three()
                self.current_state = LEVEL_THREE
            if key == arcade.key.Q:
                # close the window if 'Q' is pressed
                arcade.close_window()
        elif self.current_state == GAME_OVER:
            if key == arcade.key.A:
                self.setup()
                self.level_one()
                self.current_state = LEVEL_ONE
            elif key == arcade.key.B:
                self.setup()
                self.level_two()
                self.current_state = LEVEL_TWO
            elif key == arcade.key.C:
                self.setup()
                self.level_three()
                self.current_state = LEVEL_THREE
        else:
            # if self.current_state == LEVEL_ONE or self.current_state == LEVEL_TWO or self.current_state == LEVEL_THREE:
            if key == arcade.key.UP:
                self.player.change_y = MOVEMENT_SPEED
                self.player.angle = -180
                self.emitters.append(self.draw_treads())
            if key == arcade.key.DOWN:
                self.player.change_y = -MOVEMENT_SPEED
                self.player.angle = 0
                self.emitters.append(self.draw_treads())
            if key == arcade.key.RIGHT:
                self.player.change_x = MOVEMENT_SPEED
                self.player.angle = 90
                self.emitters.append(self.draw_treads())
            if key == arcade.key.LEFT:
                self.player.change_x = -MOVEMENT_SPEED
                self.player.angle = -90
                self.emitters.append(self.draw_treads())

            if key == arcade.key.SPACE:
                self.shot += 1
                bullet = Bullets("specialBarrel6.png")
                self.emitters.append(self.make_gun_fire_emitter())
                bullet.center_x, bullet.center_y = (
                    self.player.center_x,
                    self.player.center_y,
                )
                bullet.angle = self.player.angle + 180

                if self.player.angle == 0:
                    bullet.change_y = -MOVEMENT_SPEED * 2
                elif self.player.angle == 90:
                    bullet.change_x = MOVEMENT_SPEED * 2
                elif self.player.angle == -90:
                    bullet.change_x = -MOVEMENT_SPEED * 2
                elif self.player.angle == -180:
                    bullet.change_y = MOVEMENT_SPEED * 2
                self.player_bullet_list.append(bullet)

        if key == arcade.key.Q:
            # close the window if 'Q' is pressed
            arcade.close_window()

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.current_state == GAME_OVER:
                self.setup()
                self.level_one()
                self.current_state = LEVEL_ONE
            elif self.current_state == YOU_WIN:
                self.current_state = INSTRUCTIONS

    def on_key_release(self, key, modifiers):
        # make it so they stop moving when you stop pressing the arrows
        if (
            self.current_state == LEVEL_ONE
            or self.current_state == LEVEL_TWO
            or self.current_state == LEVEL_THREE
        ):
            if key == arcade.key.UP or key == arcade.key.DOWN:
                self.player.change_y = 0
            if key == arcade.key.RIGHT or key == arcade.key.LEFT:
                self.player.change_x = 0

    def make_explosion(self, x, y):
        """
        Function to create an explosion particle effect for when a bullet
        strikes a tank. Will return the emitter object which should be appended
        to the emitter list.

        Inputs:
            x (float): the center x position of the explosion
            y (float): the center y position of the explosion
        Outputs:
            (emitter obj): explosion particles
        """
        return arcade.Emitter(
            center_xy=(x, y),
            emit_controller=arcade.EmitBurst(30),
            particle_factory=lambda emitter: arcade.FadeParticle(
                filename_or_texture=self.t_explosion,
                change_xy=arcade.rand_in_circle((0, 0), 2),
                change_angle=10,
                lifetime=0.4,
                scale=0.75,
            ),
        )

    def draw_treads(self):
        """
        Function to create treads particle effect for when the tank moves.
        Currently is set to match the location and orientation of the tank.
        Inputs:
            None
        Outputs:
            (emitter obj): tank tread particle
        """
        return arcade.Emitter(
            center_xy=(self.player.center_x, self.player.center_y),
            emit_controller=arcade.EmitBurst(1),
            particle_factory=lambda emitter: arcade.FadeParticle(
                filename_or_texture=self.t_tread,
                angle=self.player.angle,
                change_xy=(0, 0),
                lifetime=0.4,
                scale=0.5,
            ),
        )

    def make_gun_fire_emitter(self):
        """
        Function to create a firing particle effect for when the tank fires.
        Currently is set to match the location and orientation of the tank.
        If the tank is moving rapidly, it looks a little silly at the moment,
        but to fix that I'd have to update the emitter position on update and
        I'm not sure that is worth it.

        Inputs:
            None
        Outputs:
            (emitter obj): tank tread particle
        """
        front_x = self.player.center_x + (
            self.player.width / 2 + self.t_shot.height / 2 + 5
        ) * np.cos(self.player.radians - np.pi / 2)
        front_y = self.player.center_y + (
            self.player.height / 2 + self.t_shot.height / 2 + 5
        ) * np.sin(self.player.radians - np.pi / 2)
        return arcade.Emitter(
            center_xy=(front_x, front_y),
            emit_controller=arcade.EmitBurst(1),
            particle_factory=lambda emitter: arcade.FadeParticle(
                filename_or_texture=self.t_shot,
                angle=self.player.angle,
                change_xy=(0, 0),
                lifetime=0.4,
                scale=1,
            ),
        )


class Player(arcade.Sprite):
    def update(self):
        super().update()

        # keep player on the screen
        if self.center_x < 10 or self.center_x > WIDTH - 10:
            self.change_x = 0
        if self.center_y < 10 or self.center_y > HEIGHT - 10:
            self.change_y = 0


class Bullets(arcade.Sprite):
    
    def update(self):
        super().update()
        # remove bullet if off screen
        if (
            self.center_x < 0
            or self.center_x > WIDTH
            or self.center_y < 0
            or self.center_y > HEIGHT
        ):
            self.remove_from_sprite_lists()


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
        super().update()

        # Bounce top and bottom
        if self.center_y > HEIGHT or self.center_y < 0:
            # Reset to wall edge
            if abs(self.center_y - HEIGHT) < abs(self.center_y - 0):
                self.center_y = HEIGHT
            else:
                self.center_y = 0
            # mirror angle
            self.change_y *= -1
            # Update sprite facing direction
            self.radians = np.arctan2(self.change_y, self.change_x)

        # Bounce left and right
        if self.center_x > WIDTH or self.center_x < 0:
            # Reset to wall edge
            if abs(self.center_x - WIDTH) < abs(self.center_x - 0):
                self.center_x = WIDTH
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

        # The old 90 degree rotate code in case of future reference
        # make the enemies move
        # # bottom left corner
        # if self.center_x < WIDTH / 2 and self.center_y < HEIGHT / 2:
        #     if self.angle > 180 or self.angle < 90:
        #         self.change_angle *= -1
        # # bottom right corner
        # elif self.center_x > WIDTH / 2 and self.center_y < HEIGHT / 2:
        #     if self.angle < 180 or self.angle > 270:
        #         self.change_angle *= -1
        # # top right corner
        # elif self.center_x > WIDTH / 2 and self.center_y > HEIGHT / 2:
        #     if self.angle < 270 or self.angle > 360:
        #         self.change_angle *= -1
        # # top left corner
        # elif self.center_x < WIDTH / 2 and self.center_y > HEIGHT / 2:
        #     if self.angle < 0 or self.angle > 90:
        #         self.change_angle *= -1

    def will_fire(self):
        """
        Determines whether an enemy will fire during a frame. 
        Higher values make it much more likely.

        Returns:
            boolean: if a projectile will be fired
        """
        chance = 2
        return random.randint(0, 100) <= chance

    def fire(self):
        """
        Creates and returns a Bullet object fired by this enemy.

        Returns:
            Bullet: one bullet object originating from the enemy and moving
                    in the proper direction.
        """
        bullet = Bullets("barrelRed_top.png", 0.5)
        bullet.angle = self.angle
        bullet.position = (self.center_x, self.center_y)
        direction = np.array([np.cos(bullet.radians), np.sin(bullet.radians)])
        bullet.velocity = 2 * MOVEMENT_SPEED * direction

        return bullet


class RedEnemy(Enemy):
    """
    Enemy which just spins in circles and fires.
    """

    def __init__(self, angle_rate: float):
        super().__init__("tank_red.png")
        self.change_angle = angle_rate


class GreenEnemy(Enemy):
    """
    Enemy which spins and occasionally flips rotation direction.
    """

    def __init__(self, angle_rate: float):
        super().__init__("tank_green.png")
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
        super().__init__("tank_sand.png")
        self.speed = 2


class WobblerEnemy(GreenEnemy):
    """
    Combination of Green and Sand, which moves and
    occassionally flips rotating direction.
    """

    def __init__(self, angle_rate: float, speed: float):
        Enemy.__init__(self, "tank_bigRed.png")
        self.change_angle = angle_rate
        self.speed = speed


def main():
    """ Main method """
    Game(WIDTH, HEIGHT, "Tanks")


if __name__ == "__main__":
    main()
