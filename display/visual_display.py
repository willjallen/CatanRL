import os
import pygame as pg
import thorpy
import math



class VisualDisplay:
	def __init__(self):

		self.tile_vertices = [[[]]]


		pg.init()
		self.screen = pg.display.set_mode((480, 480), pg.SCALED | pg.RESIZABLE)
		pg.display.set_caption("Monkey Fever")
		# pg.mouse.set_visible(False)
		background = pg.Surface(screen.get_size())
		background = background.convert()
		background.fill((170, 238, 187))
		screen.blit(background, (0, 0))
		pg.display.flip()

		clock = pg.time.Clock()

		hex_vertices = []

		for i in range(0,6):
			hex_vertices.append((100 + math.cos(i/6.0*2*math.pi)*20, 100 + math.sin(i/6.0*2*math.pi)*20));


	def calculate_hex_vertices(self):
		pass

	def calculate_containers(self):
		pass


	def render(self):
		pg.draw.aalines(pg.display.get_surface(), 255, True, hex_vertices)

	def main(self):
		going = True
		while going:
			clock.tick(60)

			# Handle Input Events
			for event in pg.event.get():
				if event.type == pg.QUIT:
					going = False
				elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
					going = False
				elif event.type == pg.VIDEORESIZE:
					# screen.blit(pygame.transform.scale(pic, event.dict['size']), (0, 0))
					pg.display.update()

			screen.blit(background, (0, 0))
			self.render()
			pg.display.flip()
			


VisualDisplay()