from kivy.app import App
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
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

        self.player1_buildbtn = Button(
        text="Build",
        size_hint=(.15, .15),
        pos_hint={'center_x': .075, 'center_y': .075},
        font_size="20sp",
        color=(0,1,0,1))
        self.add_widget(self.player1_buildbtn)
        self.player1_buildbtn.bind(on_press = self.player1_build)

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
        self.player2_buildbtn.bind(on_release = self.player2_build)

        self.player2_destroybtn = Button(
        text="Destroy!",
        size_hint=(.15, .15),
        pos_hint={'center_x':.075,'center_y':.075},
        font_size="20sp",
        color=(0,0,1,1))
        self.add_widget(self.player2_destroybtn)
        self.player2_destroybtn.bind(on_release = self.destroy2)

    def player1_build(self,event):
        self.player1_height += random.choice((0,0.1))
        self.player1_height = min(1, self.player1_height)
        maxy1 = int(500 * self.player1_height)
        miny1 = 90
        if maxy1 <= miny1:
            maxy1 = miny1 + 100
        print(miny1,maxy1)
        y1 = random.randint(miny1,maxy1)
        with self.canvas:
            b = random.choice(("rect", "rect", "rect", "circle", "ornament"))
            red,green,blue = random.random(), random.random(), random.random()
            Color(red,green,blue,1)
            if b == "rect":
                x = random.randint(80, 220)
                size_x = random.randint(50,150)
                size_y = random.randint(50,100)
                Rectangle(pos=(x,y1),size=(size_x,size_y))
                self.player1_list.append((b, x, y1, red, green, blue, size_x, size_y))
            elif b == "circle":
                x = random.randint(120,200)
                r = random.randint(10,30)
                size_x = random.randint(50,150)
                size_y = 100
                Line(circle=(x+50,y1+100,r),width=r)
                Rectangle(pos=(x,y1),size=(size_x,size_y))
                self.player1_list.append((b, x, y1, red, green, blue, size_x, size_y, r))
            else:
                x = random.randint(120,200)
                width = random.randint(40,200)
                height = random.randint(5,30)
                xstep = random.randint(5,15)
                self.zickzack(x,y1,width,height,xstep)
                #Line(points=[x-40,y2,x-30,y2+20,x-20,y2,x-10,y2+20,x,y2,x+10,y2+20,x+20,y2,x+30,y2+20,x+40,y2],width=3)
                self.player1_list.append((b, x, y1, red, green, blue, width, height, xstep))
    
    def destroy1(self,event):
        self.destroy(1)
        
    def destroy2(self,event):
        self.destroy(0)

    def destroy(self, playernumber):
        for number, li  in enumerate((self.player1_list, self.player2_list)):
            if number != playernumber:
                continue
            items = len(li)
            if items > 0:
                for i in range(max(items//5,1)):
                    del li[i]
            self.renew_screen()
        
    def renew_screen(self):
        print("renew_screen!")
        with self.canvas:
            Color(0, 1, 0, 1) # green; colors range from 0-1 not 0-255
            Rectangle(pos=(0,90),size=(800,510))
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
                #for t in self.player2_list:
            #       Color(t[3],t[4],t[5],1)
            #       if t[0] == "rect":
            #           Rectangle(pos=(t[1],t[2]),size=(t[6],t[7]))
            #       elif t[0] == "circle":
            #           Line(circle=(t[1]+50,t[2]+100,t[8]),width=t[8])
            #           Rectangle(pos=(t[1],t[2]),size=(t[6],t[7]))
            #       else:
            #           self.zickzack(t[1],t[2],t[6],t[7],t[8])

    def player2_build(self,event):
        self.player2_height += random.choice((0,0.1))
        self.player2_height = min(1, self.player2_height)
        maxy2 = int(500 * self.player2_height)
        miny2 = 90
        if maxy2 <= miny2:
            maxy2 = miny2 + 100
        print(miny2,maxy2)
        y2 = random.randint(miny2,maxy2)
        with self.canvas:
            b = random.choice(("rect", "rect", "rect", "circle", "ornament"))
            red,green,blue = random.random(), random.random(), random.random()
            Color(red,green,blue,1)
            if b == "rect":
                x = random.randint(500,620)
                size_x = random.randint(50,150)
                size_y = random.randint(50,100)
                Rectangle(pos=(x,y2),size=(size_x,size_y))
                self.player2_list.append((b, x, y2, red, green, blue, size_x, size_y))
            elif b == "circle":
                x = random.randint(500,620)
                r = random.randint(10,30)
                size_x = random.randint(50,150)
                size_y = 100
                Line(circle=(x+50,y2+100,r),width=r)
                Rectangle(pos=(x,y2),size=(size_x,size_y))
                self.player2_list.append((b, x, y2, red, green, blue, size_x, size_y, r))
            else:
                x = random.randint(500,620)
                width = random.randint(40,200)
                height = random.randint(5,30)
                xstep = random.randint(5,15)
                self.zickzack(x,y2,width,height,xstep)
                #Line(points=[x-40,y2,x-30,y2+20,x-20,y2,x-10,y2+20,x,y2,x+10,y2+20,x+20,y2,x+30,y2+20,x+40,y2],width=3)
                self.player2_list.append((b, x, y2, red, green, blue, width, height, xstep))
                    
    def zickzack(self, xm, ym, width, height, xstep):
        x = xm - width // 2
        while x < xm + width // 2:
            # zick
            Line(points=[x, ym, x+xstep, ym+height],width=3)
            # zack
            Line(points=[x+xstep, ym + height, x+2*xstep, ym],width=3)
            x += 2*xstep 
        
class MainApp(App):

    def build(self):
        self.root = root = RootWidget()
        root.bind(size=self._update_rect, pos=self._update_rect)
        with root.canvas.before:
            Color(0, 1, 0, 1) # green; colors range from 0-1 not 0-255
            self.rect = Rectangle(size=root.size, pos=root.pos)
        with root.canvas:
            Color(1, 0, 0, 1)
            #Line(points=[400,0,400,600],width=5)
            self.line = Line(points=[root.center_x*8,root.center_y-root.center_y,root.center_x*8,root.center_y*12],width=5)#50,50,500,500],width=10,color=(0,1,1,1))
        return root

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
if __name__ == '__main__':
    MainApp().run()
