import random

import arcade
# import matplotlib.pyplot as plt
import numpy as np
import json

import Enemies
import Player

MOVEMENT_SPEED = 5
WIDTH = 1216
HEIGHT = 832

INSTRUCTIONS = 0
LEVEL_ONE = 2
LEVEL_TWO = 3
LEVEL_THREE = 4
GAME_OVER = 100
YOU_WIN = 101

INSTRUCTION_FONT = "kenney_pixel-webfont.ttf"


class Game(arcade.Window):
    def __init__(self, width, height, title):

        super().__init__(width, height, title)

        arcade.set_background_color(color=arcade.color.PINK_LACE)

        # load the different textures
        self.t_explosion = arcade.load_texture("Sprites/explosion3.png")
        self.t_tread = arcade.load_texture("Sprites/tracksSmall.png")
        self.t_shot = arcade.load_texture("Sprites/shotThin.png")
        self.t_hit = arcade.load_texture("Sprites/tank_red.png")
        self.emitters = []
        with open("levels.json") as fh:
            self.level_data = json.load(fh)

        self.setup()
        # self.read_tmx()

        arcade.run()

    def setup(self):
        """
        Call to reset player_bullet_list, enemy_list, enemy_bullet_list, score, and shots
        """

        # start the game with instructions
        self.current_state = "instructions"
        self.current_level = 0

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

    def clean_screen(self):
        """
        Call to reset the basic screen elements in between levels.
        """
        self.player_bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.enemy_bullet_list = arcade.SpriteList()
        self.oil_list = arcade.SpriteList()
        self.obstacle_list = arcade.SpriteList()
        self.emitters = []


    def construct_level(self, number):
        """
        Constructs the necessary sprites for each level.
        """
        if number > len(self.level_data) - 1:
            return False

        level = self.level_data[number]
        self.clean_screen()
        self.read_tmx(level["background"])
        self.player = Player.Player(*level["player_pos"])
        for enemy in level.get("enemies", []):
            if enemy["type"] == "red":
                sprite = Enemies.RedEnemy()
            elif enemy["type"] == "green":
                sprite = Enemies.GreenEnemy()
            elif enemy["type"] == "sand":
                sprite = Enemies.SandEnemy()
            elif enemy["type"] == "wobble":
                sprite = Enemies.WobblerEnemy()
            else:
                sprite = Enemies.RedEnemy()
            sprite.center_x, sprite.center_y = enemy["pos"]
            sprite.angle = random.randint(0,360)
            self.enemy_list.append(sprite)
        for ob in level.get("obstacles", []):
            x,y = ob["pos"]
            self.obstacle_list.append(Obstacle(x,y))
        for slick in level.get("slicks", []):
            x,y = slick.get("pos", (None,None))
            self.oil_list.append(OilSpill(x,y))



    def read_tmx(self, mapname = "Default"):
        """
        Reads in the sprite information and location from the tmx file created by Tiled.
        """
        filename = f"Maps/{mapname}.tmx"
        background_layer_name = "Background"
        water_layer_name = "Water"

        this_map = arcade.tilemap.read_tmx(filename)
        self.background_list = arcade.tilemap.process_layer(this_map, background_layer_name)
        self.water_list = arcade.tilemap.process_layer(this_map, water_layer_name)

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
        if self.current_state == "instructions":
            self.instructions_screen()

        elif self.current_state == "running":
            self.background_list.draw()
            self.water_list.draw()
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

        elif self.current_state == "win":
            self.you_win()
        elif self.current_state == "lose":
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
        """ Handles code to be run every dt timestep. """
        if self.current_state == "running":
            # clean up emitters
            for e in self.emitters:
                e.update()
                if e.can_reap():
                    self.emitters.remove(e)
            self.player.update_friction(self.oil_list)
            if self.player.collides_with_list(self.water_list):
                self.player.set_water_state(True)
            else:
                self.player.set_water_state(False)
            self.player.update()
            # To draw treads, check distance traveled
            if self.player.get_distance_traveled() > 250:
                self.emitters.append(self.draw_treads())
                self.player.reset_distance()
            # Update bullet and enemy positions
            self.player_bullet_list.update()
            self.enemy_list.update()

            # check for shot enemies
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
                        self.score += enemy.get_point_value()
                    bullet.check_obstacle_collisions(self.obstacle_list)

            # check for struck player
            for bullet in self.enemy_bullet_list:
                if bullet.collides_with_sprite(self.player):
                    bullet.remove_from_sprite_lists()
                    self.lives -= 1
                    if self.lives == 0:
                        self.current_state = "lose"
                    else:
                        self.emitters.append(self.player_gets_hit())
                        self.lives_list.remove(self.lives_list[-1])
                bullet.check_obstacle_collisions(self.obstacle_list)

            # Check enemy firing status and collisions with player
            for i in self.enemy_list:
                # i.update()
                if i.will_fire():
                    self.enemy_bullet_list.append(i.fire())
                if i.collides_with_sprite(self.player) and self.lives == 0:
                    self.current_state = "lose"
                elif i.collides_with_sprite(self.player) and self.lives > 0:
                    self.lives -= 1
                    self.lives_list.remove(self.lives_list[-1])

            # Update obstacle status
            for obstacle in self.obstacle_list:
                obstacle.check_collisions(
                    self.player,
                    [self.player_bullet_list, self.enemy_bullet_list],
                    [self.enemy_list],
                )
            self.lives_list.update()
            self.enemy_bullet_list.update()

            # Cleanup offscreen sprites and effects
            for bullet in self.enemy_bullet_list:
                bullet.cleanup()
            for bullet in self.player_bullet_list:
                bullet.cleanup()
            for obstacle in self.obstacle_list:
                obstacle.cleanup(self.emitters)

            # check end of level status
            if len(self.enemy_list) == 0:
                self.current_level += 1
                if self.current_level > len(self.level_data) - 1:
                    self.you_win()
                    self.current_state = "win"
                else:
                    self.construct_level(self.current_level)


    def on_key_press(self, key, modifiers):
        """ Handles key press events. """
        if self.current_state == "instructions":
            self.setup()
            self.construct_level(self.current_level)
            self.current_state = "running"
        elif self.current_state == "lose":
            self.setup()
            self.construct_level(0)
            self.current_state = "running"
        else: # so we are in game
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
                self.shot += 1

        if key == arcade.key.Q:
            # close the window if 'Q' is pressed
            arcade.close_window()

    def on_mouse_press(self, x, y, button, modifiers):
        """ Handles mouse press events. """
        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.current_state == "lose":
                self.setup()
                self.construct_level(0)
                self.current_state = "running"
            elif self.current_state == "win":
                self.current_state = "instructions"

    def on_key_release(self, key, modifiers):
        """ Handles key release events. """
        # make it so they stop moving when you stop pressing the arrows
        if self.current_state == "running":
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
        """ Update bullet position, only within the screen. """
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
        """ 
        Checks if the bullet collides with any sprites in the given list
        and marks it to die if so.
        """
        if self.collides_with_list(obstacle_list):
            self.should_die = True

    def cleanup(self):
        """ Cleans up and removes the bullet. """
        if self.should_die:
            self.kill()
            return True
        return False


class OilSpill(arcade.Sprite):
    def __init__(self, x=None, y=None):
        """
        Creates an oilspill object. If x and y are given, a spill of a random
        size is placed at that location. If x and y are not given, both the spill
        size and position are determined randomly.
        """
        super().__init__("Sprites/oilSpill_large.png")
        self.scale = random.randint(1, 3)
        if x is None:
            self.center_x = random.randint(0, WIDTH)
        else:
            self.center_x = x
        if y is None:
            self.center_y = random.randint(0, HEIGHT)
        else:
            self.center_y = y


class Obstacle(arcade.Sprite):
    def __init__(self, x=None, y=None):
        """
        Creates an obstacle object. If x and y are given, the obstacle is placed at
        that location. Otherwise, the position is determined randomly.
        """
        super().__init__("Sprites/crateMetal.png")
        if x is None:
            self.center_x = random.randint(0, WIDTH)
        else:
            self.center_x = x
        if y is None:
            self.center_y = random.randint(0, HEIGHT)
        else:
            self.center_y = y
        self.health = 10
        self.should_die = False
        self.emitter = None
        self.break_sound = arcade.Sound("Sounds/box_break.mp3")

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
            self.break_sound.play(0.5)
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
