import random

import arcade
import matplotlib.pyplot as plt
import numpy as np

import Enemies
import Player

MOVEMENT_SPEED = 5
WIDTH = 1200
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
        self.oil_list = arcade.SpriteList()
        self.obstacle_list = arcade.SpriteList()
        self.emitters = []

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

    def level_one(self):

        arcade.set_background_color(color=arcade.color.GREEN)
        self.player = Player.Player(WIDTH / 2, HEIGHT / 2)
        self.positions_of_enemies = [
            (100, 100),
            (100, HEIGHT - 100),
            (WIDTH - 100, 100),
            (WIDTH - 100, HEIGHT - 100),
        ]
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
        self.oil_list.append(OilSpill())
        self.obstacle_list.extend([Obstacle() for _ in range(3)])

    def level_two(self):
        arcade.set_background_color(arcade.color.BABY_BLUE)
        self.player = Player.Player(30, WIDTH / 2)
        self.enemy_list = arcade.SpriteList()

        # FOR LOOP TO PLACE THE TANKS IN RANDOM PLACES
        for i in range(1, 8):
            y_pos = random.randint(40, 760)
            enemy = Enemies.SandEnemy(2)
            enemy.center_x, enemy.center_y = i * 100, y_pos
            enemy.angle = random.randint(0, 360)
            # enemy.change_angle = 1
            self.enemy_list.append(enemy)
        self.oil_list.append(OilSpill())
        self.obstacle_list.extend([Obstacle() for _ in range(3)])

    def level_three(self):
        arcade.set_background_color(arcade.color.PASTEL_YELLOW)
        self.player = Player.Player(WIDTH / 2, HEIGHT / 2)
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
        self.oil_list.append(OilSpill())
        self.obstacle_list.extend([Obstacle() for _ in range(3)])

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
            self.oil_list.draw()
            self.obstacle_list.draw()
            self.player.draw()
            for e in self.emitters:
                e.draw()
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
            self.player.update_friction(self.oil_list)
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
                        new_obstacle = enemy.destroy()
                        self.obstacle_list.append(new_obstacle)
                        self.emitters.extend(
                            [
                                self.make_explosion(bullet.center_x, bullet.center_y),
                                new_obstacle.generate_smoke(),
                            ]
                        )
                        self.score += 1
                    bullet.check_obstacle_collisions(self.obstacle_list)

            for bullet in self.enemy_bullet_list:
                if bullet.collides_with_sprite(self.player):
                    bullet.remove_from_sprite_lists()
                    self.lives -= 1
                    if self.lives == 0:
                        self.current_state = GAME_OVER
                    else:
                        self.emitters.append(self.player_gets_hit())
                        self.lives_list.remove(self.lives_list[-1])
                bullet.check_obstacle_collisions(self.obstacle_list)

            for i in self.enemy_list:
                # i.update()
                if i.will_fire():
                    self.enemy_bullet_list.append(i.fire())
                if i.collides_with_sprite(self.player) and self.lives == 0:
                    self.current_state = GAME_OVER
                elif i.collides_with_sprite(self.player) and self.lives > 0:
                    self.lives -= 1
                    self.lives_list.remove(self.lives_list[-1])
            for obstacle in self.obstacle_list:
                obstacle.check_collisions(
                    self.player,
                    [self.player_bullet_list, self.enemy_bullet_list],
                    [self.enemy_list],
                )
            self.lives_list.update()
            self.enemy_bullet_list.update()

            for bullet in self.enemy_bullet_list:
                bullet.cleanup()
            for bullet in self.player_bullet_list:
                bullet.cleanup()
            for obstacle in self.obstacle_list:
                obstacle.cleanup(self.emitters)

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
            if key == arcade.key.LSHIFT or modifiers % 2:
                self.player.set_precise_mode(True)
            if key in [
                arcade.key.UP,
                arcade.key.DOWN,
                arcade.key.RIGHT,
                arcade.key.LEFT,
            ]:
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
            if arcade.key.LSHIFT:
                self.player.set_precise_mode(False)
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


class Bullets(arcade.Sprite):
    def __init__(self, png, scale=1):
        super().__init__(png, scale)
        self.should_die = False

    def update(self):
        super().update()
        # remove bullet if off screen
        if (
            self.center_x < 0
            or self.center_x > WIDTH
            or self.center_y < 0
            or self.center_y > HEIGHT
        ):
            self.should_die = True

    def check_obstacle_collisions(self, obstacle_list):
        if self.collides_with_list(obstacle_list):
            self.should_die = True

    def cleanup(self):
        if self.should_die:
            self.kill()
            return True
        return False


class OilSpill(arcade.Sprite):
    def __init__(self):
        super().__init__("Sprites/oilSpill_large.png")
        self.scale = random.randint(1, 3)
        self.center_x = random.randint(0, WIDTH)
        self.center_y = random.randint(0, HEIGHT)


class Obstacle(arcade.Sprite):
    def __init__(self):
        super().__init__("Sprites/crateMetal.png")
        self.center_x = random.randint(0, WIDTH)
        self.center_y = random.randint(0, HEIGHT)
        self.health = 10
        self.should_die = False
        self.emitter = None

    def check_collisions(self, player, health_list, instant_list):
        """
        Checks for and updates obstacle health based on what might have impacted it.
        Impacts with sprites in 'health_list' deduct one health from the total, while
        impacts with sprites in 'instant_list' kill the obstacle immediately.

        Inputs:
            player (Sprite): the player sprite
            health_list (List of SpriteLists): list of sprites that will slowly break obstacle
            instant_list (List of SpriteLists): list of sprites that will instantly break obstacle
        """

        for hlist in health_list:
            if self.collides_with_list(hlist):
                self.health -= 1
        for ilist in instant_list:
            if self.collides_with_list(ilist):
                self.should_die = True
        if self.collides_with_sprite(player):
            self.should_die = True
        if self.health <= 0:
            self.should_die = True

    def cleanup(self, emitter_list):
        if self.should_die:
            self.kill()
            if self.emitter:
                if self.emitter in emitter_list:
                    emitter_list.remove(self.emitter)
            return True
        return False


def main():
    """ Main method """
    Game(WIDTH, HEIGHT, "Tanks")


if __name__ == "__main__":
    main()
