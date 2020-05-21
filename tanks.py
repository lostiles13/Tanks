import random

import arcade
import matplotlib.pyplot as plt
import numpy as np

import Enemies

MOVEMENT_SPEED = 5
WIDTH = 800
HEIGHT = 800

INSTRUCTIONS = 1
LEVEL_ONE = 2
LEVEL_TWO = 3
LEVEL_THREE = 4
GAME_OVER = 5
YOU_WIN = 6

INSTRUCTION_FONT = "kenney_pixel-webfont.ttf"


class Game(arcade.Window):
    def __init__(self, width, height, title):

        super().__init__(width, height, title)

        # start the game with instructions
        self.current_state = INSTRUCTIONS
        arcade.set_background_color(color=arcade.color.PINK_LACE)

        # load the different textures
        self.t_explosion = arcade.load_texture("Sprites/explosion3.png")
        self.t_tread = arcade.load_texture("Sprites/tracksSmall.png")
        self.t_shot = arcade.load_texture("Sprites/shotThin.png")
        self.t_hit = arcade.load_texture("Sprites/tank_red.png")
        self.emitters = []

        arcade.run()

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

        for i in range(0, self.lives):
            heart = arcade.Sprite("Sprites/tileRed_48.png", 0.3)
            heart.center_y = 750
            heart.center_x = i * 20 + 30
            self.lives_list.append(heart)

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

    # def playerZ(self, x, y):
    # """
    # Inputs:
    # x, y: integers describing where you want the player to start
    # Returns:
    # a Player object called self.player in the coordinates provided
    # """
    # self.player = Player("Sprites/tank_blue.png")
    # self.player.center_x, self.player.center_y = x, y
    # return self.player:q!

    def level_one(self):

        arcade.set_background_color(color=arcade.color.GREEN)
        self.player = Player(WIDTH / 2, HEIGHT / 2)
        self.positions_of_enemies = [(100, 100), (100, 700), (700, 100), (700, 700)]
        self.angles_of_enemies = [
            random.randint(90, 180),
            random.randint(0, 90),
            random.randint(180, 270),
            random.randint(270, 360),
        ]

        for i in range(0, len(self.positions_of_enemies)):
            enemy = Enemies.RedEnemy(1)  # call the class
            enemy.center_x, enemy.center_y = (
                self.positions_of_enemies[i][0],
                self.positions_of_enemies[i][1],
            )
            enemy.angle = self.angles_of_enemies[i]
            # enemy.change_angle = 1
            self.enemy_list.append(enemy)

    def level_two(self):
        arcade.set_background_color(arcade.color.BABY_BLUE)
        self.player = Player(30, WIDTH / 2)
        self.enemy_list = arcade.SpriteList()

        # FOR LOOP TO PLACE THE TANKS IN RANDOM PLACES
        for i in range(1, 8):
            y_pos = random.randint(40, 760)
            enemy = Enemies.SandEnemy(2)
            enemy.center_x, enemy.center_y = i * 100, y_pos
            enemy.angle = random.randint(0, 360)
            # enemy.change_angle = 1
            self.enemy_list.append(enemy)

    def level_three(self):
        arcade.set_background_color(arcade.color.PASTEL_YELLOW)
        self.player = Player(WIDTH / 2, HEIGHT / 2)
        self.enemy_list = arcade.SpriteList()
        self.positions_of_enemies3 = [
            (WIDTH / 4, HEIGHT / 4),
            (WIDTH / 4, 3 * HEIGHT / 4),
            (3 * WIDTH / 4, WIDTH / 4),
            (3 * WIDTH / 4, 3 * HEIGHT / 4),
        ]
        for i in self.positions_of_enemies3:
            enemy = Enemies.WobblerEnemy(2, 3)
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
            font_size=40,
            font_name="kenney_pixel-webfont.ttf",
            anchor_x="center",
        )
        arcade.draw_text(
            "Click to return to the instruction screen",
            WIDTH / 2,
            HEIGHT / 2 - 100,
            color=arcade.color.BLACK,
            font_size=20,
            anchor_x="center",
            font_name="kenney_pixel-webfont.ttf",
        )

    def instructions_screen(self):
        title = "Learn how to play"
        arcade.draw_text(
            title,
            WIDTH // 2,
            HEIGHT - 60,
            color=arcade.color.BLACK,
            font_size=50,
            font_name=INSTRUCTION_FONT,
            anchor_x="center",
        )
        # self.player = arcade.Sprite("tank_blue.png")
        # self.player.draw()
        instructions = [
            "Move your player using the arrow keys",
            "Shoot using the space bar",
            "Kill all enemies to pass",
            "Q to quit",
        ]
        for i in range(0, len(instructions)):
            arcade.draw_text(
                instructions[i],
                20,
                3 * HEIGHT / 4 - i * 50,
                color=arcade.color.BLACK,
                font_size=30,
                font_name="kenney_pixel-webfont.ttf",
            )

    def on_draw(self):
        arcade.start_render()
        if self.current_state == INSTRUCTIONS:
            self.instructions_screen()

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

            for i in range(0, self.lives):
                heart = arcade.Sprite("Sprites/tileRed_48.png", 0.3)
                heart.center_y = 750
                heart.center_x = i * 20 + 20
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
            # To draw treads, check distance traveled
            if self.player.get_distance_traveled() > 250:
                self.emitters.append(self.draw_treads())
                self.player.reset_distance()
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
                        self.emitters.append(self.player_gets_hit())
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
        if self.current_state == GAME_OVER:
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
        if (
            self.current_state == LEVEL_ONE
            or self.current_state == LEVEL_TWO
            or self.current_state == LEVEL_THREE
            or self.current_state == INSTRUCTIONS
        ):
            if key == arcade.key.UP:
                self.player.add_key(key)
            if key == arcade.key.DOWN:
                self.player.add_key(key)
            if key == arcade.key.RIGHT:
                self.player.add_key(key)
            if key == arcade.key.LEFT:
                self.player.add_key(key)

            if key == arcade.key.SPACE:
                self.player_bullet_list.append(self.player.fire())
                self.emitters.append(self.make_gun_fire_emitter())

                if (
                    self.current_state == LEVEL_ONE
                    or self.current_state == LEVEL_TWO
                    or self.current_state == LEVEL_THREE
                ):
                    self.shot += 1

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
            if key in [
                arcade.key.UP,
                arcade.key.DOWN,
                arcade.key.LEFT,
                arcade.key.RIGHT,
            ]:
                self.player.remove_key(key)

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
                angle=self.player.angle + 90,
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
        ) * np.cos(self.player.radians)
        front_y = self.player.center_y + (
            self.player.height / 2 + self.t_shot.height / 2 + 5
        ) * np.sin(self.player.radians)
        return arcade.Emitter(
            center_xy=(front_x, front_y),
            emit_controller=arcade.EmitBurst(1),
            particle_factory=lambda emitter: arcade.FadeParticle(
                filename_or_texture=self.t_shot,
                angle=self.player.angle + 90,  # correcting for texture orientation
                change_xy=(0, 0),
                lifetime=0.4,
                scale=1,
            ),
        )

    def player_gets_hit(self):
        """
        Function to turn the player red when it gets hit 
        Inputs: 
            None
        Outputs:
        """
        return arcade.Emitter(
            center_xy=(self.player.center_x, self.player.center_y),
            emit_controller=arcade.EmitBurst(1),
            particle_factory=lambda emitter: arcade.FadeParticle(
                filename_or_texture=self.t_hit,
                angle=self.player.angle,
                change_xy=(0, 0),
                lifetime=0.4,
                scale=1,
            ),
        )


class Player(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__("Sprites/tank_blue.png")
        self.texture_transform = arcade.Matrix3x3().rotate(90)
        self.width, self.height = self.height, self.width
        self.center_x = x
        self.center_y = y
        self.cur_keys_pressed = []
        self.turn_rate = 5
        self.distance_traveled = 0
        self.friction = 0.8

    def turn_left(self):
        """ Turn tank to the left """
        self.change_angle = self.turn_rate

    def turn_right(self):
        """ Turn tank to the right """
        self.change_angle = -self.turn_rate

    def forward(self, speed: float):
        """ 
        Set tank speed forward in facing direction

        Input:
            speed (float): speed to move forward
        """
        self.change_x = speed * np.cos(self.radians)
        self.change_y = speed * np.sin(self.radians)

    def reverse(self, speed: float):
        """
        Set tank moving backwards at some speed

        Input:
            speed (float): speed to move backwards
        """
        self.forward(-speed)

    def fire(self):
        """
        Fire a bullet object. Creates a new bullet object with
        the necessary parameters and returns it.

        Output:
            (Bullet): a new bullet object
        """
        bullet = Bullets("Sprites/specialBarrel6.png")
        bullet.texture_transform = arcade.Matrix3x3().rotate(-90)
        bullet.width, bullet.height = bullet.height, bullet.width
        bullet.center_x = self.center_x
        bullet.center_y = self.center_y
        bullet.radians = self.radians
        bullet.change_x = 2 * MOVEMENT_SPEED * np.cos(self.radians)
        bullet.change_y = 2 * MOVEMENT_SPEED * np.sin(self.radians)

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

    def update(self):
        super().update()

        for key in self.cur_keys_pressed:
            if key == arcade.key.LEFT:
                self.turn_left()
            if key == arcade.key.RIGHT:
                self.turn_right()
            if key == arcade.key.DOWN:
                self.reverse(MOVEMENT_SPEED)
            if key == arcade.key.UP:
                self.forward(MOVEMENT_SPEED)

        self.friction = 0.9
        if (
            arcade.key.UP not in self.cur_keys_pressed
            and arcade.key.DOWN not in self.cur_keys_pressed
        ):
            # rounds down to nearest tenth
            self.change_x = int(self.change_x * self.friction * 10) / 10
            self.change_y = int(self.change_y * self.friction * 10) / 10
        if (
            arcade.key.RIGHT not in self.cur_keys_pressed
            and arcade.key.LEFT not in self.cur_keys_pressed
        ):
            self.change_angle = int(self.change_angle * self.friction ** 2 * 100) / 100

        self.distance_traveled += self.change_x ** 2 + self.change_y ** 2

        # keep player on the screen
        if self.left < 0 or self.right > WIDTH:
            self.change_x = 0
        if self.bottom < 0 or self.top > HEIGHT:
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


def main():
    """ Main method """
    Game(WIDTH, HEIGHT, "Tanks")


if __name__ == "__main__":
    main()
