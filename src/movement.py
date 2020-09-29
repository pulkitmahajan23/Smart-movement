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

def command():
    while True:
        with sr.Microphone() as source:
            print("Listening")
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

def move(speed, distance, isForward):
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

def go_to_goal(x_dest, y_dest):
    global x,y,z, angle
    velocity_msg=Twist()
    cmd_vel='/turtle1/cmd_vel'

    while(True):
        k_linear = 0.5
        distance = abs(math.sqrt((x_dest-x)**2)+((y_dest-y)**2))
        linearSpeed = k_linear * distance

        k_angular = 4.0
        angular_distance = math.atan2(y_dest-y,x_dest-x) - angle
        ang_speed = k_angular * angular_distance

        velocity_msg.linear.x = linearSpeed
        velocity_msg.angular.z = ang_speed

        velocity_pub.publish(velocity_msg)
        print("x= ",x," y= ",y)

        if distance< 0.01:
            break

def set_desired_orientation(desired_angle_degrees):
    relative_angle_degree = math.radians(abs(desired_angle_degrees))-angle
    if relative_angle_degree < 0:
        clockwise = 1
    else:
        clockwise = 0
    rotate(30,math.degrees(abs(relative_angle_degree)),clockwise)


if __name__=="__main__":
    try:
        rospy.init_node('turtle_cleaner',anonymous=True)
        cmd_vel='/turtle1/cmd_vel'
        velocity_pub = rospy.Publisher(cmd_vel,Twist,queue_size=10)
        position = '/turtle1/pose'
        pose_sub = rospy.Subscriber(position,Pose,poseCallBack)
        while True:
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
            elif 'stop' in text:
                print('exiting')
                break
    except rospy.ROSInterruptException:
        rospy.loginfo("Node terminated")
        exit(0)