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
getch = _Getch()


def end_game():
	global fd
	global old_settings
	global alive
	import termios
	termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

	import os
	os.system("clear")
	gotoxy(0, 0)
	print("Game Ends ! ")

	alive = False
	import sys
	sys.exit(0)

def get_rand():
	import random
	return random.randint(3, 17)

height = 20
width = 40
player = coord(20, 10)
alive = True
offset = 2

import threading
class obstacle_move(threading.Thread):
	def __init__(self, pos):
		threading.Thread.__init__(self)
		self.pos = pos

	def run(self):
		global height
		global width
		global offset
		print(offset)
		temp_w = width
		while temp_w >= 2 and alive:
			if temp_w == player.x:
				if player.y not in range(self.pos-1+offset, self.pos+1+offset):
					end_game()
					continue
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

class player_move(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		global player
		global alive
		while True and alive:
			gotoxy(player.x, player.y)
			print("@")
			ch = getch()
			gotoxy(player.x, player.y)
			print(" ")
			if ch == 'w':
				player.y -= 2
			elif ch == 's':
				player.y += 2
			elif ch == 'q':
				end_game()


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
	
	pos = get_rand()

	global o
	global p

	o = obstacle_move(pos)
	p = player_move()

	o.start()
	p.start()
