# -*- coding: utf-8 -*-
import pygame
import time
import threading
import random
import sys

pygame.init()

class Enemy:
    def __init__(self, x, y) :
      self.x = x
      self.y = y
      self.image = pygame.image.load('src/images4.png')
      self.image = pygame.transform.scale(self.image, (20, 20))
      self.direction = random.choice(['up', 'down', 'left', 'right'])
      self.enemy_rect = pygame.Rect(self.x, self.y, 20, 20)

    def update(self, counter):
      if map_data[self.y // 20][self.x // 20] == '1' or self.x < 0 or self.x > map_width * 20 or self.y < 0 or self.y > map_height * 20:
        self.direction = random.choice(['up', 'down', 'left', 'right'])
    # Si l'ennemi n'est pas sur un mur, mettre à jour sa direction tous les n tours de boucle
      else:
       if counter % 50 == 0:
        if self.direction == 'right' and (map_data[self.y // 20][(self.x + 21) // 20] == '1' or map_data[(self.y + 20) // 20][(self.x + 21) // 20] == '1'):
	        self.direction = random.choice(['up', 'down', 'left'])
        elif self.direction == 'left' and (map_data[self.y // 20][(self.x - 1) // 20] == '1' or map_data[(self.y + 19) // 20][(self.x - 1) // 20] == '1'):
	        self.direction = random.choice(['up', 'down', 'right'])
        elif self.direction == 'up' and (map_data[(self.y - 1) // 20][self.x // 20] == '1' or map_data[(self.y - 1) // 20][(self.x + 20) // 20] == '1'):
	        self.direction = random.choice(['down', 'left', 'right'])
        elif self.direction == 'down' and (map_data[(self.y + 21) // 20][self.x // 20] == '1'or map_data[(self.y + 21) // 20][(self.x + 20) // 20] == '1'):
	        self.direction = random.choice(['up', 'left', 'right'])

      old_self_x = self.x
      old_self_y = self.y
      if self.direction == 'right' :
        self.x += 1
      elif self.direction == 'left' :
        self.x -= 1
      elif self.direction == 'up' :
        self.y -= 1
      elif self.direction == 'down' :
        self.y += 1
      self.enemy_rect = pygame.Rect(self.x, self.y, 20, 20)
      for y, row in enumerate(map_data):
        for x, cell in enumerate(row):
          if cell == '1':
            wall_rect = pygame.Rect(x * 20, y * 20, 20, 20)
            if self.enemy_rect.colliderect(wall_rect) :
	            self.x = old_self_x
	            self.y = old_self_y
	            self.enemy_rect = pygame.Rect(self.x, self.y, 20, 20)
          elif cell == '2':
            food_rect = pygame.Rect(x * 20 + 5, y * 20 + 5, 10, 10)
            if self.enemy_rect.colliderect(food_rect):
              map_data[y][x] = '0'

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

def create_map(filename):
  with open(filename, 'r') as f:
    lines = f.readlines()
  map_data = []
  pacman_x, pacman_y = None, None
  for y, line in enumerate(lines):
    row = []
    for x, cell in enumerate(line.strip()):
      if cell == 'x':
        pacman_x, pacman_y = x, y
      row.append(cell)
    map_data.append(row)
  return map_data, len(map_data[0]), len(map_data), pacman_x * 20, pacman_y * 20

map_data, map_width, map_height, pacman_x, pacman_y = create_map('src/map.txt')
screen = pygame.display.set_mode((map_width * 20, map_height * 20))
pygame.display.set_caption('Pac-Man')

pacman_image = pygame.image.load('src/images.png')
pacman_image = pygame.transform.scale(pacman_image, (20, 20))
wall_image = pygame.image.load('src/images2.png')
wall_image = pygame.transform.scale(wall_image, (20, 20))
food_image = pygame.image.load('src/images3.png')
food_image = pygame.transform.scale(food_image, (20, 20))
feed = 0
font = pygame.font.Font(None, 32)
text = font.render("{}".format(feed), True, (255, 100, 0))
counter = 0
enough_feed = 10
enemies = []
for y, row in enumerate(map_data):
  for x, cell in enumerate(row):
    if cell == 'y' :
      enemies.append(Enemy(x * 20, y * 20))
stop = False

def periodic_task():
  global stop
  while not stop :
    time.sleep(1)
    if (random.randint(0, 9)) == 5 :
     x = random.randint(0, map_width-1)
     y = random.randint(0, map_height-1)
     if map_data[y][x] == '0' :
       map_data[y][x] = '2' 

thread_food = threading.Thread(target=periodic_task)
thread_food.start()

def draw_pacman():
  screen.blit(pacman_image, (pacman_x, pacman_y))
while True:
  for y, row in enumerate(map_data):
    for x, cell in enumerate(row):
      if cell == '1':
        screen.blit(wall_image, (x * 20, y * 20))
      elif cell == '2':
        pygame.draw.rect(screen, (255, 255, 255), (x * 20, y * 20, 20, 20))  # Passage blanc
        screen.blit(food_image, (x * 20, y * 20))
      else :
        pygame.draw.rect(screen, (255, 255, 255), (x * 20, y * 20, 20, 20))  # Passage blanc
  for enemy in enemies :
    enemy.update(counter)
    enemy.draw()

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      stop = True
      thread_food.join()
      pygame.quit()
      sys.exit()

  keys = pygame.key.get_pressed()
  if keys[pygame.K_m]:
    text = font.render("Beef :{}/{}".format(feed, enough_feed), True, (255, 100, 0))
    text_rect = text.get_rect()
    rect_back = pygame.Rect(5, 5, 300, 50)
    text_x = rect_back.centerx - text_rect.width // 2
    text_y = rect_back.centery - text_rect.height // 2
    pygame.draw.rect(screen, (255, 255, 255), rect_back)
    pygame.draw.rect(screen, (0, 0, 0), rect_back, 2)
    pygame.draw.line(screen, (0, 0, 0), (rect_back.left - 5, rect_back.top - 5), (rect_back.right + 5, rect_back.top - 5), 2)
    pygame.draw.line(screen, (0, 0, 0), (rect_back.left - 5, rect_back.bottom + 5), (rect_back.right + 5, rect_back.bottom + 5), 2)
    screen.blit(text, (text_x, text_y))
  old_pacman_y = pacman_y
  old_pacman_x = pacman_x
  direction = None
  if keys[pygame.K_RIGHT]:
    direction = 'right'
  elif keys[pygame.K_LEFT]:
    direction = 'left'
  elif keys[pygame.K_UP]:
    direction = 'up'
  elif keys[pygame.K_DOWN]:
    direction = 'down'
  if direction != None :
    if direction == 'right' :
      pacman_x += 1
    elif direction == 'left' :
      pacman_x -= 1
    elif direction == 'up' :
      pacman_y -= 1
    elif direction == 'down' :
      pacman_y += 1
  pacman_rect = pygame.Rect(pacman_x, pacman_y, 20, 20)
  if feed >= enough_feed :
   print("T'as gagnés mon GADJO")
   stop = True
   thread_food.join()
   pygame.quit()
   sys.exit()
  for enemy in enemies :
   if pacman_rect.colliderect(enemy.enemy_rect) :
    print("Game OVER !")
    stop = True
    thread_food.join()
    pygame.quit()
    sys.exit()
  for y, row in enumerate(map_data):
    for x, cell in enumerate(row):
      if cell == '1':
         wall_rect = pygame.Rect(x * 20, y * 20, 20, 20)
         if pacman_rect.colliderect(wall_rect):
           pacman_x, pacman_y = old_pacman_x, old_pacman_y
         continue
      elif cell == '2':
         food_rect = pygame.Rect(x * 20 + 5, y * 20 + 5, 10, 10)
         if pacman_rect.colliderect(food_rect):
           feed += 1
           map_data[y][x] = '0'
  draw_pacman()
  pygame.display.update()
  counter += 1
