class coord(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y
	def __str__(self):
		return "%d - %d" % (self.x, self.y)

def gotoxy(x, y):
	print ("%c[%d;%df" % (0x1B, y, x), end='')

class _Getch:
	def __init__(self):
		import tty, sys
	def __call__(self):
		import sys, tty, termios
		global fd
		global old_settings
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		try:
			tty.setraw(sys.stdin.fileno())
			ch = sys.stdin.read(1)
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
		return ch

def get_rand():
	import random
	return random.randint(3, 17)

height = 20
width = 40

import threading
class obstacle_move(threading.Thread):
	def __init__(self, pos):
		threading.Thread.__init__(self)
		self.pos = pos

	def run(self):
		global height
		global width
		temp_w = width
		while temp_w >= 2:
			offset = 2
			if abs(temp_w - width) == 10:
				o = obstacle_move(get_rand())
				o.start()	
			for i in range(0+offset, self.pos-1+offset):
				gotoxy(temp_w, i)
				print("*")
			for i in range(self.pos+1+offset, height+offset):
				gotoxy(temp_w, i)
				print("*")
			import time
			time.sleep(0.5)
			for i in range(0+offset, self.pos-1+offset):
				gotoxy(temp_w, i)
				print(" ")
			for i in range(self.pos+1+offset, height+offset):
				gotoxy(temp_w, i)
				print(" ")
			temp_w -= 2

def draw():
	for i in range(0, width+2):
		print('*', end='')
	print('')
	for j in range(0, height):
		print('*', end='')
		for i in range(0, width): print(' ', end='')
		print('*', end='')
		print('')
	for i in range(0, width+2):
		print('*', end='')

if __name__ == '__main__':
	import os
	os.system("clear")

	draw()

	gotoxy(20,10)
	print("@")
	
	pos = get_rand()
	o = obstacle_move(pos)
	o.start()
