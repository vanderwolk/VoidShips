import pygame as pg
import pytweening as tween
from settings import *
from textures import *


class Item(pg.sprite.Sprite):
	def __init__(self, game, x, y, item):
		self._layer = ITEM_LAYER
		self.groups = game.all_sprites, game.items
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.item = item
		self.image = ITEMS[item]
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y
		self.tilepos = (x,y)
		self.pos = vec(x, y) * TILESIZE
		self.rect.centerx = self.pos.x + TILESIZE/2
		self.rect.centery = self.pos.y + TILESIZE/2
		self.chunkpos = (int(x / CHUNKSIZE), int(y / CHUNKSIZE))
		self.tween = tween.easeInOutSine
		self.dir = 1
		self.step = 0

	def update(self):
		offset = BOB_RANGE * (self.tween(self.step / BOB_RANGE) - 0.5)
		self.rect.centery = self.pos.y + offset * self.dir
		self.step += BOB_SPEED
		if self.step > BOB_RANGE:
			self.step = 0
			self.dir *= -1
