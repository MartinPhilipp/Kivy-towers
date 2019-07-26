from kivy.app import App
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock
import gc
import random

class RootWidget(BoxLayout):
    def __init__(self, **kwargs):
    # make sure we aren't overriding any important functionality
        super(RootWidget, self).__init__(**kwargs)
        # let's add a Widget to this layout

        self.player1_height = 0.1
        self.player2_height = 0.1
        self.player1_list = []
        self.player2_list = []
        self.player1_destroying = False
        self.player2_destroying = False
        self.playtime = 0
        self.end_of_effect1 = 0
        self.end_of_effect2 = 0
        self.flash_points1 = []
        self.flash_points2 = []

        self.player1_buildbtn = Button(
        text="Build",
        size_hint=(.15, .15),
        pos_hint={'center_x': .075, 'center_y': .075},
        font_size="20sp",
        color=(0,1,0,1))
        self.add_widget(self.player1_buildbtn)
        self.player1_buildbtn.bind(on_press = self.build1)

        self.player1_destroybtn = Button(
        text="Destroy!",
        size_hint=(.15, .15),
        pos_hint={'center_x': .075, 'center_y': .075},
        font_size="20sp",
        color=(0,1,0,1))
        self.add_widget(self.player1_destroybtn)
        self.player1_destroybtn.bind(on_press = self.destroy1)

        self.player2_buildbtn = Button(
        text="Build",
        size_hint=(.15, .15),
        pos_hint={'center_x':.075,'center_y':.075},
        font_size="20sp",
        color=(0,0,1,1))
        self.add_widget(self.player2_buildbtn)
        self.player2_buildbtn.bind(on_release = self.build2)

        self.player2_destroybtn = Button(
        text="Destroy!",
        size_hint=(.15, .15),
        pos_hint={'center_x':.075,'center_y':.075},
        font_size="20sp",
        color=(0,0,1,1))
        self.add_widget(self.player2_destroybtn)
        self.player2_destroybtn.bind(on_release = self.destroy2)

    def build1(self,event):
        self.build_tower(self.player1_list, self.player1_height, 150)
        
    def build2(self,event):
        self.build_tower(self.player2_list, self.player2_height, 550)
    
    def build_tower(self,p_list,p_height, build_x):
        if len(p_list) < 150:
            p_height += random.choice((0,0.1))
            p_height = min(1, p_height)
            maxy = int(500 * p_height)
            miny = 90
            if build_x == 150:
                self.player1_height = p_height
            elif build_x == 550:
                self.player2_height = p_height
            if maxy <= miny:
                maxy = miny + 100
            y = random.randint(miny,maxy)
            with self.canvas:
                b = random.choice(("rect", "rect", "rect", "circle", "ornament"))
                red,green,blue = random.random(), random.random(), random.random()
                Color(red,green,blue,1)
                if b == "rect":
                    x = random.randint(build_x-20, build_x+20)
                    size_x = random.randint(50,150)
                    size_y = random.randint(50,100)
                    Rectangle(pos=(x,y),size=(size_x,size_y))
                    p_list.append((b, x, y, red, green, blue, size_x, size_y))
                elif b == "circle":
                    x = random.randint(build_x-50, build_x+50)
                    r = random.randint(10,30)
                    size_x = random.randint(50,150)
                    size_y = 100
                    Line(circle=(x+50,y+100,r),width=r)
                    Rectangle(pos=(x,y),size=(size_x,size_y))
                    p_list.append((b, x, y, red, green, blue, size_x, size_y, r))
                else:
                    x = random.randint(build_x-30, build_x+150)
                    width = random.randint(40,200)
                    height = random.randint(5,30)
                    xstep = random.randint(5,15)
                    self.zickzack(x,y,width,height,xstep)
                    p_list.append((b, x, y, red, green, blue, width, height, xstep))
        
    def destroy1(self,event):
        self.player1_destroying = True
        self.destroy(1)
        self.end_of_effect1 = self.playtime + 1
        self.flash_points2 = []
        for i in range(random.randint(8,14)):
            self.flash_points2.append(random.randint(500,700))
            self.flash_points2.append(800 - i * 50 + random.randint(-20,20))
        
    def destroy2(self,event):
        self.player2_destroying = True
        self.destroy(0)
        self.end_of_effect2 = self.playtime + 1
        self.flash_points1 = []
        for i in range(random.randint(8,14)):
            self.flash_points1.append(random.randint(100,300))
            self.flash_points1.append(800 - i * 50 + random.randint(-20,20))

    def destroy(self, playernumber):
        for number, li  in enumerate((self.player1_list, self.player2_list)):
            if number != playernumber:
                continue
            items = len(li)
            if items > 0:
                for i in range(max(items//5,1)):
                    if len(Particle.zoo.keys()) < 10:
                        for x in range(3):
                            Particle(x=li[i][1],y=li[i][2],playernumber=playernumber)
                    del li[i]
            self.renew_screen()
    
    def manipulate_flash1(self):
        for pos, i in enumerate(self.flash_points1):
            if pos % 2 == 0 and random.random() < 0.5:
                self.flash_points1[pos] = i + random.randint(-20,20)
    
    def manipulate_flash2(self):
        for pos, i in enumerate(self.flash_points2):
            if pos % 2 == 0 and random.random() < 0.5:
                self.flash_points2[pos] = i + random.randint(-20,20)                
        
    def renew_screen(self):
        with self.canvas:
            if self.end_of_effect1 > self.playtime:
                Color(0,random.random(),random.random(),1)
                Rectangle(pos=(400,90),size=(400,510))
            elif self.end_of_effect2 > self.playtime:
                Color(0,random.random(),random.random(),1)
                Rectangle(pos=(0,90),size=(400,510))
            else:
                Color(0, 1, 0, 1) # green; colors range from 0-1 not 0-255
                Rectangle(pos=(0,90),size=(400,510))
                Rectangle(pos=(400,90),size=(400,510))
            Color(1, 0, 0, 1)
            Line(points=[400,0,400,600],width=5)
            for li in (self.player1_list, self.player2_list):
                for t in li:
                    Color(t[3],t[4],t[5],1)
                    if t[0] == "rect":
                        Rectangle(pos=(t[1],t[2]),size=(t[6],t[7]))
                    elif t[0] == "circle":
                        Line(circle=(t[1]+50,t[2]+100,t[8]),width=t[8])
                        Rectangle(pos=(t[1],t[2]),size=(t[6],t[7]))
                    else:
                        self.zickzack(t[1],t[2],t[6],t[7],t[8])
            if self.end_of_effect1 > self.playtime:
                Color(1,1,1,1)
                Line(points=self.flash_points2,width=random.randint(1,7))
                self.manipulate_flash2()
            if self.end_of_effect2 > self.playtime:
                Color(1,1,1,1)
                Line(points=self.flash_points1,width=random.randint(1,7))
                self.manipulate_flash1()
            for number in Particle.zoo.keys():
                p = Particle.zoo[number]
                Color(p.color)
                Line(circle=(p.x,p.y,3),width=3)
    
    def zickzack(self, xm, ym, width, height, xstep):
        x = xm - width // 2
        while x < xm + width // 2:
            # zick
            Line(points=[x, ym, x+xstep, ym+height],width=3)
            # zack
            Line(points=[x+xstep, ym + height, x+2*xstep, ym],width=3)
            x += 2*xstep
            
    #def clean_memory(self,dt):
    #    gc.collect()
        
    def update(self, dt):
        #Clock.schedule_interval(self.clean_memory, 10)
        print(len(self.player1_list),len(self.player2_list))       
        self.playtime += dt
        if self.end_of_effect1 + 0.1 or self.end_of_effect2 + 0.1 >= self.playtime:
            self.renew_screen()
        # --- particles ---
        tokill = []
        for number in Particle.zoo.keys():
            p = Particle.zoo[number]
            p.update(dt)
            if p.killme: 
                tokill.append(number)
        for killnr in tokill:
            del Particle.zoo[killnr]
            
class Particle():
    zoo = {}
    number = 0
    
    def __init__(self, x, y, playernumber):
        self.number = Particle.number
        Particle.number += 1
        Particle.zoo[self.number] = self
        self.x = x + 30
        self.y = y + 30
        self.playernumber = playernumber
        self.velocity_x = random.randint(-100,100)
        self.velocity_y = random.randint(0,100)
        self.color = (random.random(),random.random(),random.random(),1)
        #Clock.schedule_once(self.kill,random.random()*5+1)
        self.killme = False   
        self.age = 0 
        self.max_age = random.random()*3+1
         
         
    def update(self,dt):
        self.age += dt
        if self.age > self.max_age:
            self.killme = True
        self.x += self.velocity_x * dt
        self.y += self.velocity_y *dt
        if self.playernumber == 0:
            if self.x > 400:
                self.killme = True
        elif self.playernumber == 1:
            if self.x < 400:
                self.killme = True
        
    #def kill(self, dummy):
    #    del Particle.zoo[self.number]
        
class MainApp(App):

    def build(self):
        self.root = root = RootWidget()
        root.bind(size=self._update_rect, pos=self._update_rect)
        with root.canvas.before:
            Color(0, 1, 0, 1) # green; colors range from 0-1 not 0-255
            self.rect = Rectangle(size=root.size, pos=root.pos)
        with root.canvas:
            Color(1, 0, 0, 1)
            self.line = Line(points=[root.center_x*8,root.center_y-root.center_y,root.center_x*8,root.center_y*12],width=5)
        Clock.schedule_interval(root.update, 1.0/30.0)
        return root

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
if __name__ == '__main__':
    MainApp().run()
