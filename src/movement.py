#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import time
import speech_recognition as sr
import re
import pyttsx3

x=0
y=0
z=0
angle=0
r=sr.Recognizer()

class Node():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0
    def __eq__(self, other):
        return self.position == other.position
def astar(maze, start, end):
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0
    open_list = []
    closed_list = []
    open_list.append(start_node)
    while len(open_list) > 0:
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index
        open_list.pop(current_index)
        closed_list.append(current_node)
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (
                    len(maze[len(maze) - 1]) - 1) or node_position[1] < 0:
                continue
            if maze[node_position[0]][node_position[1]] != 0:
                continue
            new_node = Node(current_node, node_position)
            children.append(new_node)
        for child in children:
            for closed_child in closed_list:
                if child == closed_child:
                    continue
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + (
                    (child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue
            open_list.append(child)

def command():
    while True:
        with sr.Microphone() as source:
            print("Listening")
            #r.adjust_for_ambient_noise(source,duration=0.2)
            audio=r.listen(source)
            try:
                response=r.recognize_google(audio)
                res=str(response)
                #print(res,"\n")
                return res
                if 'stop' in res:
                    break
            except sr.UnknownValueError:
                print("Could not understand audio\n")
            except sr.RequestError as e:
                print("Error,{0}".format(e))
    print("exiting")

def poseCallBack(poseMessage):
    global x
    global y, angle
    x = poseMessage.x
    y = poseMessage.y
    angle = poseMessage.theta 

'''def move(speed, distance, isForward):
    velocity = Twist()
    global x, y
    x0 = x
    y0 = y
    if (isForward):
        velocity.linear.x = abs(speed)
    else:
        velocity.linear.x = -abs(speed)
    
    distance_moved = 0.0
    loopRate = rospy.Rate(10)
    cmd_vel = '/turtle1/cmd_vel'
    velocity_pub = rospy.Publisher(cmd_vel, Twist, queue_size=10)
    while True:
        rospy.loginfo('Moving')
        velocity_pub.publish(velocity)
        loopRate.sleep()
        distance_moved = distance_moved +abs(0.5 * math.sqrt(((x-x0)**2)+((y-y0)**2)))
        print(distance_moved)
        print("x= ",x," y= ",y)
        if not (distance_moved<distance):
            rospy.loginfo("Reached destination")
            break
    velocity.linear.x = 0
    velocity_pub.publish(velocity)'''

def move_y(speed,distance,isForward):
    velocity=Twist()
    global x,y
    y0=y
    if (isForward):
        velocity.linear.y = abs(speed)
    else:
        velocity.linear.y = -abs(speed)
    distance_moved=0.0
    loopRate = rospy.Rate(10)
    cmd_vel = '/turtle1/cmd_vel'
    velocity_pub = rospy.Publisher(cmd_vel, Twist, queue_size=10)
    while True:
        rospy.loginfo('Moving')
        velocity_pub.publish(velocity)
        loopRate.sleep()
        distance_moved =  abs(y-y0)
        print(distance_moved)
        print("x= ",x," y= ",y)
        if not (distance_moved<distance):
            rospy.loginfo("Reached destination")
            break
    velocity.linear.y = 0
    velocity_pub.publish(velocity)

def move_x(speed,distance,isForward):
    velocity=Twist()
    global x,y
    x0=x
    if (isForward):
        velocity.linear.x = abs(speed)
    else:
        velocity.linear.x = -abs(speed)
    distance_moved=0.0
    loopRate = rospy.Rate(10)
    cmd_vel = '/turtle1/cmd_vel'
    velocity_pub = rospy.Publisher(cmd_vel, Twist, queue_size=10)
    while True:
        rospy.loginfo('Moving')
        velocity_pub.publish(velocity)
        loopRate.sleep()
        distance_moved =  abs(x-x0)
        print(distance_moved)
        print("x= ",x," y= ",y)
        if not (distance_moved<distance):
            rospy.loginfo("Reached destination")
            break
    velocity.linear.x = 0
    velocity_pub.publish(velocity)

def rotate(angular_speed_degree, relative_angle_degree, clockwise):
    global angle
    velocity = Twist()
    velocity.linear.x = 0
    velocity.linear.y = 0
    velocity.linear.z = 0
    velocity.angular.x = 0
    velocity.angular.y = 0
    velocity.angular.z = 0

    angle0 = angle
    angular_speed = math.radians(abs(angular_speed_degree))
    if(clockwise):
        velocity.angular.z = -abs(angular_speed)
    else:
        velocity.angular.z = abs(angular_speed)
    angle_moved = 0.0
    loopRate = rospy.Rate(10)
    cmd_vel = '/turtle1/cmd_vel'
    velocity_pub = rospy.Publisher(cmd_vel, Twist, queue_size=10)
    t0 = rospy.Time.now().to_sec()
    while True:
        rospy.loginfo("Rotating")
        velocity_pub.publish(velocity)
        t1 = rospy.Time.now().to_sec()
        angle_moved =  (t1-t0) * angular_speed_degree
        loopRate.sleep()
        if(angle_moved>relative_angle_degree):
            rospy.loginfo("Reached")
            break
    velocity.angular.z = 0
    velocity_pub.publish(velocity)



def set_desired_orientation(desired_angle_degrees):
    relative_angle_degree = math.radians(abs(desired_angle_degrees))-angle
    if relative_angle_degree < 0:
        clockwise = 1
    else:
        clockwise = 0
    rotate(30,math.degrees(abs(relative_angle_degree)),clockwise)

def go_to_goal(x_dest,y_dest):
    global x,y,z,angle
    velocity_msg=Twist()
    cmd_vel='/turtle1/cmd_vel'

    if y_dest>int(y):
        print(y_dest-y)
        move_y(1,y_dest-y,True)
    if y_dest<int(y):
        print(int(y)-y_dest)
        move_y(1,y-y_dest,False)
    if x_dest>int(x):
        print(x_dest-x)
        move_x(1,x_dest-x,True)
    if x_dest<int(x):
        print(int(x)-x_dest)
        move_x(1,x-x_dest,False)



if __name__=="__main__":
    try:
        rospy.init_node('turtle_cleaner',anonymous=True)
        cmd_vel='/turtle1/cmd_vel'
        velocity_pub = rospy.Publisher(cmd_vel,Twist,queue_size=10)
        position = '/turtle1/pose'
        pose_sub = rospy.Subscriber(position,Pose,poseCallBack)
        graph = [[0, 0, 0, 1, 0, 0],
             [1, 0, 1, 0, 1, 0],
             [0, 1, 0, 0, 0, 1],
             [0, 0, 0, 1, 0, 0],
             [0, 1, 0, 1, 0, 0],
             [0, 0, 1, 0, 0, 0]
             ]
        start = (x,y)
        end = (0,2)
        path = astar(graph,start,end)
        for i in range(len(path)):
            go_to_goal(path[i][0],path[i][1])
            print(path[i][0],path[i][1],"\n")
            #time.sleep(4)

        '''while True:
            text=command()
            print(text)
            if 'forward' in text:
                move(1.5,10,True)
            elif 'backward' in text:
                move(1.8,15,False)
            elif 'degree'in text:
                temp=re.findall(r'\d+',text)
                deg=list(map(int,temp))
                if len(deg) == 0:
                    continue
                set_desired_orientation(deg[0])
            elif 'left' in text:
                rotate(30,90,False)
            elif 'right' in text:
                rotate(30,90,True)
            elif 'go to' in text:
                temp=re.findall(r'\d+',text)
                goal=list(map(int,temp))
                print(goal)
                if len(goal) == 0:
                    continue
                go_to_goal(goal[0],goal[1])
            elif 'stop' in text:
                print('exiting')
                break'''
    except rospy.ROSInterruptException:
        rospy.loginfo("Node terminated")
        exit(0)