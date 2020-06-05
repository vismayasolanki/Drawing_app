from tkinter import *
import tkinter.font
from PIL import Image,ImageTk
import pyscreenshot as ImageGrab
import math
from tkinter.filedialog import asksaveasfilename
class PaintApp:
    drawing_tool = "line"
    left_but = "up"
    colour = "black"
    background_colour = "white"
    width = 1
    x_pos,y_pos = None,None
    x1_line_pt,y1_line_pt,x2_line_pt,y2_line_pt = None,None,None,None
    r,diag,width,height = None,None,None,None
    theta = math.pi/4
    start_x,start_y=None,None
    clicktool=0

    def save(self):
        self.drawing_area.update()
        file_name = asksaveasfilename()
        self.drawing_area.postscript(file = file_name + ".ps", colormode = 'color')

    def change_tool(self,tool):
        self.drawing_tool = tool
        self.clicktool=1


    def change_colour(self,colour):
        self.colour = colour

    def left_but_down(self,event = None):
        self.left_but = "down"
        self.x1_line_pt = event.x
        self.y1_line_pt = event.y
        self.start_x=event.x
        self.start_y=event.y

    def left_but_up(self,event = None):
        self.left_but = "up"
        self.start_x=None
        self.start_y=None

        self.x_pos = None
        self.y_pos = None

        self.x2_line_pt = event.x
        self.y2_line_pt = event.y
        
        if self.drawing_tool == "line":
            self.line_draw(event)

        elif self.drawing_tool == "rectangle":
            self.rect_draw(event)

        elif self.drawing_tool == "oval":
            self.oval_draw(event) 

        elif self.drawing_tool == "eraser":
            self.eraser(event)

        elif self.drawing_tool == "text":
            self.text_write(event)

        elif self.drawing_tool == "circle":
            self.circle_draw(event)

        elif self.drawing_tool == "square":
            self.square_draw(event)

        #elif self.drawing_tool == "add_text":
        #	self.add_text(event)

    def motion(self,event = None):
        if self.drawing_tool == "pencil":
            if self.clicktool==1:
                self.slider.set(0)
                self.clicktool=0
            self.pencil_draw(event)
        elif self.drawing_tool == "eraser":
            self.eraser(event)
            if self.clicktool==1:
                self.slider.set(30)
                self.clicktool=0
        elif self.drawing_tool == "brush":
            if self.clicktool==1:
                self.slider.set(20)
                self.clicktool=0
            self.pencil_draw(event)
        elif self.drawing_tool=="square_tunnel":
            self.square_tunnel(event)
        elif self.drawing_tool=="circular_tunnel":
            self.circular_tunnel(event)

    def pencil_draw(self,event = None):
        if self.left_but == "down":
            if self.x_pos is not None and self.y_pos is not None:
                event.widget.create_line(self.x_pos,self.y_pos,event.x,event.y,fill=self.colour,smooth=True,width=self.slider.get())
            self.x_pos = event.x
            self.y_pos = event.y

    def eraser(self,event = None):
        if self.left_but == "down":
            if self.x_pos is not None and self.y_pos is not None:
                event.widget.create_line(self.x_pos,self.y_pos,event.x,event.y,smooth=True,fill=self.background_colour,width=self.slider.get())
            self.x_pos = event.x
            self.y_pos = event.y


    def add_text(self,event = None):
     	# if self.left_but == "down":
            # if self.x_pos is not None and self.y_pos is not None:
            	# event.widget.create_text(self.x_pos,self.y_pos,event.x,event.y,activefill = "Red",text = "hello")
     			# event.widget.create_text(self.x,self.y)
        # t = Text(drawing_area,height = 2,width = 30)
        # t.pack(side = TOP)
        entry = Entry(drawing_area,height = 2,width = 30,bg = "Black")
        entry.pack(side = CENTER)
        content = entry.get()
        self.drawing_area.create_text(100,10,fill = "darkblue",font = "Times 20 italic bold",
                        text = content)

    def square_tunnel(self,event=None):

        if None not in (self.start_x,self.start_y):

            self.diag=math.sqrt((self.x1_line_pt-event.x)**2 + (self.y1_line_pt-event.y)**2)

            event.widget.create_rectangle(self.x1_line_pt-self.diag*math.cos(self.theta),self.y1_line_pt-self.diag*math.sin(self.theta),self.x1_line_pt+self.diag*math.cos(self.theta),self.y1_line_pt+self.diag*math.sin(self.theta),outline=self.colour)



    def circular_tunnel(self,event=None):

        if None not in (self.start_x,self.start_y):

            self.r=math.sqrt((self.x1_line_pt-event.x)**2 + (self.y1_line_pt-event.y)**2)

            event.widget.create_oval(self.x1_line_pt-self.r*math.cos(self.theta),self.y1_line_pt-self.r*math.sin(self.theta),self.x1_line_pt+self.r*math.cos(self.theta),self.y1_line_pt+self.r*math.sin(self.theta),outline=self.colour)


    def line_draw(self,event = None):
        if None not in (self.x1_line_pt,self.y1_line_pt,self.x2_line_pt,self.y2_line_pt):
            event.widget.create_line(self.x1_line_pt,self.y1_line_pt,self.x2_line_pt,self.y2_line_pt,smooth = True,fill = self.colour,width = self.slider.get())

    def rect_draw(self,event = None):
        if None not in (self.x1_line_pt,self.y1_line_pt,self.x2_line_pt,self.y2_line_pt):
            event.widget.create_rectangle(self.x1_line_pt,self.y1_line_pt,self.x2_line_pt,self.y2_line_pt,outline=self.colour)

    def square_draw(self,event = None):
        if None not in (self.x1_line_pt,self.y1_line_pt,self.x2_line_pt,self.y2_line_pt):
            self.diag=math.sqrt((self.x1_line_pt-self.x2_line_pt)**2 + (self.y1_line_pt-self.y2_line_pt)**2)
            event.widget.create_rectangle(self.x1_line_pt-self.diag*math.cos(self.theta),self.y1_line_pt-self.diag * math.sin(self.theta),self.x1_line_pt + self.diag * math.cos(self.theta),self.y1_line_pt + self.diag * math.sin(self.theta),outline = self.colour)

    def oval_draw(self,event = None):
         if None not in (self.x1_line_pt,self.y1_line_pt,self.x2_line_pt,self.y2_line_pt):
            event.widget.create_oval(self.x1_line_pt,self.y1_line_pt,self.x2_line_pt,self.y2_line_pt,outline = self.colour)

    def circle_draw(self,event = None):
        if None not in (self.x1_line_pt,self.y1_line_pt,self.x2_line_pt,self.y2_line_pt):
            self.r = math.sqrt((self.x1_line_pt-self.x2_line_pt)**2 + (self.y1_line_pt-self.y2_line_pt)**2)
            event.widget.create_oval(self.x1_line_pt-self.r * math.cos(self.theta),self.y1_line_pt-self.r * math.sin(self.theta),self.x1_line_pt+self.r * math.cos(self.theta),self.y1_line_pt + self.r*math.sin(self.theta),outline = self.colour)

    def text_write(self,event = None):
        if None not in (self.x1_line_pt,self.y1_line_pt):
            text_font = tkinter.font.Font(family =' Helvetica',size = 20,weight = 'bold')
            #input_text=StringVar()
            #entry=ttk.Entry(root,textvariable=input_text,justify=CENTER)
            event.widget.create_text(self.x1_line_pt,self.y1_line_pt,fill = self.colour,font = text_font,text = "hello")

    def clear_canvas(self):
        self.drawing_area.delete("all")

    def __init__(self,root,leftframe,topframe,width,height,pencil_img,rectangle_img,oval_img,square_img,eraser_img,paint_brush_img,i,a):
        self.drawing_area=Canvas(root,bg = "White",height = height,width = width - 100)
        self.drawing_area.pack(expand = True,fill = BOTH)

        self.width=width
        self.a = a
        self.height=height

        paint_brush  = Button(leftframe,command = lambda : self.change_tool("brush"),image = paint_brush_img)
        paint_brush.pack(side = TOP,padx = 10,pady = 10)
        
        line_but=Button(leftframe,text="LINE",command=lambda : self.change_tool("line"),height="2",width="10")
        line_but.pack(side=TOP,padx=10,pady=10)

        pencil_but=Button(leftframe,text="PENCIL",command=lambda : self.change_tool("pencil"),image  = pencil_img)
        pencil_but.pack(side=TOP,fill = X,padx=10,pady=10)

        rect_but=Button(leftframe,text = "RECTANGLE",command=lambda : self.change_tool("rectangle"),image = rectangle_img)
        rect_but.pack(side = TOP,fill = X,padx=10,pady=10)

        square_but=Button(leftframe,text = "SQUARE",command=lambda : self.change_tool("square"),image = square_img)
        square_but.pack(side = TOP,fill = X,padx=10,pady=10)

        oval_but=Button(leftframe,text = "OVAL",command=lambda : self.change_tool("oval"),image = oval_img)
        oval_but.pack(side = TOP,fill = X,padx=10,pady=10)

        circle_but=Button(leftframe,text = "CIRCLE",command=lambda : self.change_tool("circle"),image = circle_img)
        circle_but.pack(side = TOP,fill = X,padx=10,pady=10)

        # text_but=Button(leftframe,text="TEXT",command=lambda : self.change_tool("text"))
        # text_but.pack(side=TOP)

        eraser = Button(leftframe,text = "ERASER",command=lambda : self.change_tool("eraser"),image = eraser_img)
        eraser.pack(side = TOP,padx=10,pady=10)

        add_text = Button(leftframe,text = "ADD TEXT",command = lambda : self.change_tool("add_text"))
        add_text.pack(side = TOP,padx = 10,pady = 10)
        
        # save_label = Label(topframe,text = "save as: ")
        # save_label.pack(side = LEFT)




        # entry = Entry(topframe,width = 10)
        # entry.pack(side = LEFT)
        # a = entry.get()
        sq_tunnel_but=Button(leftframe,text = "SQUARE\nTUNNEL",command=lambda : self.change_tool("square_tunnel"))

        sq_tunnel_but.pack(side = TOP,fill = X,padx=10,pady=10)



        circular_tunnel_but=Button(leftframe,text = "CIRCULAR\nDISC",command=lambda : self.change_tool("circular_tunnel"))

        circular_tunnel_but.pack(side = TOP,fill = X,padx=10,pady=10)



        save_button = Button(topframe,text = "SAVE",fg = "Green",height="2",width="15",command = lambda : self.save())
        save_button.pack(side = LEFT,padx = 5,pady = 5)




        clear_but=Button(topframe,text="CLEAR CANVAS",command=lambda : self.clear_canvas(),height="2",width="15")
        clear_but.pack(side = LEFT,padx=5,pady=5)


        label1 = Label(topframe,text = "PENCIL/ERASER THICKNESS",fg="Black",highlightbackground="SeaGreen2",underline=0)
        label1.pack(side = LEFT)

        self.slider=Scale(topframe,from_= 0,to=100,orient = HORIZONTAL,cursor="dot")
        self.slider.pack(side = LEFT)
        
        redbutton = Button(topframe,text="RED",bg="Red",fg="Red",activeforeground="Red",command=lambda : self.change_colour("red"),height="2",width="5")
        redbutton.pack(side = RIGHT,padx=5,pady=5)
        
        greenbutton = Button(topframe,text="GREEN",bg="medium aquamarine",fg="medium aquamarine",activebackground="medium aquamarine",command=lambda : self.change_colour("medium aquamarine"),height="2",width="5")
        greenbutton.pack(side = RIGHT ,padx=5,pady=5)
        
        bluebutton = Button(topframe,text="BLUE",bg="blue",fg="Blue",activebackground="Blue",command=lambda : self.change_colour("blue"),height="2",width="5")
        bluebutton.pack(side = RIGHT,padx=5,pady=5 )
        
        blackbutton = Button(topframe,text="BLACK",bg="Black",fg="Black",activeforeground="White",activebackground="Black",command=lambda : self.change_colour("black"),height="2",width="5")
        blackbutton.pack(side = RIGHT,padx=5,pady=5)

        violetbutton = Button(topframe,text="VIOLET",bg="purple4",fg="purple4",activeforeground="DarkOrchid1",activebackground="purple4",command=lambda : self.change_colour("purple4"),height="2",width="5")
        violetbutton.pack(side = RIGHT,padx=5,pady=5)

        yellowbutton = Button(topframe,text="YELLOW",bg="YELLOW",fg="yellow",activebackground="yellow",activeforeground="goldenrod4",command=lambda : self.change_colour("yellow"),height="2",width="8")
        yellowbutton.pack(side = RIGHT ,padx=5,pady=5)

        orangebutton = Button(topframe,text="ORANGE",bg="orange red",fg="orange red",activebackground="orange red",command=lambda : self.change_colour("orange red"),height="2",width="8")
        orangebutton.pack(side = RIGHT ,padx=5,pady=5)

        whitebutton = Button(topframe,text="WHITE",bg="snow",fg="snow",activeforeground="black",activebackground="snow",command=lambda : self.change_colour("snow"),height="2",width="5")
        whitebutton.pack(side = RIGHT,padx=5,pady=5)

        dgreenbutton = Button(topframe,text="DEEP GREEN",bg="dark green",fg="dark green",activeforeground="pale green",activebackground="dark green",command=lambda : self.change_colour("dark green"),height="2",width="10")
        dgreenbutton.pack(side = RIGHT,padx=5,pady=5)

        lbluebutton = Button(topframe,text="LIGHT BLUE",bg="deep sky blue",fg="deep sky blue",activeforeground="blue",activebackground="deep sky blue",command=lambda : self.change_colour("deep sky blue"),height="2",width="10")
        lbluebutton.pack(side = RIGHT,padx=5,pady=5)
        
        self.drawing_area.bind("<Motion>",self.motion)
        self.drawing_area.bind("<ButtonPress-1>",self.left_but_down)
        self.drawing_area.bind("<ButtonRelease-1>",self.left_but_up)
        

root = Tk()
root.title("Your Canvas")
width = 1700
height = 1000
root.minsize(width,height)
leftframe = Frame(root,bg = "SeaGreen2")
leftframe.pack(side = LEFT)
topframe = Frame(root)
topframe.pack(side = TOP)
pencil_img = PhotoImage(file = "pencil.png")
rectangle_img = PhotoImage(file = "rectangle.png")
square_img = PhotoImage(file = "square.png")
oval_img = PhotoImage(file = "oval.png")
paint_brush_img = PhotoImage(file = "paint_brush.png")
circle_img = PhotoImage(file ="circle.png")
eraser_img = PhotoImage(file = "eraser.png")
i = 0
a = ""
paint_app = PaintApp(root,leftframe,topframe,width,height,pencil_img,rectangle_img,oval_img,square_img,eraser_img,paint_brush_img,i,a)
root.mainloop()