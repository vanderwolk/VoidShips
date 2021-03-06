import pygame as pg
from settings import *
from settings import collide_hit_rect
from textures import *

# Collide with the passed group of tiles
def collide_with_walls(sprite, group, dir):
	if dir == "x":
		hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
		if hits:
			# From the left side
			if hits[0].rect.centerx > sprite.hit_rect.centerx:
				sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
			# From the right side
			if hits[0].rect.centerx < sprite.hit_rect.centerx:
				sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
			sprite.vel.x = 0
			sprite.hit_rect.centerx = sprite.pos.x
	if dir == "y":
		hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
		if hits:
			# From bottom
			if hits[0].rect.centery > sprite.hit_rect.y:
				sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height - sprite.hitrect_offset
			# From top
			if hits[0].rect.centery < sprite.hit_rect.y:
				sprite.pos.y = hits[0].rect.bottom - sprite.hitrect_offset
			sprite.vel.y = 0
			sprite.hit_rect.y = sprite.pos.y + sprite.hitrect_offset

class Player(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		self._layer = PLAYER_LAYER
		self.groups = game.all_sprites
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.img = PLAYER_IMG
		self.image = self.img
		self.rect = self.image.get_rect()
		self.hit_rect = PLAYER_HITRECT
		self.hitrect_offset = 12
		self.vel = vec(0,0)
		self.pos = vec(x, y) * TILESIZE
		self.tilepos = vec(int(self.pos.x / TILESIZE), int(self.pos.y / TILESIZE))
		self.chunkpos = self.tilepos * CHUNKSIZE
		self.name = PLAYER_DEFAULT_NAME
		self.on_inv = false
		self.holding = null
		self.hotbar_display = {
		0 : null,
		1 : null,
		2 : null
		}
		self.inv_display = {
		0 : null,
		1 : null,
		2 : null,
		3 : null,
		4 : null,
		5 : null,
		6 : null,
		7 : null,
		8 : null
		}
		self.selected_slot = 0
		# Create new inventory ──────────────────────────────────────────────────────────────────────────
		self.selected_slot = 0
		self.fullinv = DEFAULT_WORLD_FORMAT["player"]["fullinv"]
	# Load the data passed from the create() function in main.py
	def load_data(self, data):
		self.playerdata = data
		self.pos = vec(data["pos"])
		self.tilepos = vec(int(self.pos.x / TILESIZE), int(self.pos.y / TILESIZE))
		self.chunkpos = self.tilepos * CHUNKSIZE
		self.name = data["name"]
		# Load inventory ────────────────────────────────────────────────────────────────────────────────
		self.selected_slot = data["selected_slot"]
		self.fullinv = data["fullinv"]
	# Save the player"s data
	def save_data(self):
		print("Saving player data")
		self.playerdata.update({
		"pos" : tuple(self.pos),
		"name" : self.name,
		"selected_slot" : self.selected_slot,
		"fullinv": self.fullinv
		})
		return self.playerdata
	# Get input for player movement
	def get_keys(self):
		self.vel = vec(0,0)
		keys = pg.key.get_pressed()
		# if not self.on_inv:
		if keys[pg.K_LEFT] or keys[pg.K_a]:
			self.vel.x = -PLAYER_SPEED
		if keys[pg.K_RIGHT] or keys[pg.K_d]:
			self.vel.x = PLAYER_SPEED
		if keys[pg.K_UP] or keys[pg.K_w]:
			self.vel.y = -PLAYER_SPEED
		if keys[pg.K_DOWN] or keys[pg.K_s]:
			self.vel.y = PLAYER_SPEED
		if self.vel.x != 0 and self.vel.y != 0:
			self.vel *= 0.7071
	# Update the player values
	def update(self):

		self.get_keys()
		self.rect = self.image.get_rect()
		self.rect.center = self.pos
		self.pos += self.vel * self.game.delta

		# Flip the player's image depending on its velocity
		if self.vel.x < 0:
			self.image = pg.transform.flip(self.img, true, false)
		if self.vel.x > 0:
			self.image = self.img

		# Move the player and collide if necesary
		self.hit_rect.centerx = self.pos.x
		if PLAYER_COLLIDE:
			collide_with_walls(self, self.game.collidables, "x")
		self.hit_rect.y = self.pos.y + self.hitrect_offset
		if PLAYER_COLLIDE:
			collide_with_walls(self, self.game.collidables, "y")

		# Move the player's rect with its position
		self.rect.center = self.pos

		# Find the position measured in tiles or chunks of the player
		self.tilepos = vec(int(self.pos.x / TILESIZE), int(self.pos.y / TILESIZE))
		self.chunkpos = vec(int(self.tilepos.x / CHUNKSIZE), int(self.tilepos.y / CHUNKSIZE))

		# Limit the player movement to the positive side of the grid
		if self.pos.x < XLIMIT:
			print("You have reached the edge of the world!")
			self.pos.x = XLIMIT
		if self.pos.y < YLIMIT:
			print("You have reached the edge of the world!")
			self.pos.y = YLIMIT
