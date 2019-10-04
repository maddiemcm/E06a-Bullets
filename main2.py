import sys, logging, os, random, math, open_color, arcade

#check to make sure we are running the right version of Python
version = (3,7)
assert sys.version_info >= version, "This script requires at least Python {0}.{1}".format(version[0],version[1])

#turn on logging, in case we have to leave ourselves debugging messages
logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MARGIN = 30
SCREEN_TITLE = "Bullet exercise"

NUM_ENEMIES = 5
STARTING_LOCATION = (400,100)
BULLET_DAMAGE = 20
ENEMY_HP = 100
HIT_SCORE = 10
KILL_SCORE = 100
PLAYER_HP = 500

class Bullet(arcade.Sprite):
    def __init__(self, position, velocity, damage):
        ''' 
        initializes the bullet
        Parameters: position: (x,y) tuple
            velocity: (dx, dy) tuple
            damage: int (or float)
        '''
        super().__init__("assets/bullet.png", 0.5)
        (self.center_x, self.center_y) = position
        (self.dx, self.dy) = velocity
        self.damage = damage
        #makes damage an attribute of the bullet
    def update(self):
        '''
        Moves the bullet
        '''
        self.center_x += self.dx
        self.center_y += self.dy


    
class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("assets/narwhal.png", 0.5)
        #super is whatever arcade.sprite needs to initialize itself, do it
        (self.center_x, self.center_y) = STARTING_LOCATION
        self.hp = PLAYER_HP

class Enemy(arcade.Sprite):
    def __init__(self, position):
        '''
        initializes a penguin enemy
        Parameter: position: (x,y) tuple
        '''
        super().__init__("assets/penguin.png", 0.5)
        self.hp = ENEMY_HP
        (self.center_x, self.center_y) = position


class Window(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.set_mouse_visible(True)
        arcade.set_background_color(open_color.blue_4)
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.bullet_enemy_list = arcade.SpriteList()
        self.player = Player()
        self.score = 0

    def setup(self):
        '''
        Set up enemies
        '''
        for i in range(NUM_ENEMIES):
            x = 120 * (i+1) + 40
            y = 500
            enemy = Enemy((x,y))
            self.enemy_list.append(enemy)            

    def update(self, delta_time):
        self.bullet_list.update()
        for e in self.enemy_list:
            
            damage = arcade.check_for_collision_with_list(e,self.bullet_list)
            for d in damage:
                e.hp = e.hp - d.damage
                d.kill()
                if e.hp < 0:
                    e.kill()
                    self.score = self.score + KILL_SCORE
                else:
                    self.score = self.score + HIT_SCORE

            if len(self.enemy_list) == 0:
            # == means comparison, = means assignment 
                arcade.draw_text("Congratulations!", 400, 300, open_color.white, 32)  

        self.bullet_enemy_list.update()
        for player:
            damage = arcade.check_for_collision_with_list(self.bullet_enemy_list, Player)
            for d in damage:
                d.kill()
                if PLAYER_HP < 0:
                    self.player.kill()
                    self.score = self.score + 0
                else:
                    self.score = self.score + 0                  

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(str(self.score), 20, SCREEN_HEIGHT - 40, open_color.white, 16)
        self.player.draw()
        self.bullet_list.draw()
        self.enemy_list.draw()
        self.bullet_enemy_list.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        '''
        The player moves left and right with the mouse
        '''
        self.player.center_x = x

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            x = self.player.center_x
            y = self.player.center_y + 15
            #center x, center y is the middle of the sprite
            bullet = Bullet((x,y),(0,10),BULLET_DAMAGE)
            # gives bullet position, velocity, bullet damage already defined as 10
            self.bullet_list.append(bullet)
            #fire a bullet
            #the pass statement is a placeholder. Remove line 97 when you add your code

def main():
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()




if __name__ == "__main__":
    main()