from ext.Platformer.game_utils import Image, MotionSprite, Sprite, screen_rect
import ext.Core.operations as Opr
import pygame


class Player(MotionSprite):
    def __init__(self, x: int = 0, y: int = 0, w=None, h=None):
        super().__init__('Assets/Platformer/Player.png', x, y, w, h, [0,0], [1,.05])
        self.energy = 100

    def move(self):
        self.pos = tuple(self.pos[i] + self.vector[i] for i in range(2))
        self.r = [self.r[i] + self.vector[i % 2] for i in range(4)]
        self.updateBorders()

    def update(self, floor):
        move = pygame.key.get_pressed()
        self.vector = [
            -4 if move[pygame.K_LEFT] else 4 if move[pygame.K_RIGHT] else 0,
            -10 if move[pygame.K_UP] and self.energy > 0 else 0
          ]
        
        if move[pygame.K_UP] and self.energy > 0:
          self.energy -= 2
        Opr.render_text('Energy:' + str(self.energy),(100,50))
        # on regarde si le `player` touche le sol
        touch_floor_top = self.vector[1]<0 and self.borderCollide(0, floor)
        if touch_floor_top:
          self.vector[1] = touch_floor_top.r[3] - self.r[1]
        touch_floor_bottom = self.vector[1] >= 0 and self.borderCollide(2, floor)
        if touch_floor_bottom:
            self.vector[1] = touch_floor_bottom.r[1] - self.r[3] + 1
            if self.energy< 100:
              self.energy += 1
        elif not move[pygame.K_UP]:
            self.vector[1] += 10#gravity effect
        
        touch_floor_left = self.vector[0]<0 and self.borderCollide(3, floor)
        if touch_floor_left:
            self.vector[0] = touch_floor_left.r[2] - self.r[0]-2
            self.vector[1]-=7
        touch_floor_right = self.vector[0]>0 and self.borderCollide(1, floor)
        if touch_floor_right:
            self.vector[0] = touch_floor_right.r[0] - self.r[2]+2
            self.vector[1]-=7

        self.move()
        Image.relative = tuple(self.pos[i] + self.size[i] / 2 for i in range(2))
        self.display()
        self.updateVector()
        # print(self.pos)


#On definit le sol
class Floor(Sprite):
    def __init__(self, x, y):
        super().__init__("Assets/Platformer/Floor_(Test).png", x, y)


class Level_Flag(Sprite):
    def __init__(self, x, y):
        super().__init__("Assets/Platformer/Checkpoint.png", x, y)


class Lava(Sprite):
    def __init__(self, x, y):
        super().__init__("Assets/Platformer/Lava.png", x, y)


class Platform(Sprite):  #Moving platform
    def __init__(self, x, y, speed):
        super().__init__("Assets/Platformer/Floor_(Test).png", x, y)
        self.speed = speed  # Vitesse de deplacement

    def move(self):
        pass
