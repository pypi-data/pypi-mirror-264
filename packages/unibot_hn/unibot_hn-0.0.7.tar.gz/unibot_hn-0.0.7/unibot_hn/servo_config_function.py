from .robot_config import Device_Config
from .unibot import Unibot
from unihiker import GUI
import time



#全局button
servo_angle=[]
servo_but_add = []
servo_but_sub = []


def setbuttontext(butid):
    global servo_angle_value,servo_angle
    servo_angle[butid-1].config(text=str(servo_angle_value[butid-1]))


def servo1_button_add1_click():
    global servo_angle_value
    servo_angle_value[0]+=1
    setbuttontext(1)
    robot.robotic_arm.angle_Kinematic(1, servo_angle_value[0],servo_angle_value[1],servo_angle_value[2],servo_angle_value[3])
    
def servo1_button_sub1_click():
    global servo_angle_value,servo_angle
    servo_angle_value[0]-=1
    setbuttontext(1)
    robot.robotic_arm.angle_Kinematic(1, servo_angle_value[0],servo_angle_value[1],servo_angle_value[2],servo_angle_value[3])

def servo2_button_add1_click():
    global servo_angle_value
    servo_angle_value[1]+=1
    setbuttontext(2)
    robot.robotic_arm.angle_Kinematic(1, servo_angle_value[0],servo_angle_value[1],servo_angle_value[2],servo_angle_value[3])
    
def servo2_button_sub1_click():
    global servo_angle_value,servo_angle
    servo_angle_value[1]-=1
    setbuttontext(2)
    robot.robotic_arm.angle_Kinematic(1, servo_angle_value[0],servo_angle_value[1],servo_angle_value[2],servo_angle_value[3])

def servo3_button_add1_click():
    global servo_angle_value
    servo_angle_value[2]+=1
    setbuttontext(3)
    robot.robotic_arm.angle_Kinematic(1, servo_angle_value[0],servo_angle_value[1],servo_angle_value[2],servo_angle_value[3])
    
def servo3_button_sub1_click():
    global servo_angle_value,servo_angle
    servo_angle_value[2]-=1
    setbuttontext(3)
    robot.robotic_arm.angle_Kinematic(1, servo_angle_value[0],servo_angle_value[1],servo_angle_value[2],servo_angle_value[3])


def servo4_button_add1_click():
    global servo_angle_value
    servo_angle_value[3]+=1
    setbuttontext(4)
    robot.robotic_arm.angle_Kinematic(1, servo_angle_value[0],servo_angle_value[1],servo_angle_value[2],servo_angle_value[3])
    
def servo4_button_sub1_click():
    global servo_angle_value,servo_angle
    servo_angle_value[3]-=1
    setbuttontext(4)
    robot.robotic_arm.angle_Kinematic(1, servo_angle_value[0],servo_angle_value[1],servo_angle_value[2],servo_angle_value[3])



def servo1_button_add5_click():
    global servo_angle_value
    servo_angle_value[0]+=5
    setbuttontext(1)
    robot.robotic_arm.angle_Kinematic(1, servo_angle_value[0],servo_angle_value[1],servo_angle_value[2],servo_angle_value[3])
    
def servo1_button_sub5_click():
    global servo_angle_value,servo_angle
    servo_angle_value[0]-=5
    setbuttontext(1)
    robot.robotic_arm.angle_Kinematic(1, servo_angle_value[0],servo_angle_value[1],servo_angle_value[2],servo_angle_value[3])

def servo2_button_add5_click():
    global servo_angle_value
    servo_angle_value[1]+=5
    setbuttontext(2)
    robot.robotic_arm.angle_Kinematic(1, servo_angle_value[0],servo_angle_value[1],servo_angle_value[2],servo_angle_value[3])
    
def servo2_button_sub5_click():
    global servo_angle_value,servo_angle
    servo_angle_value[1]-=5
    setbuttontext(2)
    robot.robotic_arm.angle_Kinematic(1, servo_angle_value[0],servo_angle_value[1],servo_angle_value[2],servo_angle_value[3])

def servo3_button_add5_click():
    global servo_angle_value
    servo_angle_value[2]+=5
    setbuttontext(3)
    robot.robotic_arm.angle_Kinematic(1, servo_angle_value[0],servo_angle_value[1],servo_angle_value[2],servo_angle_value[3])
    
def servo3_button_sub5_click():
    global servo_angle_value,servo_angle
    servo_angle_value[2]-=5
    setbuttontext(3)
    robot.robotic_arm.angle_Kinematic(1, servo_angle_value[0],servo_angle_value[1],servo_angle_value[2],servo_angle_value[3])


def servo4_button_add5_click():
    global servo_angle_value
    servo_angle_value[3]+=5
    setbuttontext(4)
    robot.robotic_arm.angle_Kinematic(1, servo_angle_value[0],servo_angle_value[1],servo_angle_value[2],servo_angle_value[3])
    
def servo4_button_sub5_click():
    global servo_angle_value,servo_angle
    servo_angle_value[3]-=5
    setbuttontext(4)
    robot.robotic_arm.angle_Kinematic(1, servo_angle_value[0],servo_angle_value[1],servo_angle_value[2],servo_angle_value[3])

def servo_button_zero10_test():
    global servo_angle_value,servo_angle
    for i in range(10):
        robot.robotic_arm.angle_Kinematic(2, 90,90,90,90)
        time.sleep(4)
        robot.robotic_arm.angle_Kinematic(2, servo_angle_value[0],servo_angle_value[1],servo_angle_value[2],servo_angle_value[3])
        time.sleep(4)

def servo_button_zero_test():
    global servo_angle_value,servo_angle
    robot.robotic_arm.angle_Kinematic(2, 90,90,90,90)
    time.sleep(4)
    robot.robotic_arm.angle_Kinematic(2, servo_angle_value[0],servo_angle_value[1],servo_angle_value[2],servo_angle_value[3])
    time.sleep(4)



u_gui=GUI()
#1号舵机
u_gui.draw_text(text="1号舵机当前角度为:",x=0,y=0,font_size=10, color="#0000FF")
servo_angle.append(u_gui.draw_text(text='0',x=145,y=0,font_size=10, color="#FF0000"))
servo_but_add.append(u_gui.add_button(text="+1",x=0,y=20,w=40,h=30,onclick=servo1_button_add1_click))
servo_but_sub.append(u_gui.add_button(text="-1",x=50,y=20,w=40,h=30,onclick=servo1_button_sub1_click))
servo_but_add.append(u_gui.add_button(text="+5",x=100,y=20,w=40,h=30,onclick=servo1_button_add5_click))
servo_but_sub.append(u_gui.add_button(text="-5",x=150,y=20,w=40,h=30,onclick=servo1_button_sub5_click))

#2号舵机
u_gui.draw_text(text="2号舵机当前角度为:",x=0,y=60,font_size=10, color="#0000FF")
servo_angle.append(u_gui.draw_text(text='0',x=145,y=60,font_size=10, color="#FF0000"))
servo_but_add.append(u_gui.add_button(text="+1",x=0,y=80,w=40,h=30,onclick=servo2_button_add1_click))
servo_but_sub.append(u_gui.add_button(text="-1",x=50,y=80,w=40,h=30,onclick=servo2_button_sub1_click))
servo_but_add.append(u_gui.add_button(text="+5",x=100,y=80,w=40,h=30,onclick=servo2_button_add5_click))
servo_but_sub.append(u_gui.add_button(text="-5",x=150,y=80,w=40,h=30,onclick=servo2_button_sub5_click))


#3号舵机
u_gui.draw_text(text="3号舵机当前角度为:",x=0,y=120,font_size=10, color="#0000FF")
servo_angle.append(u_gui.draw_text(text='0',x=145,y=120,font_size=10, color="#FF0000"))
servo_but_add.append(u_gui.add_button(text="+1",x=0,y=140,w=40,h=30,onclick=servo3_button_add1_click))
servo_but_sub.append(u_gui.add_button(text="-1",x=50,y=140,w=40,h=30,onclick=servo3_button_sub1_click))
servo_but_add.append(u_gui.add_button(text="+5",x=100,y=140,w=40,h=30,onclick=servo3_button_add5_click))
servo_but_sub.append(u_gui.add_button(text="-5",x=150,y=140,w=40,h=30,onclick=servo3_button_sub5_click))


#4号舵机
u_gui.draw_text(text="4号舵机当前角度为:",x=0,y=180,font_size=10, color="#0000FF")
servo_angle.append(u_gui.draw_text(text='0',x=145,y=180,font_size=10, color="#FF0000"))
servo_but_add.append(u_gui.add_button(text="+1",x=0,y=200,w=40,h=30,onclick=servo4_button_add1_click))
servo_but_sub.append(u_gui.add_button(text="-1",x=50,y=200,w=40,h=30,onclick=servo4_button_sub1_click))
servo_but_add.append(u_gui.add_button(text="+5",x=100,y=200,w=40,h=30,onclick=servo4_button_add5_click))
servo_but_sub.append(u_gui.add_button(text="-5",x=150,y=200,w=40,h=30,onclick=servo4_button_sub5_click))


servo_angle_value = [90,90,0,0]

for i in range(4):
    setbuttontext(i+1)

robot = Unibot()

robot.robotic_arm.angle_Kinematic(1, servo_angle_value[0],servo_angle_value[1],servo_angle_value[2],servo_angle_value[3])
u_gui.add_button(text="复位测试角度",x=10,y=240,w=120,h=30,onclick=servo_button_zero_test)
u_gui.add_button(text="定位测试10次",x=10,y=280,w=120,h=30,onclick=servo_button_zero10_test)
while True:
    pass