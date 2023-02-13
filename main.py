# -*- coding: utf-8 -*-
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
import time
import threading
import random
import sys

pygame.init()

class Enemy:
    def __init__(self, x, y, choosen_map) :
      self.x = x
      self.y = y
      self.image = pygame.image.load('src/%simages4.png'%choosen_map)
      self.image = pygame.transform.scale(self.image, (20, 20))
      self.direction = random.choice(['up', 'down', 'left', 'right'])
      self.enemy_rect = pygame.Rect(self.x, self.y, 20, 20)

    def update(self, counter, map_data, map_width, map_height):
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

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

def draw_pacman(screen, player_image, pacman_x, pacman_y):
  screen.blit(player_image, (pacman_x, pacman_y))

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

def periodic_task(map_data, map_width, map_height):
  global stop
  while not stop :
    time.sleep(1)
    if (random.randint(0, 9)) == 5 :
     x = random.randint(0, map_width-1)
     y = random.randint(0, map_height-1)
     if map_data[y][x] == '0' :
       map_data[y][x] = '2'

def pause_menu(screen, map_width, map_height):
  width = map_width * 20
  height = map_height * 20
  pause_dimx = width / 3
  pause_dimy = height / 10
  screen.fill((0, 0, 0))
  pause_rect = pygame.Rect(width / 2 - pause_dimx, height  * 0.10, pause_dimx * 2, pause_dimy * 2)
  restart_rect = pygame.Rect(width / 2 - pause_dimx / 2, height * 0.50 - pause_dimy / 2, pause_dimx, pause_dimy)
  resume_rect = pygame.Rect(width / 2 - pause_dimx / 2, height * 0.65 - pause_dimy / 2, pause_dimx, pause_dimy)
  exit_rect = pygame.Rect(width / 2 - pause_dimx / 2, height * 0.80 - pause_dimy / 2, pause_dimx, pause_dimy)
  running = True
  paused = True
  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        return 1
      mouse_pos = pygame.mouse.get_pos()
      if restart_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (255, 150, 150), restart_rect)
        if event.type == pygame.MOUSEBUTTONDOWN:
          return 2
      else:
        pygame.draw.rect(screen, (255, 0, 0), restart_rect)
      if resume_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (150, 255, 150), resume_rect)
        if event.type == pygame.MOUSEBUTTONDOWN:
          running = False
          return 0
      else:
        pygame.draw.rect(screen, (0, 255, 0), resume_rect)
      if exit_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (150, 150, 255), exit_rect)
        if event.type == pygame.MOUSEBUTTONDOWN:
          running = False
          return 1
      else:
        pygame.draw.rect(screen, (0, 0, 255), exit_rect)
      font_size = int(min(pause_dimy / 2, pause_dimx / 2))
      font = pygame.font.Font(None, font_size)
      restart_text = font.render("Main Menu", 1, (255, 255, 255))
      restart_text_rect = restart_text.get_rect()
      restart_text_rect.center = restart_rect.center
      resume_text = font.render("Resume", 1, (255, 255, 255))
      resume_text_rect = resume_text.get_rect()
      resume_text_rect.center = resume_rect.center
      exit_text = font.render("Exit", 1, (255, 255, 255))
      exit_text_rect = exit_text.get_rect()
      exit_text_rect.center = exit_rect.center
      screen.blit(restart_text, restart_text_rect)
      screen.blit(resume_text, resume_text_rect)
      screen.blit(exit_text, exit_text_rect)
      font_title = pygame.font.Font(None, 36)
      pygame.draw.rect(screen, (0, 0, 0), pause_rect)
      pause_text = font_title.render("Pause Menu :", 1, (255, 255, 255))
      pause_text_rect = pause_text.get_rect()
      pause_text_rect.center = pause_rect.center
      screen.blit(pause_text, pause_text_rect)
      pygame.display.update()

def decide_color(choosen_map):
  if choosen_map == "map1":
    return 180, 180, 180
  elif choosen_map == "map2":
    return 150, 125, 30
  else :
    return 239, 221, 111

def main_loop(choosen_map, skin):
  R, G, B = decide_color(choosen_map)
  map_data, map_width, map_height, pacman_x, pacman_y = create_map('src/%s.txt'%choosen_map)
  screen = pygame.display.set_mode((map_width * 20, map_height * 20))
  pygame.display.set_caption('Beef-Man')
  player_image = pygame.image.load('src/%s.png'%skin)
  player_image = pygame.transform.scale(player_image, (20, 20))
  wall_image = pygame.image.load('src/%simages2.png'%choosen_map)
  wall_image = pygame.transform.scale(wall_image, (20, 20))
  food_image = pygame.image.load('src/images3.png')
  food_image = pygame.transform.scale(food_image, (20, 20))
  feed = 0
  pygame.font.init()
  font = pygame.font.Font(None, 32)
  text = font.render("{}".format(feed), True, (255, 100, 0))
  counter = 0
  enough_feed = 10
  enemies = []
  for y, row in enumerate(map_data):
    for x, cell in enumerate(row):
      if cell == 'y' :
        enemies.append(Enemy(x * 20, y * 20, choosen_map))
  global stop 
  stop = False 
  thread_food = threading.Thread(target=lambda : periodic_task(map_data, map_width, map_height))
  thread_food.start()

  while True:
    for y, row in enumerate(map_data):
      for x, cell in enumerate(row):
        if cell == '1':
          screen.blit(wall_image, (x * 20, y * 20))
        elif cell == '2':
          pygame.draw.rect(screen, (R, G, B), (x * 20, y * 20, 20, 20))
          screen.blit(food_image, (x * 20, y * 20))
        else :
          pygame.draw.rect(screen, (R, G, B), (x * 20, y * 20, 20, 20))
    for enemy in enemies :
      enemy.update(counter, map_data, map_width, map_height)
      enemy.draw(screen)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        stop = True
        thread_food.join()
        pygame.quit()
        sys.exit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
      ret = pause_menu(screen, map_width, map_height)
      if ret == 1 :
        stop = True
        thread_food.join()
        pygame.quit()
        sys.exit()
      elif ret == 2 :
        main_menu()
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
      print("You WON !")
      stop = True
      thread_food.join()
      win_menu(screen, map_width, map_height, choosen_map, skin)
    for enemy in enemies :
      if pacman_rect.colliderect(enemy.enemy_rect) :
        print("Game OVER !")
        stop = True
        thread_food.join()
        loss_menu(screen, map_width, map_height, choosen_map, skin)
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
    draw_pacman(screen, player_image, pacman_x, pacman_y)
    pygame.display.update()
    counter += 1

def map_menu(screen):
  width = 800
  height = 600
  menu_dimx = width / 3
  menu_dimy = height / 10
  screen.fill((0, 0, 0))
  menu_rect = pygame.Rect(width / 2 - menu_dimx, height  * 0.10, menu_dimx * 2, menu_dimy * 2)
  map1_rect = pygame.Rect(width / 2 - menu_dimx / 2, height * 0.50 - menu_dimy / 2, menu_dimx, menu_dimy)
  map2_rect = pygame.Rect(width / 2 - menu_dimx / 2, height * 0.65 - menu_dimy / 2, menu_dimx, menu_dimy)
  map3_rect = pygame.Rect(width / 2 - menu_dimx / 2, height * 0.80 - menu_dimy / 2, menu_dimx, menu_dimy)
  running = True
  paused = True
  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
        thread_food.join()
        pygame.quit()
        sys.exit()
      mouse_pos = pygame.mouse.get_pos()
      if map1_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (150, 150, 255), map1_rect)
        if event.type == pygame.MOUSEBUTTONDOWN:
          running = False
          return("map1")
      else:
        pygame.draw.rect(screen, (0, 0, 255), map1_rect)
      if map2_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (150, 255, 150), map2_rect)
        if event.type == pygame.MOUSEBUTTONDOWN:
          running = False
          return("map2")
      else:
        pygame.draw.rect(screen, (0, 255, 0), map2_rect)
      if map3_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (255, 150, 150), map3_rect)
        if event.type == pygame.MOUSEBUTTONDOWN:
          running = False
          return("map3")
      else:
        pygame.draw.rect(screen, (255, 0, 0), map3_rect)
      font_size = int(min(menu_dimy / 2, menu_dimx / 2))
      font = pygame.font.Font(None, font_size)
      map1_text = font.render("Rocking Slice", 1, (255, 255, 255))
      map1_text_rect = map1_text.get_rect()
      map1_text_rect.center = map1_rect.center
      map2_text = font.render("Backrooms", 1, (255, 255, 255))
      map2_text_rect = map2_text.get_rect()
      map2_text_rect.center = map2_rect.center
      map3_text = font.render("Do Not Go There", 1, (255, 255, 255))
      map3_text_rect = map3_text.get_rect()
      map3_text_rect.center = map3_rect.center
      screen.blit(map1_text, map1_text_rect)
      screen.blit(map2_text, map2_text_rect)
      screen.blit(map3_text, map3_text_rect)
      font_title = pygame.font.Font(None, 36)
      pygame.draw.rect(screen, (0, 0, 0), menu_rect)
      menu_text = font_title.render("Map Menu :", 1, (255, 255, 255))
      menu_text_rect = menu_text.get_rect()
      menu_text_rect.center = menu_rect.center
      screen.blit(menu_text, menu_text_rect)
      pygame.display.update()

def skin_menu(screen):
  width = 800
  height = 600
  menu_dimx = width / 3
  menu_dimy = height / 10
  screen.fill((0, 0, 0))
  menu_rect = pygame.Rect(width / 2 - menu_dimx, height  * 0.10, menu_dimx * 2, menu_dimy * 2)
  skin1_rect = pygame.Rect(width / 2 - menu_dimx / 2, height * 0.50 - menu_dimy / 2, menu_dimx, menu_dimy)
  skin2_rect = pygame.Rect(width / 2 - menu_dimx / 2, height * 0.65 - menu_dimy / 2, menu_dimx, menu_dimy)
  skin3_rect = pygame.Rect(width / 2 - menu_dimx / 2, height * 0.80 - menu_dimy / 2, menu_dimx, menu_dimy)
  running = True
  paused = True
  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
        thread_food.join()
        pygame.quit()
        sys.exit()
      mouse_pos = pygame.mouse.get_pos()
      if skin1_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (150, 150, 255), skin1_rect)
        if event.type == pygame.MOUSEBUTTONDOWN:
          running = False
          return("skin1")
      else:
        pygame.draw.rect(screen, (0, 0, 255), skin1_rect)
      if skin2_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (150, 255, 150), skin2_rect)
        if event.type == pygame.MOUSEBUTTONDOWN:
          running = False
          return("skin2")
      else:
        pygame.draw.rect(screen, (0, 255, 0), skin2_rect)
      if skin3_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (255, 150, 150), skin3_rect)
        if event.type == pygame.MOUSEBUTTONDOWN:
          running = False
          return("skin3")
      else:
        pygame.draw.rect(screen, (255, 0, 0), skin3_rect)
      font_size = int(min(menu_dimy / 2, menu_dimx / 2))
      font = pygame.font.Font(None, font_size)
      skin1_text = font.render("Pacman", 1, (255, 255, 255))
      skin1_text_rect = skin1_text.get_rect()
      skin1_text_rect.center = skin1_rect.center
      skin2_text = font.render("Hehboi", 1, (255, 255, 255))
      skin2_text_rect = skin2_text.get_rect()
      skin2_text_rect.center = skin2_rect.center
      skin3_text = font.render("Do Not Take This One", 1, (255, 255, 255))
      skin3_text_rect = skin3_text.get_rect()
      skin3_text_rect.center = skin3_rect.center
      screen.blit(skin1_text, skin1_text_rect)
      screen.blit(skin2_text, skin2_text_rect)
      screen.blit(skin3_text, skin3_text_rect)
      font_title = pygame.font.Font(None, 36)
      pygame.draw.rect(screen, (0, 0, 0), menu_rect)
      menu_text = font_title.render("Skin Menu :", 1, (255, 255, 255))
      menu_text_rect = menu_text.get_rect()
      menu_text_rect.center = menu_rect.center
      screen.blit(menu_text, menu_text_rect)
      pygame.display.update()

def main_menu():
  screen = pygame.display.set_mode((800, 600))
  pygame.display.set_caption('Beef-Man')
  width = 800
  height = 600
  menu_dimx = width / 3
  menu_dimy = height / 10
  screen.fill((0, 0, 0))
  menu_rect = pygame.Rect(width / 2 - menu_dimx, height  * 0.10, menu_dimx * 2, menu_dimy * 2)
  start_rect = pygame.Rect(width / 2 - menu_dimx / 2, height * 0.35 - menu_dimy / 2, menu_dimx, menu_dimy)
  choosemap_rect = pygame.Rect(width / 2 - menu_dimx / 2, height * 0.50 - menu_dimy / 2, menu_dimx, menu_dimy)
  chooseskin_rect = pygame.Rect(width / 2 - menu_dimx / 2, height * 0.65 - menu_dimy / 2, menu_dimx, menu_dimy)
  exit_rect = pygame.Rect(width / 2 - menu_dimx / 2, height * 0.80 - menu_dimy / 2, menu_dimx, menu_dimy)
  running = True
  paused = True
  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
        thread_food.join()
        pygame.quit()
        sys.exit()
      mouse_pos = pygame.mouse.get_pos()
      if choosemap_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (255, 150, 150), choosemap_rect)
        if event.type == pygame.MOUSEBUTTONDOWN:
          choosen_map = map_menu(screen)
      else:
        pygame.draw.rect(screen, (255, 0, 0), choosemap_rect)
      if chooseskin_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (180, 180, 150), chooseskin_rect)
        if event.type == pygame.MOUSEBUTTONDOWN:
          skin = skin_menu(screen)
      else:
        pygame.draw.rect(screen, (180, 180, 0), chooseskin_rect)
      if exit_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (150, 150, 255), exit_rect)
        if event.type == pygame.MOUSEBUTTONDOWN:
          running = False
          thread_food.join()
          pygame.quit()
          sys.exit()
      else:
        pygame.draw.rect(screen, (0, 0, 255), exit_rect)
      if start_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (150, 255, 150), start_rect)
        if event.type == pygame.MOUSEBUTTONDOWN:
          pygame.quit()
          if 'choosen_map' not in locals():
            choosen_map = 'map1'
          if 'skin' not in locals():
            skin = 'skin1'
          main_loop(choosen_map, skin)
      else:
        pygame.draw.rect(screen, (0, 255, 0), start_rect)
      font_size = int(min(menu_dimy / 2, menu_dimx / 2))
      font = pygame.font.Font(None, font_size)
      choosemap_text = font.render("Choose Map", 1, (255, 255, 255))
      choosemap_text_rect = choosemap_text.get_rect()
      choosemap_text_rect.center = choosemap_rect.center
      chooseskin_text = font.render("Choose Skin", 1, (255, 255, 255))
      chooseskin_text_rect = chooseskin_text.get_rect()
      chooseskin_text_rect.center = chooseskin_rect.center
      exit_text = font.render("Exit", 1, (255, 255, 255))
      exit_text_rect = exit_text.get_rect()
      exit_text_rect.center = exit_rect.center
      start_text = font.render("Start Game", 1, (255, 255, 255))
      start_text_rect = start_text.get_rect()
      start_text_rect.center = start_rect.center
      screen.blit(choosemap_text, choosemap_text_rect)
      screen.blit(chooseskin_text, chooseskin_text_rect)
      screen.blit(exit_text, exit_text_rect)
      screen.blit(start_text, start_text_rect)
      font_title = pygame.font.Font(None, 36)
      pygame.draw.rect(screen, (0, 0, 0), menu_rect)
      menu_text = font_title.render("Main Menu :", 1, (255, 255, 255))
      menu_text_rect = menu_text.get_rect()
      menu_text_rect.center = menu_rect.center
      screen.blit(menu_text, menu_text_rect)
      pygame.display.update()

def pause_menu(screen, map_width, map_height):
  width = map_width * 20
  height = map_height * 20
  pause_dimx = width / 3
  pause_dimy = height / 10
  screen.fill((0, 0, 0))
  pause_rect = pygame.Rect(width / 2 - pause_dimx, height  * 0.10, pause_dimx * 2, pause_dimy * 2)
  restart_rect = pygame.Rect(width / 2 - pause_dimx / 2, height * 0.50 - pause_dimy / 2, pause_dimx, pause_dimy)
  resume_rect = pygame.Rect(width / 2 - pause_dimx / 2, height * 0.65 - pause_dimy / 2, pause_dimx, pause_dimy)
  exit_rect = pygame.Rect(width / 2 - pause_dimx / 2, height * 0.80 - pause_dimy / 2, pause_dimx, pause_dimy)
  running = True
  paused = True
  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        return 1
      mouse_pos = pygame.mouse.get_pos()
      if restart_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (255, 150, 150), restart_rect)
        if event.type == pygame.MOUSEBUTTONDOWN:
          return 2
      else:
        pygame.draw.rect(screen, (255, 0, 0), restart_rect)
      if resume_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (150, 255, 150), resume_rect)
        if event.type == pygame.MOUSEBUTTONDOWN:
          running = False
          return 0
      else:
        pygame.draw.rect(screen, (0, 255, 0), resume_rect)
      if exit_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (150, 150, 255), exit_rect)
        if event.type == pygame.MOUSEBUTTONDOWN:
          running = False
          return 1
      else:
        pygame.draw.rect(screen, (0, 0, 255), exit_rect)
      font_size = int(min(pause_dimy / 2, pause_dimx / 2))
      font = pygame.font.Font(None, font_size)
      restart_text = font.render("Main Menu", 1, (255, 255, 255))
      restart_text_rect = restart_text.get_rect()
      restart_text_rect.center = restart_rect.center
      resume_text = font.render("Resume", 1, (255, 255, 255))
      resume_text_rect = resume_text.get_rect()
      resume_text_rect.center = resume_rect.center
      exit_text = font.render("Exit", 1, (255, 255, 255))
      exit_text_rect = exit_text.get_rect()
      exit_text_rect.center = exit_rect.center
      screen.blit(restart_text, restart_text_rect)
      screen.blit(resume_text, resume_text_rect)
      screen.blit(exit_text, exit_text_rect)
      font_title = pygame.font.Font(None, 36)
      pygame.draw.rect(screen, (0, 0, 0), pause_rect)
      pause_text = font_title.render("Pause Menu :", 1, (255, 255, 255))
      pause_text_rect = pause_text.get_rect()
      pause_text_rect.center = pause_rect.center
      screen.blit(pause_text, pause_text_rect)
      pygame.display.update()

def win_menu(screen, map_width, map_height, choosen_map, skin):
  width = map_width * 20
  height = map_height * 20
  win_dimx = width / 3
  win_dimy = height / 10
  screen.fill((0, 0, 0))
  win_rect = pygame.Rect(width / 2 - win_dimx, height  * 0.10, win_dimx * 2, win_dimy * 2)
  restart_rect = pygame.Rect(width / 2 - win_dimx / 2, height * 0.50 - win_dimy / 2, win_dimx, win_dimy)
  resume_rect = pygame.Rect(width / 2 - win_dimx / 2, height * 0.65 - win_dimy / 2, win_dimx, win_dimy)
  exit_rect = pygame.Rect(width / 2 - win_dimx / 2, height * 0.80 - win_dimy / 2, win_dimx, win_dimy)
  running = True
  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
        thread_food.join()
        pygame.quit()
        sys.exit()
      mouse_pos = pygame.mouse.get_pos()
      if restart_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (255, 150, 150), restart_rect)
        if event.type == pygame.MOUSEBUTTONDOWN:
          running = False
          main_menu()
      else:
        pygame.draw.rect(screen, (255, 0, 0), restart_rect)
      if resume_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (150, 255, 150), resume_rect)
        if event.type == pygame.MOUSEBUTTONDOWN:
          running = False
          main_loop(choosen_map, skin)
      else:
        pygame.draw.rect(screen, (0, 255, 0), resume_rect)
      if exit_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (150, 150, 255), exit_rect)
        if event.type == pygame.MOUSEBUTTONDOWN:
          running = False
          thread_food.join()
          pygame.quit()
          sys.exit()
      else:
        pygame.draw.rect(screen, (0, 0, 255), exit_rect)
      font_size = int(min(win_dimy / 2, win_dimx / 2))
      font = pygame.font.Font(None, font_size)
      restart_text = font.render("Main Menu", 1, (255, 255, 255))
      restart_text_rect = restart_text.get_rect()
      restart_text_rect.center = restart_rect.center
      resume_text = font.render("Try Again", 1, (255, 255, 255))
      resume_text_rect = resume_text.get_rect()
      resume_text_rect.center = resume_rect.center
      exit_text = font.render("Exit", 1, (255, 255, 255))
      exit_text_rect = exit_text.get_rect()
      exit_text_rect.center = exit_rect.center
      screen.blit(restart_text, restart_text_rect)
      screen.blit(resume_text, resume_text_rect)
      screen.blit(exit_text, exit_text_rect)
      font_title = pygame.font.Font(None, 50)
      pygame.draw.rect(screen, (0, 0, 0), win_rect)
      win_text = font_title.render("You WON !", 1, (255, 255, 255))
      win_text_rect = win_text.get_rect()
      win_text_rect.center = win_rect.center
      screen.blit(win_text, win_text_rect)
      pygame.display.update()

def loss_menu(screen, map_width, map_height, choosen_map, skin):
  width = map_width * 20
  height = map_height * 20
  loss_dimx = width / 3
  loss_dimy = height / 10
  screen.fill((0, 0, 0))
  loss_rect = pygame.Rect(width / 2 - loss_dimx, height  * 0.10, loss_dimx * 2, loss_dimy * 2)
  restart_rect = pygame.Rect(width / 2 - loss_dimx / 2, height * 0.50 - loss_dimy / 2, loss_dimx, loss_dimy)
  resume_rect = pygame.Rect(width / 2 - loss_dimx / 2, height * 0.65 - loss_dimy / 2, loss_dimx, loss_dimy)
  exit_rect = pygame.Rect(width / 2 - loss_dimx / 2, height * 0.80 - loss_dimy / 2, loss_dimx, loss_dimy)
  running = True
  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
        thread_food.join()
        pygame.quit()
        sys.exit()
      mouse_pos = pygame.mouse.get_pos()
      if restart_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (255, 150, 150), restart_rect)
        if event.type == pygame.MOUSEBUTTONDOWN:
          running = False
          main_menu()
      else:
        pygame.draw.rect(screen, (255, 0, 0), restart_rect)
      if resume_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (150, 255, 150), resume_rect)
        if event.type == pygame.MOUSEBUTTONDOWN:
          running = False
          main_loop(choosen_map, skin)
      else:
        pygame.draw.rect(screen, (0, 255, 0), resume_rect)
      if exit_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, (150, 150, 255), exit_rect)
        if event.type == pygame.MOUSEBUTTONDOWN:
          running = False
          thread_food.join()
          pygame.quit()
          sys.exit()
      else:
        pygame.draw.rect(screen, (0, 0, 255), exit_rect)
      font_size = int(min(loss_dimy / 2, loss_dimx / 2))
      font = pygame.font.Font(None, font_size)
      restart_text = font.render("Main Menu", 1, (255, 255, 255))
      restart_text_rect = restart_text.get_rect()
      restart_text_rect.center = restart_rect.center
      resume_text = font.render("Try Again", 1, (255, 255, 255))
      resume_text_rect = resume_text.get_rect()
      resume_text_rect.center = resume_rect.center
      exit_text = font.render("Exit", 1, (255, 255, 255))
      exit_text_rect = exit_text.get_rect()
      exit_text_rect.center = exit_rect.center
      screen.blit(restart_text, restart_text_rect)
      screen.blit(resume_text, resume_text_rect)
      screen.blit(exit_text, exit_text_rect)
      font_title = pygame.font.Font(None, 50)
      pygame.draw.rect(screen, (0, 0, 0), loss_rect)
      loss_text = font_title.render("You LOST !", 1, (255, 255, 255))
      loss_text_rect = loss_text.get_rect()
      loss_text_rect.center = loss_rect.center
      screen.blit(loss_text, loss_text_rect)
      pygame.display.update()

main_menu()