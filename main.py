from numba.typed import List
from numba import njit, prange
from numpy import dot, array
import time


w = h = size = 700
uvel = 1
speed = 0.05

mx = [float(0), float(2)] # x zoom !zoom == zoom!
my = [float(0), float(2)] # y zoom !zoom == zoom!

xz = 1
yz = -3
xc = 2
yc = 5


class fractal():
	@staticmethod
	@njit(fastmath=True, parallel = True)
	def render(arr, mx, my):
		for x in prange(w):
			for y in prange(h):
				z = 0
				c = mx[0]+mx[1]*2*(x/w)-mx[1] + 1j * (my[0]+my[1]*2*(y/h)-my[1])
				#print(c)
				for i in prange(255):
					z = z ** 2 + c
					if z.real ** 2 + z.imag ** 2 > 4: # or abs(z) > 4
						arr[x][y] = i
						break
				else:
					arr[x][y] = 0
		return arr


f = fractal()


import pygame as pg
import random as r
import time
import numpy as np

old_time = time.time()
delta_time = 1 # time.time() to 60 fps
FPS = 60
WIDTH = w*uvel
HEIGHT = h*uvel

img = pg.Surface((w, h))
img2arr = pg.surfarray.array2d(img)

sc = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE)

old_WIDTH, old_HEIGHT = sc.get_size()

clock = pg.time.Clock()
pg.display.set_caption("mandel")

while True:

	delta_time = (time.time()-old_time)*60
	old_time = time.time()

	keys = pg.key.get_pressed()

	for event in pg.event.get():
		if event.type == pg.QUIT:
			exit()

	if old_WIDTH != WIDTH or old_HEIGHT != HEIGHT:
		old_WIDTH, old_HEIGHT = sc.get_size()
	WIDTH, HEIGHT = sc.get_size()

	if keys[pg.K_a]:
		mx[0] += -speed*mx[1]
	if keys[pg.K_d]:
		mx[0] += speed*mx[1]
	if keys[pg.K_w]:
		my[0] += -speed*my[1]
	if keys[pg.K_s]:
		my[0] += speed*my[1]
	if keys[pg.K_q]:
		mx[1] = mx[1]*0.9
		my[1] = my[1]*0.9
	if keys[pg.K_e]:
		mx[1] = mx[1]*1.1
		my[1] = my[1]*1.1

	sc.fill((24, 20, 37))

	img2arr = f.render(img2arr, mx, my)

	pg.surfarray.blit_array(sc, img2arr)

	pg.display.set_caption(str(round(clock.get_fps())))
	pg.display.flip()
	clock.tick(FPS)