# import and initialize pygame
import pygame
from pygame import mixer
import math
import random

pygame.init()
pygame.mixer.init()

screen_width = 800
screen_height = 480

# set up the window
win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Pyghter")

# defining most of the variables we'll need later
p1 = {'x': 50, 'y': 300, 'xvel': 0, "alive": True}
p2 = {'x': 50, 'y': 200, 'xvel': 0, "alive": True}
rock = {"xsize": [], "ysize": [], "x": [], "y": [], "yvel": [], "spawn": 0, "rotation": 0.0}
charwidth, charheight = 75, 25
yvel = 8 # velocity, speed at which player will move at (yvel is constant, xvel is variable)
scroll, hitcount = 0, 0
playercount = 2

# bg (background) and img(player sprite)
bg = pygame.transform.scale(pygame.image.load('C:/Users/Moi/Pictures/gayme/background.jpg'), (640, 480))
sprite1 = pygame.transform.scale(pygame.image.load("C:/Users/Moi/Pictures/gayme/sprite.png"), (charwidth, charheight))
sprite2 = pygame.transform.scale(pygame.image.load("C:/Users/Moi/Pictures/gayme/sprite2.png"), (charwidth, charheight))
rock_template1 = pygame.transform.scale(pygame.image.load('C:/Users/Moi/Pictures/gayme/rock1.png'), (50, 50))
rock_template2 = pygame.transform.scale(pygame.image.load('C:/Users/Moi/Pictures/gayme/rock2.png'), (50, 50))
rock_template3 = pygame.transform.scale(pygame.image.load('C:/Users/Moi/Pictures/gayme/rock3.png'), (50, 50))
rock_template4 = pygame.transform.scale(pygame.image.load('C:/Users/Moi/Pictures/gayme/cool_rock.png'), (50, 50)) # transform later
button_start = pygame.transform.scale(pygame.image.load('C:/Users/Moi/Pictures/gayme/start.png'), (120, 100))
button_resume = pygame.transform.scale(pygame.image.load('C:/Users/Moi/Pictures/gayme/resume.png'), (120, 100))
button_exit = pygame.transform.scale(pygame.image.load('C:/Users/Moi/Pictures/gayme/exit.png'), (120, 100))
button_p1 = pygame.transform.scale(pygame.image.load('C:/Users/Moi/Pictures/gayme/1 player.png'), (120, 100))
button_p2 = pygame.transform.scale(pygame.image.load('C:/Users/Moi/Pictures/gayme/2 players.png'), (120, 100))
gameover_img = pygame.image.load('C:/Users/Moi/Pictures/gayme/gameover_screen.png')
darken = pygame.Surface((screen_width, screen_height))
darken.set_alpha(128)
darken.fill((0, 0, 0))
# tiles
tiles = math.ceil(screen_width / bg.get_width()) + 1  # amount of bg tiles, +1 for buffer



def refresh(rotate):
  """Function that draws all the usual components (backgound, players, rock if needed),
  defines variables that need to be constantly refreshed such as mouse and keys,
  sets fps,
  event handler for exit
  --
  Does everything that basically all of the loops (start menu, pause, game loop, game over) need, to avoid having to define all of this in every single loop."""
  # defining variables
  global scroll, keys, mouse
  mouse = pygame.mouse.get_pos()
  keys = pygame.key.get_pressed()
  pygame.time.Clock().tick(60) # fps
  # drawing everything : scrolling background
  for i in range(tiles):
    win.blit(bg, (i * 640 + scroll, 0))
  scroll -= 0.5 
  if abs(scroll) > 640: scroll = 0
  # player sprite
  if rotate:
    if keys[pygame.K_DOWN]: win.blit(pygame.transform.rotate(sprite1, -20), (p1['x'], p1['y']))
    elif keys[pygame.K_UP]: win.blit(pygame.transform.rotate(sprite1, 20), (p1['x'], p1['y']))
    else: win.blit(sprite1, (p1['x'], p1['y']))
    if keys[pygame.K_s]: win.blit(pygame.transform.rotate(sprite2, -20), (p2['x'], p2['y']))
    elif keys[pygame.K_z]: win.blit(pygame.transform.rotate(sprite2, 20), (p2['x'], p2['y']))
    else: win.blit(sprite2, (p2['x'], p2['y']))
  if not rotate: 
    win.blit(sprite1, (p1['x'], p1['y']))
    win.blit(sprite2, (p2['x'], p2['y']))
  # rock if it is spawned
  if rock["spawn"] > 0:
    for i in range(rock['spawn']):
      rock_img = pygame.transform.rotate(pygame.transform.scale(rock_template1, (rock['xsize'][i], rock['ysize'][i])), rock["rotation"])
      new_rect = rock_img.get_rect(center = rock_template1.get_rect(center = (rock['x'][i], rock['y'][i])).center)
      #rotate is a local var, so rotating 5° then undoing it
      win.blit(rock_img, new_rect)
  # event (quit) handler
  for event in pygame.event.get():
      if event.type == pygame.QUIT:
        exit()



def pause():
  broken = False
  while True:
    # refresh
    refresh(False)
    win.blit(darken, (0, 0))
    win.blit(button_resume, (330, 140))
    win.blit(button_exit, (330, 290))
    pygame.display.update()
    # exit conditions (escape key)
    if pygame.KEYUP and keys[pygame.K_ESCAPE]:
      break
    # mouse or enter
    if  330 <= mouse[0] <= 430 and 140 <= mouse[1] <= 205 and pygame.mouse.get_pressed()[0] or keys[pygame.K_RETURN]:
      break
    if  330 <= mouse[0] <= 430 and 290 <= mouse[1] <= 355 and pygame.mouse.get_pressed()[0] or keys[pygame.K_RETURN]:
      exit()
    # selector arrow, settings button, darken screen (before true loop), resume, quit



def coordfail(player):
  global playercount
  player['xvel'] = -0.4
  player['x'] += player['xvel']
  if player["x"] < -100:
    player['x'] = 999
    player['xvel'] = 0
    player["alive"] = False
    playercount -= 1



def hitfail(player):
  global hitcount
  if hitcount < 241:
    player['x'] -= 8
    hitcount += 1



def game_over():
  global p1, p2, rock, playercount
  while True:
    refresh(False)
    win.blit(darken, (0, 0))
    win.blit(gameover_img, (screen_width // 2 - gameover_img.get_width() // 2, screen_height // 2 - gameover_img.get_height() // 2))
    win.blit(button_resume, (330, 290))
    win.blit(button_exit, (330, 350))
    pygame.display.update()
    if  330 <= mouse[0] <= 430 and 290 <= mouse[1] <= 355 and pygame.mouse.get_pressed()[0] or keys[pygame.K_RETURN]:
      p1 = {'x': 50, 'y': 300, 'xvel': 0, "alive": 1}
      p2 = {'x': 50, 'y': 200, 'xvel': 0, "alive": 1}
      rock = {"xsize": [], "ysize": [], "x": [], "y": [], "yvel": [], "spawn": 0, "rotation": 0.0}
      playercount = 2
      break
    if  330 <= mouse[0] <= 430 and 350 <= mouse[1] <= 415 and pygame.mouse.get_pressed()[0] or keys[pygame.K_RETURN]:
      exit()



# beginner menu loop
while True:
  #refresh
  refresh(False)
  win.blit(button_start, (330, 375))
  pygame.display.update()
  # if mouse in start button and left click start game loop
  if 350 <= mouse[0] <= 430 and 405 <= mouse[1] <= 440 and pygame.mouse.get_pressed()[0] or keys[pygame.K_RETURN]:
    break



"""# player count choice menu loop
while True:
  #refresh
  refresh(False)
  win.blit(button_p1, (330, 375))
  win.blit(button_p2, (330, 375))
  pygame.display.update()
  # if mouse in start button and left click start game loop
  if 350 <= mouse[0] <= 430 and 405 <= mouse[1] <= 440 and pygame.mouse.get_pressed()[0] or keys[pygame.K_RETURN]:
    break"""



# game loop (includes game, /pause screen, and /gameover screen)
while True:
  # refresh
  refresh(True)
  pygame.display.update()
  # right wall limit to block the user from going off the screen
  if p1['x'] < 722: p1['x'] += p1['xvel']
  elif p1['xvel'] < 0: p1['x'] += p1['xvel']
  elif p1['xvel'] > 0: p1['xvel'] = 0
  if p2['x'] < 722: p2['x'] += p2['xvel']
  elif p2['xvel'] < 0: p2['x'] += p2['xvel']
  elif p2['xvel'] > 0: p2['xvel'] = 0
  # controls
  if p1["alive"]:
    if keys[pygame.K_UP] and p1['y'] > 0: p1['y'] -= yvel
    if keys[pygame.K_DOWN] and p1['y'] < 451: p1['y'] += yvel
    if keys[pygame.K_LEFT] and p1['x'] > 0: p1['xvel'] -= 0.5
    if keys[pygame.K_RIGHT] and p1['x'] < 722: p1['xvel'] += 0.5
  if p2["alive"]:
    if keys[pygame.K_z] and p2['y'] > 0: p2['y'] -= yvel
    if keys[pygame.K_s] and p2['y'] < 451: p2['y'] += yvel
    if keys[pygame.K_q] and p2['x'] > 0: p2['xvel'] -= 0.5
    if keys[pygame.K_d] and p2['x'] < 722: p2['xvel'] += 0.5
  # pause
  if pygame.KEYUP and keys[pygame.K_ESCAPE]:
      pause()
  # if player too far to the right then coordfail
  if p1['x'] < 10 and p1["alive"]: coordfail(p1)
  if p2['x'] < 10 and p2["alive"]: coordfail(p2)



  # chance of rock spawning
  if random.randint(0,260) > 250:
    rock["spawn"] += 1
    rock['yvel'].append(random.randint(-10, 10) / 10)
    rock['y'].append(random.randint(0, 480))
    rock["x"].append(800)
    rock['xsize'].append(random.randint(30, 100)) 
    rock['ysize'].append(random.randint(30, 100))
  # if rock is spawned then move left, if rock goes off screen then teleport to right side and stop spawning
  if rock['spawn'] > 0: 
    for i in range(rock["spawn"]):
      rock['x'][i] -= 5
      rock['y'][i] += rock['yvel'][i]
    if rock["rotation"] < 360:
      rock["rotation"] += 10
    else:
      rock["rotation"] = 0
  # hit check if a player has hit the rock
  for i in range(rock["spawn"]):
    if abs(rock['x'][i] - p1['x']) <= rock["xsize"][i] and abs(rock['y'][i] - p1['y']) <= rock["ysize"][i] and p1["alive"]: hitfail(p1)
    if abs(rock['x'][i] - p2['x']) <= rock["xsize"][i] and abs(rock['y'][i] - p2['y']) <= rock["ysize"][i] and p2["alive"]: hitfail(p2)
  # if no more players game over
  for i in range(rock["spawn"]-1):
    if rock['x'][i] < -50:
      rock['yvel'].pop(i)
      rock['y'].pop(i)
      rock['x'].pop(i)
      rock['xsize'].pop(i)
      rock['ysize'].pop(i)
      rock["spawn"] -= 1
  if playercount <= 0: game_over()

"""fix deaths
fix keyup problems
random rock size
random rock rotation
random rock direction
p1 p2 choice
pause resume and exit"""

# constantly rock list appending, but not removing when < -50 (find a way to remove certain list indexes without pop)