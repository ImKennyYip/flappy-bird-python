import pygame
from sys import exit
import random

#game variables -- dimensions of the background image
GAME_WIDTH = 360
GAME_HEIGHT = 640

# variable for game over popup
popup_width = 280
popup_height = 240

popup_bg_color = (30, 30, 30)
popup_border_color = (254, 254, 254)

# bird class
bird_x = GAME_WIDTH/8
bird_y = GAME_HEIGHT/2
bird_width = 34 # ratio is 17/12 SIMPLIFIED
bird_height = 24

class Bird(pygame.Rect): # this is a class for the placement of the bird to be used
   def __init__(self, img):
       pygame.Rect.__init__(self, bird_x, bird_y, bird_width, bird_height)
       self.img = img


# game images
background_image = pygame.image.load("flappybirdbg.png")
bird_image = pygame.image.load("flappybird.png")
bird_image = pygame.transform.scale(bird_image, (bird_width, bird_height))

# pipe class
pipe_x = GAME_WIDTH     # starting for the pipes to come in (WILL BE OFFSCREEN AT FIRST)
pipe_y = 0
pipe_width = 64
pipe_height = 512      # later to be moved up since the pipe will be scaled

class Pipe (pygame.Rect):
   def __init__ (self, img):
       pygame.Rect.__init__(self, pipe_x, pipe_y, pipe_width, pipe_height)
       self.img = img
       # if flappybird passed through the pipe, then this will be switched to true and will NOT be counted for again!
       self.passed = False
       
# load in image
top_pipe_image = pygame.image.load("toppipe.png")
# scale image to the given pipe width and height
top_pipe_image = pygame.transform.scale(top_pipe_image, (pipe_width, pipe_height))
# same thing with bottom pip
bottom_pipe_image = pygame.image.load("bottompipe.png")
bottom_pipe_image = pygame.transform.scale (bottom_pipe_image, (pipe_width, pipe_height))

# game logic
bird = Bird(bird_image)
pipes = [] # list
# for the change in position at which the bird moves at -- determine the velocity
velocity_x = -2 # 2 pixels to the left
velocity_y = 0
gravity_var = 0.4 # to help make sure the bird doesn't go out of frame
# scoring
score = 0
high_score = 0
game_over = False


# drawing the image
def draw():
   # coordinates on where to start drawing the image
   # top left corner is (0,0)
   window.blit(background_image, (0,0))
   window.blit(bird_image, bird)
  
   for pipe in pipes:
       window.blit(pipe.img, pipe)
  
   text_note = str(int(score))
   # if the game is over
   #if game_over:
      # text_note = "Game Over: " + text_note
          
   text_font = pygame.font.SysFont("Comic Sans MS", 50, bold = True)
   text_rendering = text_font.render(text_note, True, "white")
   window.blit(text_rendering, (5,0))
      
# move function

def move():
   global velocity_y, score, game_over, high_score # global variable since velocity_y is being reassigned
   velocity_y += gravity_var
   bird.y += velocity_y
   bird.y = max(bird.y, 0) #limit the y position, which can be a positive num or 0
  
   if bird.y > GAME_HEIGHT:
       game_over = True
       return
  
   # this will draw the pipes per the velocity
   for pipe in pipes:
       pipe.x += velocity_x

       # for everytime flappy passes the pipe, the score of 0.5 is added
       if not pipe.passed and bird.x > pipe.x + pipe.width:
           score += 50
           pipe.passed = True
       # check for highest score
       if score > high_score:
           high_score = score
          
       # check if flappy crashes into the pipe
       if bird.colliderect(pipe):
           game_over = True
           pygame.mixer.music.pause()
          
   while len(pipes) > 0 and pipes[0].x + pipe_width < 0:
       pipes.pop(0) # pop will remove the first element from the list
       # in this case, it removes the pipe at index 0
       # every time the pipes move off the screen, the pipes are removed - makes it easier for program to save mem
  
# creating new pipes  
def create_pipes():
   # randomly drawing bottom pipes
   random_pipe_y = pipe_y - pipe_height/4 - random.random()*(pipe_height/2) # this will randomly subract some amount of height
   # range is between 0 - h/2

   opening_space = GAME_HEIGHT/4
  
   top_pip = Pipe(top_pipe_image)
   top_pip.y = random_pipe_y
   pipes.append(top_pip)
  
   bottom_pipe = Pipe(bottom_pipe_image)
   # get the "in between" to which the bird can go through
   bottom_pipe.y = top_pip.y + pipe_height + opening_space
   pipes.append(bottom_pipe)
  
   print(len(pipes))

def game_over_popup():
  # pop-up rectangle in the center
   popup_rect = pygame.Rect(
      (GAME_WIDTH - popup_width) / 2,
      (GAME_HEIGHT - popup_height) / 2,
      popup_width,
      popup_height
  )
   # draw the popup background
   pygame.draw.rect(window, popup_bg_color, popup_rect, border_radius=13)
   pygame.draw.rect(window, popup_border_color, popup_rect, 3, border_radius=13)
 
   #fonts for the popup
   heading = pygame.font.SysFont("Comic Sans MS", 32, bold = True)
   score_font = pygame.font.SysFont("Comic Sans MS", 24, bold = True)
   reset_font = pygame.font.SysFont("Comic Sans MS", 18)
   highest_score_text  = pygame.font.SysFont("Comic Sans MS", 18)

   #text rendering
   heading_rendering = heading.render("GAME OVER", True, "white")
   score_rendering = score_font.render(f"Your Score: {int(score)}", True, "white")
   reset_rendering = reset_font.render("Press SPACE to restart", True, "white")
   highest_score_rendering = highest_score_text.render(f"Highest score: {int(high_score)}", True, "white")
  
   # center the text inside the popup
   heading_rect = heading_rendering.get_rect(
       center=(popup_rect.centerx, popup_rect.top + 45)
   )
   score_rect = score_rendering.get_rect(
       center=(popup_rect.centerx, popup_rect.centery)
   )
   highest_score_rect = highest_score_rendering.get_rect(
       center=(popup_rect.centerx, popup_rect.bottom - 85)
   )
   reset_rect = reset_rendering.get_rect(
       center=(popup_rect.centerx, popup_rect.bottom - 35)
   )
  
   # draw
   window.blit(heading_rendering, heading_rect)
   window.blit(score_rendering, score_rect)
   window.blit(reset_rendering, reset_rect)
   window.blit(highest_score_rendering, highest_score_rect)
  
pygame.init() # initialize pygame
# variable window for the background image to open up

#now for background music
pygame.mixer.init()
pygame.mixer.music.load("flappy_theme.mp3")
pygame.mixer.music.set_volume(0.4) # going from 0.0 - 0.4
pygame.mixer.music.play(-1) #-1 = loop infinitely, will stop when collision


window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("Flappy Bird")
# clock will run the game for the given amount of time
clock = pygame.time.Clock()

# what per rate we want to generate new pipes (a new event every time)
create_pipes_timer = pygame.USEREVENT + 0
pygame.time.set_timer(create_pipes_timer, 1500) # makes pipe every 1.5 seconds

# game loop for the window to stay open
while True:
   # for loop to check all current events
   for event in pygame.event.get():
       # create an exit button when the user clicks on the "X"
       if event.type == pygame.QUIT:
           pygame.quit()
           exit()
          
       # every 1.5 second, a new event is created and a pipe is generated
       if event.type == create_pipes_timer and not game_over:
           create_pipes()
  
       if event.type == pygame.KEYDOWN:
           # determing the key pressed down
           if event.key == pygame.K_SPACE: # checks if SPACE key is pressed so the bird can go up
               velocity_y = -6 # bird will go up by -6 frames (TOO MUCH, infinite loop, it'll keep going)
              
               # reset game
               if game_over:
                   bird.y = bird_y
                   pipes.clear()
                   score = 0
                   game_over = False
                   pygame.mixer.music.unpause()

              
   if not game_over:
       move() 
       draw()
   # if the game is OVER, then the popup is triggered and reset back
   else:
       draw()
       game_over_popup()
  
   pygame.display.update()
   # 60 frames per second
   clock.tick(60)





