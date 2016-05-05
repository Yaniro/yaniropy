import uuid

from collections import namedtuple

from . import constants
from .transforms import Transform


Link = namedtuple("Link", "name joints mass center_mass inertia")


class Joint(object):
    '''

    '''

    def __init__(self, name, joint_type, min_value, max_value,
                 transform=None, actuator=None):
        self.name = name
        self.joint_type = joint_type
        self.transform = transform
        self._value = 0.0
        self.min_value = min_value
        self.max_value = max_value
        self.actuator = actuator

        def compute_transform(self):
            pass

        @property
        def joint_type(self):
            return self._joint_type

        @joint_type.setter
        def joint_type(self, joint_type):
            if joint_type not in constants.JOINT_TYPES:
                raise ValueError("Joint is not a valid type.")

            self._joint_type = joint_type

        @property
        def value(self):
            return self._value

        @value.setter
        def value(self, value):
            if self.type == constants.PRISMATIC:
                self._value = min(max(self.min_value, value), self.max_value)
            elif self.type == constants.REVOLUTE:
                self._value = value % 360
            else:
                self._value = value

        @property
        def actuator(self):
            return self._actuator

        @actuator.setter
        def actuator(self, actuator):
            if actuator not in constants.ACTUATORS:
                raise ValueError("Actuator is not a valid type.")

            self._actuator = actuator


class IndustrialArm(object):
    '''
        Generic robot base class. Defines basic interface with the world.
    '''

    def __init__(self, name=""):
        self._name = name
        self._uid = uuid.uuid4()
        self.joints = {}
        self.kinematic_chain = []
        self.direct_kinematics = None
        self.inverse_kinematics = None

    def joint(self, joint_name):
        return self.joints[joint_name]

    def add_joint(self, joint):
        self.joints[joint.name] = joint
        self.kinematic_chain.append((joint.name, []))

    def remove_joint(self, joint):
        del self.joints[joint.name]
        # TODO : remove joint from kinematic chain

    def add_link(self, link):
        for joint in self.kinematic_chain:
            if joint[0] == link.joints[0]:
                joint[1].append(link)
                break

    def remove_link(self, link):
        pass

    def move_to(self, coordinates):
        pass

    def rotate(self, angles):
        pass

    def move_axis(self, axis, value):
        if axis not in constants.AXES:
            raise ValueError("Axis name isn't valid. Accepted values: X, Y, Z")

        coords = [0, 0, 0]
        coords[axis] = value
        self.move_to(coords)

    def rotate_axis(self, axis, angle):
        angles = [0, 0, 0]
        angles[axis] = angle
        self.rotate(angles)

    def set_pose(self, pose):
        pass

    def compute_joint_coordinates(self, pose):
        pass

    def compute_pose(self, joint_coords):
        pass

    @property
    def uid(self):
        return self._uid


class AntropomorphicRobot(IndustrialArm):

    def __init__(self, name):
        pass