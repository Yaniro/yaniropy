import math

'''
    Constants to be used in othe modules to make code
    more readible and avoid magic numbers
'''

YANIRO_S = "yaniro s"
YANIRO_M = "yaniro m"
YANIRO_L = "yaniro l"
YANIRO_SCARA = "yaniro scara"
YANIRO_FAMILY = (YANIRO_S, YANIRO_M, YANIRO_L, YANIRO_SCARA)

# Board used to interface with Yaniro robot.
# Master slave = board/PC + Arduino for low level control hardware interface
MASTER_SLAVE = "master slave"
BEAGLEBOARD = "beagleboard"
RASPERRY_PI = "rasperry pi"
CONFIGURATIONS = (MASTER_SLAVE, BEAGLEBOARD, RASPERRY_PI)


LINEAR_JOINT = "linear joint"
ROTATIONAL_JOINT = "rotational joint"
JOINT_TYPES = (LINEAR_JOINT, ROTATIONAL_JOINT)

# Common joint names
SHOULDER = "shoulder"
ELBOW = "elbow"
# Wrist = Wrist_pitch
WRIST = "wrist"
WRIST_ROLL = "wrist roll"
WRIST_YAW = "wrist yaw"
GRIPPER = "gripper"


# Yaniro design
# Length [mm]
L1 = 250


TWO_PI = 2 * math.pi
PI = math.pi
HALF_PI = math.pi / 2
QUARTER_PI = math.pi / 4
