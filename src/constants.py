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
CONFIGURATIONS = (MASTER_SLAVE, BEAGLEBOARD, RASPERRY_PI,)


# Joints types & aliases
PRISMATIC = "prismatic"
REVOLUTE = "revolute"
SPHERICAL = "spherical"
JOINT_TYPES = (PRISMATIC, REVOLUTE, SPHERICAL,)

# Common joint names
SHOULDER = "shoulder"
ELBOW = "elbow"
# Wrist = Wrist_pitch
WRIST = "wrist"
WRIST_ROLL = "wrist roll"
WRIST_YAW = "wrist yaw"
GRIPPER = "gripper"

# Axis & angles indexes for end effector pose vector
X = 0
Y = 1
Z = 2
ALPHA = ROLL = 3
BETA = YAW = 4
GAMMA = PITCH = 5
AXES = [X, Y, Z]


# Actuators
SERVO = "servo"
STEPPER = "stepper"
DC = "dc"
ACTUATORS = (SERVO, STEPPER, DC,)


# Yaniro design
# Length [mm]
L1 = 250


TWO_PI = 2 * math.pi
PI = math.pi
HALF_PI = math.pi / 2
QUARTER_PI = math.pi / 4
