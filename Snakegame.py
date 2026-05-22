import pygame as pg
import random
from snakelevels import *
pg.init()

SCREENWIDTH = 720
SCREENHEIGHT = 1500
screen = pg.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
clock = pg.time.Clock()

#       ____Loading and playing music____

background_music = pg.mixer.music.load("Assets/Background_music.mp3")
eating_sound = pg.mixer.Sound("Assets/EatingSound.mp3")
eating_sound.set_volume(1.0)
death_sound = pg.mixer.Sound("Assets/Dead.mp3")
death_sound.set_volume(1.0)
new_level_sound = pg.mixer.Sound("Assets/Nextlevel.mp3")
new_level_sound.set_volume(1.0)


#playing background music indefinitely
pg.mixer.music.play(-1, 0.0)
pg.mixer.music.set_volume(0.4)


#      ______   SETTINGS   ______

GRIDLENGTH = 720
framerate = 60
snakespeed = 7
initial_length = 2
snake_headcolor = (1, 0.2, 0.5) #Keep these rgb values in 0-1 range
bwidth = 350
bheight = 320
bw = bwidth/2
bh = bheight/3
score = 0
font = pg.font.Font("Assets/technology.ttf", 30)
tileoffset = 2
creasecolor = "grey"

level_index = 0
current_level = levels[level_index] #default level when program starts

gridsize = max(len(current_level), len(current_level[0]))
tilesize = GRIDLENGTH//gridsize
level_surface = pg.Surface((len(current_level[0])*tilesize, len(current_level)*tilesize))


buttons = [

	    #Button positions
		((SCREENWIDTH/2)-(bwidth/2)-10, GRIDLENGTH + ((SCREENHEIGHT-GRIDLENGTH)/2), "left"),
		((SCREENWIDTH/2) + 10, GRIDLENGTH + ((SCREENHEIGHT-GRIDLENGTH)/2), "right"),
		((SCREENWIDTH/2)-(bwidth/4), GRIDLENGTH + ((SCREENHEIGHT-GRIDLENGTH)/2)-(bheight/3)-10, "up"),
		((SCREENWIDTH/2)-(bwidth/4), GRIDLENGTH + ((SCREENHEIGHT-GRIDLENGTH)/2)+bheight/3 + 10, "down")
		
]
#___________________________________

# Functions

def drawlevel(surface, level):
	
	pg.draw.rect(surface, creasecolor, (0,0, (len(level[0]))*tilesize, (len(level))*tilesize))
	
	for row in range(len(level)):
		for column in range(len(level[row])):
			blockcode = level[row][column]
			x = column*tilesize
			y = row*tilesize
			color = level_encoding[str(blockcode)]
			pg.draw.rect(surface, color, (x+tileoffset/2, y+tileoffset/2, tilesize - tileoffset, tilesize - tileoffset))
		
				
def draw_buttons():
	for button in buttons:
		x, y = button[0], button[1]
		pg.draw.rect(screen, "grey", (x, y, bw, bh))
		pg.draw.rect(screen, "black", (x, y, bw, bh), 4	)
		
		
def increase_level():
	global level_index, current_level, score
	try:
		level_index += 1
		current_level = levels[level_index]
	except IndexError:
		current_level = levels[0]
		level_index = 0
		
		
def display_score(score, font):
	position = (5, len(current_level)*tilesize + 30)
	rendered_score = font.render("score: "+ str(score), True, "black")
	score_rect = rendered_score.get_rect(topleft = position)
	screen.fill("white", score_rect)
	screen.blit(rendered_score, score_rect)
	return score_rect
	
def getrects(snakebody, food):
	positions = snakebody.copy()
	positions.append(food)
	rectlist = []
	for box in positions:
		x = box[0] * tilesize
		y = box[1] * tilesize
		boxrect = pg.Rect((x, y, tilesize, tilesize))
		rectlist.append(boxrect)
	return rectlist
	
	
#______________________________________

#classes

class Snake():
	def __init__(self, headcolor, initiallength):
		
		maxgridsize = max(len(current_level), len(current_level[0]))
		self.tilesize = GRIDLENGTH//maxgridsize
		self.x_gridsize, self.y_gridsize = self.setgridsize()
		self.body = [[self.x_gridsize//2, self.y_gridsize//2]]
		for i in range(initiallength):
			self.body.append([self.body[i][0] + 1, self.body[0][1]])
		self.allowing_movement = False
		self.dx = -1
		self.dy = 0
		self.direction = "left"
		self.headcolor = headcolor
		self.offset = 0
		self.BOXSIZE = self.tilesize - self.offset
		self.food = self.generate_food()
	
	def setgridsize(self):
		return len(current_level[0]), len(current_level)
	
	def collision(self, head):
		x = 0
		y = 1
		for box in self.body[1:len(self.body)]:
			if box[x] == head[x] and box[y] == head[y]:
				return True
		else:
			return False
	
	
	def collision_with_wall(self):
		x = self.body[0][0]* self.tilesize
		y = self.body[0][1]* self.tilesize
		head_row = int(y//self.tilesize)
		head_col = int(x//self.tilesize)
		value = current_level[head_row][head_col]
		if value != 0:
			return True
		else:
			return False
			
			
	def collision_with_food(self):
		if (self.body[0][0]) == self.food[0] and (self.body[0][1]) == self.food[1]:
			return True
		else:
			return False
						
						
	def addbox(self):
		# adding a box to body
		self.body.append([0, 0])
		self.food = self.generate_food()
	
	
	def generate_food(self):
		# making sure food doesnt appear inside snake body or wall
		while True:
			random_x = random.randint(0, self.x_gridsize-1)
			random_y = random.randint(0, self.y_gridsize-1)
			for box in self.body:
				x = box[0]
				y = box[1]
				if random_x == x and random_y == y:
					break
				elif current_level[random_y][random_x] != 0:
					break
			else:
				return [random_x, random_y]
				break
					
					
	def reset(self):
			global score
			score = 0
			self.body = [[int(self.x_gridsize/2) if self.x_gridsize%2 == 0 else (self.x_gridsize+1)/2, self.y_gridsize/2 if self.y_gridsize%2 == 0 else (self.y_gridsize+1)/2]]
			for i in range(initial_length):
				self.body.append([self.body[i][0] + 1, self.body[0][1]])
			
			maxgridsize = max(len(current_level), len(current_level[0]))
			self.tilesize = GRIDLENGTH//maxgridsize
			self.x_gridsize, self.y_gridsize = self.setgridsize()
			self.food = self.generate_food()
			self.dx = -1
			self.dy = 0
			self.direction = "left"
			self.allowing_movement = False
			
			
	def move(self):
		global score
		
		if self.allowing_movement:
			unchangedbody = [box[:] for box in self.body]
			self.body[0][0] += self.dx
			self.body[0][1] += self.dy
			
			# making boundaries teleporters
			if self.body[0][0] < 0:
				self.body[0][0] = self.x_gridsize-1
			if self.body[0][0] > self.x_gridsize-1:
				self.body[0][0] = 0
			if self.body[0][1] < 0:
				self.body[0][1] = self.y_gridsize-1
			if self.body[0][1] > self.y_gridsize-1:
				self.body[0][1] = 0
			#___________________________
			
			#checking collision with food
			if self.collision_with_food():
				self.addbox()
				eating_sound.play()
				self.haseatenfood = True
				score += 1
				
			#checking collision with wall
			if self.collision_with_wall():
				death_sound.play()
				self.reset()
				return
				
			#checking collision with itself	
			if not self.collision(self.body[0]):
				for i in range(1, len(self.body)):
					self.body[i][0] = unchangedbody[i-1][0]
					self.body[i][1] = unchangedbody[i-1][1]
			else:
				death_sound.play()
				self.reset()
				return			
				
	
	def turn(self, d):
			direction = d.strip().lower()
			if self.direction != direction:
				if direction == "left" and self.direction!="right":
					self.dx = -1
					self.dy = 0
				elif direction == "right" and self.direction != "left":
					self.dx = 1
					self.dy = 0
				elif direction == "down" and self.direction != "up":
					self.dx = 0
					self.dy = 1
				elif direction == "up" and self.direction != "down":
					self.dx = 0
					self.dy = -1
				self.direction = direction
				
			
	def show(self):
		for box in self.body:
			#  calculating dist to create gradient
			dist = self.body.index(box)*(255/len(self.body))
			
			box_x = (box[0]* self.tilesize) + self.offset/2
			box_y = (box[1]* self.tilesize) + self.offset/2
			
			pg.draw.rect(screen, (self.headcolor[0]*255 - self.headcolor[0]*dist, self.headcolor[1]*255 - self.headcolor[1]*dist, self.headcolor[2]*255 - self.headcolor[2]*dist), (box_x, box_y, self.BOXSIZE, self.BOXSIZE))
#		
		pg.draw.circle(screen, "red", (self.food[0] * self.tilesize + self.BOXSIZE/2 + self.offset/2, self.food[1] * self.tilesize + self.BOXSIZE/2 + self.offset/2), self.BOXSIZE/2)

#________________________________________

snake = Snake(snake_headcolor, initial_length)
drawlevel(level_surface, current_level)

framecount = 0
running = True

while running:
	framecount += 1
	clock.tick(framerate)
	mx, my = pg.mouse.get_pos()
	events = pg.event.get()
	for event in events:
		if event.type == pg.QUIT:
			running = False
			break
		if event.type == pg.FINGERDOWN:
			for button in buttons:
				x, y = button[0],button[1]
				dir = button[2]
				if x+bw > mx > x and y+bh > my > y:
					snake.allowing_movement = True
					snake.turn(dir)
	
	screen.fill("white")
	
	screen.blit(level_surface, (0, 0))
	snake.show()
	display_score(score, font)
	draw_buttons()
					
	#______________________________________
	
	# Level changing logic
	if score > (level_index+1)*5:
		new_level_sound.play()
		increase_level()
		snake.reset()
		#updating level specific variables
		gridsize = max(len(current_level), len(current_level[0]))
		tilesize = GRIDLENGTH//gridsize
		level_surface = pg.Surface((len(current_level[0])*tilesize, len(current_level*tilesize)))
		drawlevel(level_surface, current_level)
	
	#____________________________________
	
	# Speed controlling logic
	if framecount >= framerate/snakespeed:
		snake.move()
		framecount = 0
	#______________________________
	
	
	pg.display.update()