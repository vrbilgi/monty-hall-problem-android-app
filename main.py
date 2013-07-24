# Montly Hall problem statement and illustration
#  	wiki: http://en.wikipedia.org/wiki/Monty_Hall_problem 
#  	Link: http://kcs-rijtuigen.nl/hb/xjlaldlnjnafdbvdpilrxrrsci  


#  Here we are using layered approach  
#  	pygame layer involves  Door and  Dicision
#  	Dicision object can be goat or car

#  	For there Doors we are using three pygame layeres

#  on Click of the Door we are opening Door ie 
#  	we are bring Dicision object behing the Door

import pygame
import random
import sys

try:
    import android
except ImportError:
    android = None



WHITE = (255, 255, 255)
FILE_TYPE = "png"
WINDOW_SIZE = (500, 500)
DOOR_X = 100
DOOR_Y = 100

class Door(pygame.sprite.Sprite):

	def __init__(self, image, pos_x, pos_y, object_name ):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(image)
		self.rect = self.image.get_rect()

		self.rect.x = pos_x
		self.rect.y = pos_y
		self.object_name = "Door"


class Dicision(pygame.sprite.Sprite):

	def __init__(self, image_index, pos_x, pos_y):
		pygame.sprite.Sprite.__init__( self )

		image_list = ("goat1","goat2","car")

		self.image = pygame.image.load(image_list[image_index]+".png")
		self.image = pygame.transform.scale(self.image, (70,70))

		self.rect = self.image.get_rect()
		self.rect.x = pos_x
		self.rect.y = pos_y

		self.object_name = image_list[image_index]


class Game:

	def __init__(self):

		print "I am in ctor of Game"

		pygame.init()
		pygame.display.set_caption("Monty Hall")

		self.window = pygame.display.set_mode((500, 500)) 
		self.surface = pygame.Surface((500, 500))
	
		self.layer1 = pygame.sprite.LayeredUpdates()
		self.layer2 = pygame.sprite.LayeredUpdates()
		self.layer3 = pygame.sprite.LayeredUpdates()

		#button.png and Font start make the Start Button
		self.start_button = pygame.image.load("button.png")
		self.start_button = pygame.transform.scale(self.start_button, (100, 40))
		self.start_button=self.window.blit(self.start_button, (180, 200))

		print "I about to load font"
		self.my_font= pygame.font.Font("comic.ttf", 40)
		print "I have loaded font"
		start=self.my_font.render("start", 1, WHITE)
		self.window.blit(start, (200, 205))
		#button.png and Font start make the Start Button
	
		self.exit_button = pygame.image.load("exit.png")
		self.exit_button = pygame.transform.scale(self.exit_button, (70, 70))
		self.exit_button = self.window.blit(self.exit_button, (425, 425))

		self.my_font.set_underline(1)
		headder=self.my_font.render("Monty Hall Problem", 1, WHITE)
		self.my_font.set_underline(0)
		self.window.blit(headder, (100, 20))

		
	def start_game(self):
		''' This funciton is responsible do all the pre-requisite 
		required to run the game from beginning. 
 		
		clear  old traces of the game window
		prepare layer and list to hold objects

		create Door and Dicision object (random) and add to layer
		Dicision objects are will load randomly goat, goat and car
		'''
		self.choice = 0

		surface_clear_door = pygame.Surface((300, 75))
		surface_clear_message = pygame.Surface((350, 200))

		self.window.blit(surface_clear_door, (100, 100))
		self.window.blit(surface_clear_message, (75, 275))

		self.layer1.empty()
		self.layer2.empty()
		self.layer3.empty()

		self.list = []

		random_list = random.sample(range(3), 3)

		self.layer1.add(Dicision(random_list[0], 100, 100))
		self.layer1.add(Door("red.png", DOOR_X, DOOR_Y, random_list[0]))

		self.layer2.add(Dicision(random_list[1], 200, 100))
		self.layer2.add(Door("green.png", DOOR_X+100, DOOR_Y, random_list[1]))

		self.layer3.add(Dicision(random_list[2], 300, 100))
		self.layer3.add(Door("blue.png", DOOR_X+200, DOOR_Y, random_list[2]))

		self.list.append(self.layer1) 
		self.list.append(self.layer2) 
		self.list.append( self.layer3 ) 

		print random_list
		for layer in self.list:
			layer.draw(self.window)	
	


		self.show_host_instructions()
		pygame.display.update()

	def open_other_door(self, second_list): 
		''' When user selects one door. Open other door which has goat
		As we are using layering approach are bringing Dicision object to front layer
		'''

		for layer in second_list:
			for sprite in layer:
				if isinstance(sprite, Dicision): 
					if sprite.object_name == "goat1" or sprite.object_name == "goat2":
						layer.move_to_front(sprite)

						dirty=layer.draw(self.window)	
						pygame.display.update(dirty)

						return


	def main(self):
		''' This is our game loop
		start game
		wait for user input:	
			Quit on QUIT			
			Quit on exit
			Handle Click	'''

		self.start_game()
		#pygame.display.update()


		if android:
		    android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)

		run = True
		while run:
			if android:
			    if android.check_pause():
				android.wait_for_resume()
						
			for event in pygame.event.get():
				pos = pygame.mouse.get_pos()

				if event.type == pygame.QUIT:
					run = False

				if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
					second_list=[]

					if self.click_start( pos ):
						#optimize here
						continue
					elif self.exit_button.collidepoint(pos):
						sys.exit()
					else:	
						self.handle_choice(pos, second_list)
	def handle_second_choice(self, pos):
		''' When user selects the door second time, 	
		move is Dicision object to front and return layer
		for calculating display_result '''

		second_choice_door=[]
		self.choice = 2			

		for layer in self.list:
			for sprite in layer:
				if sprite.rect.collidepoint(pos) and isinstance(sprite, Door):
					second_choice_door.append(layer)	
			
				if isinstance(sprite, Dicision): 
					layer.move_to_front(sprite)

					dirty = layer.draw(self.window)	
					pygame.display.update(dirty)
		return second_choice_door

	def display_result(self,second_choice_door):
		''' This funciton handles two responsibility 
			make the juidgement on result
			Does the formating of result '''

		surface_clear_message = pygame.Surface((400, 150))
		self.window.blit(surface_clear_message, (75, 275))
		pygame.display.update()

		for layer in second_choice_door:
			for sprite in layer: 
				if isinstance(sprite, Dicision):
					if sprite.object_name == "car":
						win_text = self.my_font.render("You Won         Car !!!", 1, WHITE)
					else:
						win_text = self.my_font.render("   Goat is        yours :D ", 1, WHITE)

					joker = pygame.image.load("joker.png")

					self.window.blit(joker, (175, 275))
					self.window.blit(win_text, (90, 375))

					pygame.display.update()

	def handle_choice(self, pos, second_list):
		''' This funciton behaves as state machine for user choice 
		choice = 0  No choice it will be the first choice
		choice = 1  This will be the second click ''' 

		if self.choice == 1:
			second_choice_door = self.handle_second_choice(pos)
			self.display_result(second_choice_door)
		if self.choice == 0:
			self.handle_first_choice(pos, second_list)			
		if self.choice == 1:
			self.show_host_instructions()
			self.open_other_door(second_list)

	def show_host_instructions(self):

		surface_clear_message = pygame.Surface((400, 150))
		self.window.blit(surface_clear_message, (50, 275))
		pygame.display.update()

		if self.choice == 0:
			self.my_font.set_italic(1)
			instruction_one = self.my_font.render("Behind one door is a car", 1, WHITE)
			instruction_two = self.my_font.render("Behind the others, goats", 1, WHITE)
			self.my_font.set_italic(0)
			self.window.blit(instruction_one, (75, 300))
			self.window.blit(instruction_two, (75, 350))
			pygame.display.update()

		if self.choice == 1:
			self.my_font.set_italic(1)
			instruction_one = self.my_font.render("Do you want to pick other", 1, WHITE)
			instruction_two = self.my_font.render("            !!! door !!!", 1, WHITE)
			self.my_font.set_italic(0)
			self.window.blit(instruction_one, (75, 300))
			self.window.blit(instruction_two, (75, 350))
			pygame.display.update()

	def handle_first_choice(self, pos, second_list):
		''' In this funcition 
		add other layers to second_list which does not 
			had a click on it( or not choosen ) '''

		for layer in self.list:
			add = 0	
			for sprite in layer:
				if sprite.rect.collidepoint(pos):
					add = 1
					self.choice = 1			
			if add ==0:
				second_list.append(layer)


	def click_start(self, pos):
		''' on click of start button start the game 			
		@return True on click on start button 
			False otherwise '''

		if self.start_button.collidepoint(pos):					
			self.start_game()
			return True
				
		return False 

if __name__ == "__main__":

	print "I am in main 1"
	game = Game()
	print "I am in main 2"
	game.main()
	print "I am in main 3"


