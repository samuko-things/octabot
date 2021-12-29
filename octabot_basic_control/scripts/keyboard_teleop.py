import rospy
from geometry_msgs.msg import Twist
from pynput.keyboard import Key, KeyCode, Listener





node_name="keyboard_teleop"
# topic_being_subscribed_to = "ros_tutorial/topic1" 
topic_being_published_to="/cmd_vel"

rospy.init_node(node_name, anonymous=False) #initialize and startup the ros node
pub_cmd = rospy.Publisher(topic_being_published_to, Twist, queue_size=100)



in_motion = False
inc = 0.01


max_lin_vel = 0.2
min_lin_vel = 0
default_lin_vel = 0.2

max_ang_vel = 1.0
min_ang_vel = 0
default_ang_vel = max_ang_vel/2


def drive_robot(v, w):
    global default_lin_vel, default_ang_vel, max_lin_vel, min_lin_vel ,max_ang_vel, min_ang_vel
    cmd = Twist()
    cmd.linear.x = v
    cmd.angular.z = w

    rospy.loginfo(f"v = {cmd.linear.x}, w = {cmd.angular.z}")
    pub_cmd.publish(cmd)





   
def Stop():
    global default_lin_vel, default_ang_vel, max_lin_vel, min_lin_vel ,max_ang_vel, min_ang_vel
    drive_robot(0,0)

def forward():
    global default_lin_vel, default_ang_vel, max_lin_vel, min_lin_vel ,max_ang_vel, min_ang_vel
    drive_robot(default_lin_vel, 0)

def backward():
    global default_lin_vel, default_ang_vel, max_lin_vel, min_lin_vel ,max_ang_vel, min_ang_vel
    drive_robot(-1*default_lin_vel,0)

def left_turn():
    global default_lin_vel, default_ang_vel, max_lin_vel, min_lin_vel ,max_ang_vel, min_ang_vel
    drive_robot(0,default_ang_vel)

def right_turn():
    global default_lin_vel, default_ang_vel, max_lin_vel, min_lin_vel ,max_ang_vel, min_ang_vel
    drive_robot(0,-1*default_ang_vel)





def inc_lin_vel():
    global default_lin_vel, default_ang_vel, max_lin_vel, min_lin_vel ,max_ang_vel, min_ang_vel, inc

    default_lin_vel += inc
    if default_lin_vel >= max_lin_vel:
        default_lin_vel = max_lin_vel

    rospy.loginfo(f"current_lin_vel: {default_lin_vel}")

def dec_lin_vel():
    global default_lin_vel, default_ang_vel, max_lin_vel, min_lin_vel ,max_ang_vel, min_ang_vel, inc

    default_lin_vel -= inc
    if default_lin_vel <= min_lin_vel:
        default_lin_vel = min_lin_vel

    rospy.loginfo(f"current_lin_vel: {default_lin_vel}")


def inc_ang_vel():
    global default_ang_vel, max_ang_vel, min_ang_vel, inc

    default_ang_vel += inc
    if default_ang_vel >= max_ang_vel:
        default_ang_vel = max_ang_vel

    rospy.loginfo(f"current_ang_vel: {default_ang_vel}")

def dec_ang_vel():
    global default_ang_vel, max_ang_vel, min_ang_vel, inc

    default_ang_vel -= inc
    if default_ang_vel <= min_ang_vel:
        default_ang_vel = min_ang_vel

    rospy.loginfo(f"current_ang_vel: {default_ang_vel}")


def reset_speed():
    global default_lin_vel, default_ang_vel, max_lin_vel, max_ang_vel
    default_ang_vel = max_ang_vel/2
    default_lin_vel = max_lin_vel/2




def press(key):
    
    global in_motion
    
    if key == Key.up:
        if not in_motion:
            in_motion = True
            forward()    

    elif key == Key.down:
        if not in_motion:
            in_motion = True
            backward() 

    elif key == Key.left:
        if not in_motion:
            in_motion = True
            left_turn() 

    elif key == Key.right:
        if not in_motion:
            in_motion = True
            right_turn() 


    # if key=='w' or key=='W':
    #     inc_lin_vel()
    #     print(key)
    # elif key == 'x'or'X':
    #     dec_lin_vel()
    # elif key == 'd'or'D':
    #     inc_ang_vel()
    # elif key == 'a'or'A':
    #     dec_ang_vel()
    # elif key == 's'or'S':
    #     reset_speed()
   

def release(key):
    global in_motion

    if key == Key.up:
        in_motion= False
        Stop()
        
    elif key == Key.down:
        in_motion= False
        Stop()

    elif key == Key.left:
        in_motion= False
        Stop()

    elif key == Key.right:
        in_motion= False
        Stop()

    elif key == Key.esc:
        # Stop listener
        Stop()
        return False




Stop()

rospy.loginfo("use direction keays to control the robot")

# ...or, in a non-blocking fashion:
listener = Listener(on_press=press, on_release=release)
listener.start()
listener.join()
