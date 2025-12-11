
from tkinter import * # tkinter에서 모든 정의를 임포트한다.
import time
import pygame
import random
import time


class Enemy:
	def __init__(self,canvas,images,id):
		self.__frame = 0		
		self.id = 'e'+str(id)
		self.canvas = canvas
		self.images = images
		self.me = self.canvas.create_image(1440,random.randint(10,950), image = self.images[0],tags=self.id)
		self.frame = 0
		

	def update(self):
		self.canvas.itemconfig(self.me, image = self.images[self.frame%len(self.images)])
		self.canvas.move(self.me,-4,0)		
		self.frame = self.frame + 1

	def getPos(self):
		return self.canvas.coords(self.me)

	def getId(self):
		return self.me

	

	#def setPos(self,pos):
	#	self.__pos = pos

class ShootingGame:
	def __init__(self):
		self.window = Tk() # 윈도우 생성
		self.window.title("슈팅 게임") # 제목을 설정
		self.window.geometry("1440x960") # 윈도우 크기 설정
		self.window.resizable(0,0)        
		self.lastTime = time.time()
		self.lightingTimer = time.time()
		self.keys=set()
		self.canvas = Canvas(self.window, bg = "white")
		self.canvas.pack(expand=True,fill=BOTH)
		self.window.bind("<KeyPress>",self.keyPressHandler)
		self.window.bind("<KeyRelease>",self.keyReleaseHandler)
		self.window.protocol("WM_DELETE_WINDOW", self.onClose)



		
		self.my_image_number = 0 
		self.myimages = [PhotoImage(file='image/dragon-animated-gif.gif',format = 'gif -index %i' %(i)).subsample(3) for i in range(40)]

		self.enemy_img_number = 0
		
		self.enemyimages = [PhotoImage(file='image/spaceship.png').subsample(6)]

		self.bgimage = PhotoImage(file="image/bgimage2.png")
		self.lightimage = PhotoImage(file="image/lightning-effect-png2.png")
		self.canvas.create_image(0,0, image = self.bgimage,anchor = NW,tags="bg")
		
		self.fire = PhotoImage(file = "image/fire_type2.png")

		self.dragon = self.canvas.create_image(300,480, image = self.myimages[0],tags="dragon")

		self.enemy_list = []
		self.enemy_id = 0
				
        #Play bg sound.
		pygame.init()
		pygame.mixer.music.load("sound/bgm.wav") #Loading File Into Mixer
		pygame.mixer.music.play(-1) #Playing It In The Whole Device

		#Effect sound
		self.sounds = pygame.mixer
		self.sounds.init()
		self.s_effect1 = self.sounds.Sound("sound/destruction.mp3")

		self.canvas.create_text(150,50,fill="white",font="Times 15 italic bold",text="입력키: ↑, ↓, ←, →, space")
		self.canvas.create_text(720,800,fill="white",font="Times 15 italic bold",text="Shooting Game Example")
		self.canvas.create_text(720,840,fill="white",font="Times 15 italic bold",text="Gyeongsang National University")

		while True:

			try:
				self.canvas.itemconfig(self.dragon, image = self.myimages[self.my_image_number%len(self.myimages)])    			

				self.my_image_number += 1
				self.enemy_img_number += 1

				fires = self.canvas.find_withtag("fire")
				self.display()
			

				for fire in fires:
					self.canvas.move(fire,9,0)
					if self.canvas.coords(fire)[0] > self.canvas.winfo_width():
						self.canvas.delete(fire)
			    
					#print(self.canvas.coords(fire)) # get the location of a image in canvas.

				self.manageEnemy()

			except TclError:#윈도우 강제 종료 후 에러발 생시 실행됨
				return

			self.window.after(33)
			self.window.update()

		#window.mainloop() # 이벤트 루프를 생성한다.

	def manageEnemy(self):
		if (random.randint(0,70) == 0):		
			self.enemy_list.append(Enemy(self.canvas,self.enemyimages,self.enemy_id))
			self.enemy_id = self.enemy_id + 1

		for e in self.enemy_list:
			e.update()
			if e.getPos()[0] < 0:
				self.canvas.delete(e.getId())
				self.enemy_list.pop(self.enemy_list.index(e))

		
		fires = self.canvas.find_withtag("fire")
		area = 25
		for fire in fires:
			f_pos = self.canvas.coords(fire)
			for e in self.enemy_list:
				e_pos = e.getPos()
				if e_pos[0] - area < f_pos[0] and e_pos[0] + area > f_pos[0] and e_pos[1] - area < f_pos[1] and e_pos[1] + area > f_pos[1]:
					self.s_effect1.play()
					self.canvas.delete(e.getId())
					self.enemy_list.pop(self.enemy_list.index(e))
					self.canvas.delete(fire)
			

	def keyReleaseHandler(self, event):
		if event.keycode in self.keys:
			self.keys.remove(event.keycode)
	
	def lighting_effect(self):
		for i in range(0,random.randint(5,15)):
			self.canvas.create_image(random.randint(0,self.canvas.winfo_width()),random.randint(0,self.canvas.winfo_height()), image = self.lightimage,anchor = NW,tags="lighting")
		

	def display(self):
		dragon = self.canvas.find_withtag("dragon")
		for key in self.keys:
			if key == 39: # right direction key
				self.canvas.move(dragon, 5, 0)
			if key == 37: # left direction key
				self.canvas.move(dragon, -5, 0)
			if key == 38: # down direction key
				self.canvas.move(dragon, 0, -5)
			if key == 40: # up direction key
				self.canvas.move(dragon, 0, 5)
			if key == 32:#space key
				now = time.time()#print(now-self.lastTime)
				if (now-self.lastTime) > 0.3:
					self.lastTime = now
					pos = self.canvas.coords(dragon)
					self.canvas.create_image(pos[0]+95, pos[1]+12, image = self.fire,tags="fire")

			
		if(self.lightingTimer == -1):
			self.lightingTimer = time.time()
			self.lighting_effect()
		else:
			now = time.time()
			if(now - self.lightingTimer > 4.0):
				self.lightingTimer = -1
			elif(now - self.lightingTimer > 2.0):
				lightings = self.canvas.find_withtag("lighting")
				for light in lightings:
					self.canvas.delete(light)


	def keyPressHandler(self, event):		
		if event.keycode == 27:#esc key 입력시 종료			
			self.onClose()
			
		else:
			self.keys.add(event.keycode)

	def onClose(self):
		self.running = False
		pygame.mixer.music.stop()
		pygame.quit()
		self.window.destroy()


ShootingGame() # GUI 생성한다.

