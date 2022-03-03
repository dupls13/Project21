
#Package imports 
import math
import pygame
import sys

from pygame.sprite import Sprite


clock = pygame.time.Clock()
bullets = []


class Settings:
	def __init__(self):
		#Screen settings
		self.SCREEN_WIDTH = 1000
		self.SCREEN_HEIGHT = 600
		self.WHITE = (255, 255, 255)

#---------------Environment 
#---------------Obstacles

class Player:
	def __init__(self, P22_game):
		PLAYER_WIDTH, PLAYER_HEIGHT = (70, 50)

		#Screen rectangle 
		self.screen = P22_game.screen
		self.settings = P22_game.Settings
		self.screen_rect = P22_game.screen.get_rect()


		#Load player image
		self.imageload = pygame.image.load('player.png')
		self.image = pygame.transform.scale(self.imageload, (PLAYER_WIDTH, PLAYER_HEIGHT))
		self.rect = self.image.get_rect()

#------------------------Player rotate

		#Player initial position 
		self.rect.midbottom = self.screen_rect.midbottom 

		#Decimal value for player horizontal and vertical position 
		self.x = float(self.rect.x)
		self.y = float(self.rect.y)

		#Movement flags
		self.moving_left = False
		self.moving_right = False
		self.moving_up = False
		self.moving_down = False

	def update(self):
		#Update player movement flags 
		if self.moving_left and self.rect.left > 0 :
			self.rect.x -= 5 
		if self.moving_right and self.rect.right < self.settings.SCREEN_WIDTH:
			self.rect.x += 5
		if self.moving_up and self.rect.top > 0:
			self.rect.y -= 5
		if self.moving_down and self.rect.bottom < self.settings.SCREEN_HEIGHT:
			self.rect.y += 5

	def blitme(self):
		#Puts image on screen 
		self.screen.blit(self.image, self.rect)

class Bullet(Sprite):
	def __init__(self, P22_game):
		super().__init__()

		#Sets bullet location equal to player location 
		self.x = P22_game.Player.rect.x + 35
		self.y = P22_game.Player.rect.y + 35

 
		self.screen = P22_game.screen
		self.settings = P22_game.Settings

		#Bullet position origin
		self.origin = P22_game.Player.rect.midbottom 

		#Store bullet x and y position 
		self.x = float(self.x)
		self.y = float(self.y)

		#Get mouse x and y 
		mouse_x, mouse_y = pygame.mouse.get_pos()
		self.mouse_x = mouse_x
		self.mouse_y = mouse_y 

		#Bullet Settings
		self.lifetime = 50
		self.speed = 15
		self.angle = math.atan2(mouse_y - self.y, mouse_x - self.x )
		self.x_vel = math.cos(self.angle) * self.speed
		self.y_vel = math.sin(self.angle) * self.speed
		self.radius = 5

	def update(self):
		#Update bullet position 
		self.x += int(self.x_vel)
		self.y += int(self.y_vel)

	def draw_bullet(self):
		#Draw bullet onto screen 
		pygame.draw.circle(self.screen , (0, 0, 0), (self.x, self.y), self.radius)
		self.lifetime -=1


#------------------Enemies



#Game file 
class Project22:
	def __init__(self):
		pygame.init()
		pygame.display.set_caption("Project22")

		self.Settings = Settings()

		self.screen = pygame.display.set_mode(
			(self.Settings.SCREEN_WIDTH, self.Settings.SCREEN_HEIGHT))

		self.Player = Player(self)
		self.Bullet = pygame.sprite.Group()
		

	def run_game(self):
		FPS = 60
		while True:
			x, y = pygame.mouse.get_pos()
			clock.tick(FPS)

			self._update_screen()
			self.Player.update()
			self.Bullet.update()
			self._check_events()


	def _check_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
				pygame.quit()


			#Movement keys 
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_a:
					self.Player.moving_left = True 
				if event.key == pygame.K_d:
					self.Player.moving_right = True
				if event.key == pygame.K_w:
					self.Player.moving_up = True
				if event.key == pygame.K_s:
					self.Player.moving_down = True

			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_a:
					self.Player.moving_left = False
				if event.key == pygame.K_d:
					self.Player.moving_right = False
				if event.key == pygame.K_w:
					self.Player.moving_up = False
				if event.key == pygame.K_s:
					self.Player.moving_down = False


			#Bullet controls and works 		
			elif event.type == pygame.MOUSEBUTTONDOWN:
				self._fire_bullet()
				

			for bullet_ in bullets:
				if bullet_lifetime <= 0:
					bullets.pop(bullet.index(bllet_))
				bullet_.draw(screen)


	def _fire_bullet(self):
		new_bullet = Bullet(self)
		self.Bullet.add(new_bullet)


	def _update_screen(self):
		self.screen.fill(self.Settings.WHITE)
		self.Player.blitme()
		for Bullet in self.Bullet.sprites():
			Bullet.draw_bullet()

		pygame.display.flip()


if __name__ == "__main__":
	P22 = Project22()
	P22.run_game()

