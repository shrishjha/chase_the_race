import pygame
import time
import random
#gamehere
pygame.init()

display_width=900
display_height=750

black=(0,0,0)
white=(255,255,255)
red=(255,0,0)
green=(0,255,0)
blue=(0,0,255)
color_list=[black,red,blue,green]

car_width=65
car_height=140

gameDisplay=pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('CAR CRUNCH')
clock=pygame.time.Clock()

carImg=pygame.image.load("scarunit.jpg")

def level_dodged(dodged,level):
	#level and color change
	if dodged%4==0:
		level+=1
		#color=random.choice(color_list)
	return level


def things(thingx,thingy,thingw,thingh,color):
	pygame.draw.rect(gameDisplay,color,[thingx,thingy,thingw,thingh])


def car(x,y):
	gameDisplay.blit(carImg,(x,y))

def text_objects(text,font):
	textSurface=font.render(text,True,red)
	return textSurface, textSurface.get_rect()

def message_display(text):
	largeText=pygame.font.Font('freesansbold.ttf',50)
	TextSurf, TextRect=text_objects(text,largeText)
	TextRect.center=((display_width/2),(display_height/2))
	gameDisplay.blit(TextSurf,TextRect)

	pygame.display.update()


def crash():
	message_display("YOU CRASHED!")
	time.sleep(2)
	game_loop()


def life_display(life,color):
	lifefont=pygame.font.SysFont(None,35)
	lifetext=lifefont.render("Life: "+str(life),True,color)
	gameDisplay.blit(lifetext,(display_width/2,10))


def things_dodged(count,color):
	font=pygame.font.SysFont(None,35)
	text=font.render("Dodged: "+str(count),True,color)
	gameDisplay.blit(text,(10,10))

def game_level(level,color):
	levelfont=pygame.font.SysFont(None,35)
	leveltext=levelfont.render("Level: "+str(level),True,color)
	level_width=leveltext.get_width()
	gameDisplay.blit(leveltext,(display_width-level_width-10,10))


def game_loop():

	y=display_height*0.75
	x=display_width*0.45

	dodged=0
	level=1
	life=0

	gameExit=False

	x_change=0
	list=[] #using as a stack for car movement
	length=0 #length of list
	color=(0,0,0)
	

	#for obrstructive moving things
	thing_width=70
	thing_height=120
	thing_speed=10
	
	thing_startx=random.randrange(0,display_width-thing_width)
	thing_starty=-600
	
	

	lifething_width=thing_width
	lifething_height=thing_height
	lifething_startx=random.randrange(0,display_width-thing_width)
	lifething_starty=-750*12

	greenthing_width=thing_width
	greenthing_height=thing_height
	greenthing_startx=random.randrange(0,display_width-thing_width)
	greenthing_starty=-750*7




	while not gameExit:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			#car movement code
			if event.type == pygame.KEYDOWN:
				if event.key==pygame.K_LEFT:
					if length==0 or list[length-1]!=-1: 
						list.append(-1)
						length+=1
					x_change=-5
					
				if event.key==pygame.K_RIGHT:
					if length==0 or list[length-1]!=1:
						list.append(1)
						length+=1
					x_change=5

			if event.type == pygame.KEYUP:
				if length==0:
						x_change=0
			
				elif length==1:
					if event.key==pygame.K_LEFT:
						if list[0]==1:
							x_change=5
						elif list[0]==-1:
							list.pop()
							length-=1
							x_change=0
					if event.key==pygame.K_RIGHT:
						if list[0]==-1:
							x_change=-5
						elif list[0]==1:
							list.pop()
							length-=1
							x_change=0

				elif length==2:
					if event.key==pygame.K_LEFT:
						list.remove(-1)
						length-=1
						x_change=5
					if event.key==pygame.K_RIGHT:
						list.remove(1)
						length-=1
						x_change=-5



		x+=x_change
		thing_starty+=thing_speed
		lifething_starty+=thing_speed
		greenthing_starty+=thing_speed

		#lifethings regenerate
		if lifething_starty>display_height:
			lifething_starty=random.randrange(-16*display_height,-12*display_height)
			lifething_startx=random.randrange(0,display_width-thing_width)


		#greenthings regenerate
		if greenthing_starty>display_height:
			greenthing_starty=random.randrange(-14*display_height,-10*display_height)
			greenthing_startx=random.randrange(0,display_width-thing_width)


		#things regenerate	
		if thing_starty>display_height:
			thing_starty=0-thing_height
			thing_startx=random.randrange(0,display_width-thing_width)

			#to avoid things regenerating on life things
			if lifething_starty<0 and lifething_starty>(0-thing_height) and thing_startx>(lifething_startx-thing_width) and thing_startx<(lifething_startx+thing_width):
				thing_starty=-2*thing_width

			#to avoid things regenerating on green things
			if greenthing_starty<0 and greenthing_starty>(0-thing_height) and thing_startx>(greenthing_startx-thing_width) and thing_startx<(greenthing_startx+thing_width):
				thing_starty=-2*thing_width
			
			#dodged score
			dodged+=1
			level=level_dodged(dodged,level)
			
			#difficulty level increase by changing speed for each even level
			if level%2==0:
				thing_speed+=2

			
		
		#crashed by life things
		if y<=lifething_starty+lifething_height and y+car_height>=lifething_starty: 
				# x coordinates crossover
			if x>=lifething_startx and x<=lifething_startx+lifething_width or x+car_width>=lifething_startx and x+car_width<=lifething_startx+lifething_width or lifething_startx>=x and lifething_startx+lifething_width<=x+car_width:
				life=life+1
				#disappear
				lifething_starty=random.randrange(-600*6,-600*5)
				lifething_startx=random.randrange(0,display_width-thing_width)


		#crashed by green things
		if y<=greenthing_starty+greenthing_height and y+car_height>=greenthing_starty: 
				# x coordinates crossover
			if x>=greenthing_startx and x<=greenthing_startx+greenthing_width or x+car_width>=greenthing_startx and x+car_width<=greenthing_startx+greenthing_width or greenthing_startx>=x and greenthing_startx+greenthing_width<=x+car_width:
				dodged+=2
				level=level_dodged(dodged,level)
				thing_speed-=thing_speed/4
				#disappear
				greenthing_starty=random.randrange(-600*7,-600*4)
				greenthing_startx=random.randrange(0,display_width-thing_width)


		#crashed by walls
		if x<0 or x+car_width>display_width:
			if life<=0:
				crash()
			else:
				life=life-1
				#to use only one life for one crash
				x=(display_width-car_width)/2
				thing_starty=0-thing_height
				thing_startx=random.randrange(0,display_width-thing_width)

		#crashed by other cars
			# y coordinates crossover
		if y<=thing_starty+thing_height and y+car_height>=thing_starty: 
				# x coordinates crossover
			if x>=thing_startx and x<=thing_startx+thing_width or x+car_width>=thing_startx and x+car_width<=thing_startx+thing_width or thing_startx>=x and thing_startx+thing_width<=x+car_width:
				if life<=0:
					crash()
				else:
					life=life-1
					#disappear
					thing_starty=0-thing_height
					thing_startx=random.randrange(0,display_width-thing_width)
				

		#new frame starts here
		gameDisplay.fill(white)

		car(x,y)
		things_dodged(dodged,blue)
		life_display(life,red)
		game_level(level,blue)
		things(lifething_startx,lifething_starty,lifething_width,lifething_height,red)
		things(greenthing_startx,greenthing_starty,greenthing_width,greenthing_height,green)
		things(thing_startx,thing_starty,thing_width,thing_height,black)
		


		pygame.display.update() #applies all the updates made to the frame by updating full frame display
		clock.tick(60)

game_loop()