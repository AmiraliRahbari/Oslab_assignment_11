import arcade
import time

from random import randint, randrange

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900
SCREEN_TITLE = "Snake Game"

RECT_WIDTH = 30
RECT_HEIGHT = 30
RECT_COLOR = arcade.color.BLACK

MOVEMENT_SPEED = 15

BACKGROUND_COLOR = arcade.color.ALMOND

SHIT = 0
APPLE = 1
PEAR = 2

APPLE_COLOR = arcade.color.RED
PEAR_COLOR = arcade.color.GREEN
SHIT_COLOR = arcade.color.BROWN

SPRITE_SCALING = 0.5

UP = 0
DOWN = 1
RIGHT = 2
LEFT = 3

DIRECTION = UP


class Snake(arcade.Sprite):

    def __init__(self):
        super().__init__('snake.png', SPRITE_SCALING)

        self.direction = RIGHT
        self.width = RECT_WIDTH
        self.height = RECT_HEIGHT
        self.size = 1

    def update(self):
        self.center_x = self.center_x
        self.center_y = self.center_y


class Food(arcade.Sprite):

    def __init__(self):
        self.type = randrange(0, 3)
        self.food_scale = SPRITE_SCALING / 10

        if self.type == APPLE:
            super().__init__("apple.png", self.food_scale)
        elif self.type == PEAR:
            super().__init__("pear.png", self.food_scale)
        elif self.type == SHIT:
            super().__init__("shit.png", self.food_scale / 2)

        self.center_x = randint(30, SCREEN_WIDTH)
        self.center_y = randint(30, SCREEN_HEIGHT)

        self.width = RECT_WIDTH
        self.height = RECT_HEIGHT

    def update(self):
        self.center_x = self.center_x
        self.center_y = self.center_y


class MyGame(arcade.Window):

    def __init__(self, width, height, title):

        super().__init__(width, height, title)

        self.player_list = None

        self.food_queue = None

        self.player_sprite = None

        self.food_list = None

        self.food_sprite = None

        self.score = 0

        self.lost = False

        self.end = False

        self.target = None

        self.pre_direction = None

        self.score_board = arcade.draw_text("Score: 0",
                                            10,
                                            10,
                                            arcade.color.BLACK,
                                            20,
                                            width=SCREEN_WIDTH,
                                            align="center")

        arcade.set_background_color(BACKGROUND_COLOR)

    def setup(self):
        """ Set up the game and initialize the variables. """

        self.player_list = arcade.SpriteList()
        self.food_list = arcade.SpriteList()

        self.player_sprite = Snake()
        self.player_sprite.center_x = 30
        self.player_sprite.center_y = 30
        self.player_list.append(self.player_sprite)

        self.food_queue = arcade.SpriteList()

        for i in range(10):
            food_sprite = Food()
            food_sprite.center_x = randint(30, SCREEN_WIDTH - 30)
            food_sprite.center_y = randint(30, SCREEN_HEIGHT - 30)
            self.food_list.append(food_sprite)
            self.food_queue.append(food_sprite)

        self.target = self.food_queue.pop()

        self.pre_direction = RIGHT

    def on_draw(self):
        arcade.start_render()

        self.player_list.draw()
        self.food_list.draw()

        message = ""
        color = None

        if self.lost:
            self.score = 0
            message = "Game Over"
            color = arcade.color.RED
        elif self.end:
            message = "Game Finished"
            color = arcade.color.BLUE
        elif not self.lost and not self.end:
            message = "Score: {0}".format(self.score)
            color = arcade.color.BLACK

        arcade.draw_text(message,
                         20,
                         30,
                         color,
                         20,
                         width=SCREEN_WIDTH,
                         align="center")

    def on_update(self, delta_time):

        if not self.lost and not self.end:
            last_step_x = self.player_sprite.center_x
            last_step_y = self.player_sprite.center_y

            if not self.target is None and self.target.type == SHIT:
                self.target = None

            if self.food_queue and self.target is None:
                self.target = self.food_queue.pop()
                while True:
                    if self.target.type == APPLE:
                        break
                    elif self.food_queue:
                        self.target = self.food_queue.pop()
                    elif not self.food_queue:
                        self.end = True
            print("food type is")
            print(self.target.type)
            if not self.end:

                print("length is")
                print(len(self.food_queue))

                target_center_x = self.target.center_x
                target_center_y = self.target.center_y

                player_direction = self.player_list[0].direction

                # print(self.target.type)

                if target_center_x >= last_step_x and self.player_sprite.direction != LEFT:
                    self.player_sprite.direction = RIGHT
                elif target_center_x >= last_step_x and self.player_sprite.direction == LEFT:
                    if target_center_y >= last_step_y:
                        self.player_sprite.direction = UP
                    else:
                        self.player_sprite.direction = DOWN
                elif target_center_x <= last_step_x and self.player_sprite.direction != RIGHT:
                    self.player_sprite.direction = LEFT
                elif target_center_x <= last_step_x and self.player_sprite.direction == RIGHT:
                    if target_center_y >= last_step_y:
                        self.player_sprite.direction = UP
                    else:
                        self.player_sprite.direction = DOWN
                elif target_center_y >= last_step_y and self.player_sprite.direction != DOWN:
                    self.player_sprite.direction = UP
                elif target_center_y >= last_step_y and self.player_sprite.direction == DOWN:
                    if target_center_x >= last_step_x:
                        self.player_sprite.direction = RIGHT
                    else:
                        self.player_sprite.direction = LEFT
                elif target_center_y <= last_step_y and self.player_sprite.direction != UP:
                    if target_center_x >= last_step_x:
                        self.player_sprite.direction = RIGHT
                    else:
                        self.player_sprite.direction = LEFT

                if self.player_sprite.direction == RIGHT:
                    print("right")
                    self.player_sprite.center_x += MOVEMENT_SPEED
                elif self.player_sprite.direction == LEFT:
                    print("left")
                    self.player_sprite.center_x += -MOVEMENT_SPEED
                elif self.player_sprite.direction == UP:
                    print("up")
                    self.player_sprite.center_y += MOVEMENT_SPEED
                elif self.player_sprite.direction == DOWN:
                    print("down")
                    self.player_sprite.center_y += -MOVEMENT_SPEED

                for i in range(1, len(self.player_list)):
                    new_step_x = self.player_list[i].center_x
                    new_step_y = self.player_list[i].center_y

                    self.player_list[i].center_x = last_step_x
                    self.player_list[i].center_y = last_step_y

                    last_step_x = new_step_x
                    last_step_y = new_step_y

                # self_collision = arcade.check_for_collision_with_list(self.player_sprite,
                #                                                       self.player_list)
                #
                # for tail in self_collision:
                #     if tail is not self.player_list[1] and tail is not self.player_list[2]:
                #         self.lost = True

                if self.player_sprite.left < 0:
                    self.player_sprite.left = 0
                    self.lost = True
                elif self.player_sprite.right > SCREEN_WIDTH - 1:
                    self.player_sprite.right = SCREEN_WIDTH - 1
                    self.lost = True
                if self.player_sprite.bottom < 0:
                    self.player_sprite.bottom = 0
                    self.lost = True
                elif self.player_sprite.top > SCREEN_HEIGHT - 1:
                    self.player_sprite.top = SCREEN_HEIGHT - 1
                    self.lost = True

                colliding = arcade.check_for_collision_with_list(self.player_sprite, self.food_list)

                if colliding:
                    print("colliding")

                    for food in colliding:
                        print(food.type)
                        if food.type == APPLE:
                            tail_sprite = Snake()
                            tail_sprite.center_x = self.player_sprite.center_x - 100
                            tail_sprite.center_y = self.player_sprite.center_y - 100
                            self.player_list.append(tail_sprite)
                            self.score += 1
                            self.target = None

                        elif food.type == PEAR:
                            self.score += 2
                            self.target = None
                        elif food.type == SHIT:
                            self.score -= 1

                        if self.score <= 0:
                            self.lost = True

                        if len(self.food_list) == 0:
                            self.end = True

                        if len(self.food_queue) == 0:
                            self.end = True

                        self.food_list.remove(food)

                    food_sprite = Food()
                    if arcade.check_for_collision_with_list(food_sprite, self.food_list) \
                            or arcade.check_for_collision_with_list(food_sprite, self.player_list):
                        print("food collide")
                    else:
                        self.food_list.append(food_sprite)
                        self.food_queue.append(food_sprite)

                time.sleep(0.1)

                self.player_list.update()
                self.food_list.update()

    def on_key_press(self, key, modifiers):

        if key == arcade.key.UP:
            self.player_sprite.direction = UP
        elif key == arcade.key.DOWN:
            self.player_sprite.direction = DOWN
        elif key == arcade.key.LEFT:
            self.player_sprite.direction = LEFT
        elif key == arcade.key.RIGHT:
            self.player_sprite.direction = RIGHT

    def on_key_release(self, key, modifiers):

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0


def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
