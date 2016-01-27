import numpy as np


class RotationMatrix(object):

    def __init__(self, base_frame, to_frame, R=[], n=4):
        self.base_frame = base_frame
        self.to_frame = to_frame

        if not R:
            self._rotation_matrix = np.asmatrix(np.identity(n, np.float64))
        else:
            t = np.asmatrix(R, np.float64)
            shape = t.shape
            if shape[0] == shape[1]:
                self._rotation_matrix = t
            else:
                raise ValueError("A RotationMatrix has to be a square matrix")

    def invert(self):
        return RotationMatrix(self.to_frame,
                              self.base_frame,
                              R=self.rotation_matrix.T)

    def __mul__(self, B):
        if hasattr(B, 'rotation_matrix'):
            return self.rotation_matrix * B.rotation_matrix
        else:
            return self.rotation_matrix * B

    @property
    def rotation_matrix(self):
        return self._rotation_matrix

    @rotation_matrix.setter
    def rotation_matrix(self, A):
        R = np.asmatrix(A, np.float64)
        if R.shape == self.rotation_matrix.shape:
            self._rotation_matrix = R


# Convenience classes for safe use of proper matrix and vector sizes
class RotationMatrix3D(RotationMatrix):

    def __init__(self, base_frame, to_frame, R=[]):
        super().__init__(base_frame, to_frame, n=3)
        if R:
            if np.asmatrix(R).shape == (3, 3):
                self._rotation_matrix = np.asmatrix(R, np.float64)
            else:
                raise ValueError("A 3D Rotation Matrix has to be 3x3")


class RotationMatrix2D(RotationMatrix):

    def __init__(self, base_frame, to_frame, R=[]):
        super().__init__(base_frame, to_frame, n=2)
        if R:
            if np.asmatrix(R).shape == (2, 2):
                self._rotation_matrix = np.asmatrix(R, np.float64)
            else:
                raise ValueError("A 2D Rotation Matrix has to be 2x2")


class TranslationVector(object):

    def __init__(self, base_frame, t=[], n=4):
        self.base_frame = base_frame
        if t:
            self._translation_vector = np.asmatrix(t, np.float64)
        else:
            self._translation_vector = np.asmatrix(np.zeros(n, 1), np.float64)

    def __add__(self, t):
        if hasattr(t, 'translation'):
            return self.translation_vector + t.translation
        else:
            return self.translation_vector + t

    @property
    def translation_vector(self):
        return self._translation_vector

    @translation_vector.setter
    def translation_vector(self, t):
        tr = np.asmatrix(t, np.float64)
        if tr.shape == self.translation_vector.shape:
            self._translation_vector = tr


# Convenience classes for safe use of proper matrix and vector sizes
class Translation3D(TranslationVector):

    def __init__(self, base_frame, t=[]):
        super().__init__(base_frame, n=3)
        if t:
            tr = np.asmatrix(t, np.float64)
            if tr.shape == (3, 1):
                self._translation_vector = tr
            else:
                raise ValueError("A 3D translation vector has to be 3x1")


class Translation2D(TranslationVector):

    def __init__(self, base_frame, t=[]):
        super().__init__(base_frame, n=2)
        if t:
            tr = np.asmatrix(t, np.float64)
            if tr.shape == (2, 1):
                self._translation_vector = np.asmatrix(t, np.float64)
            else:
                raise ValueError("A 2D translation vector has to be 2x1")


class Transform(object):

    def __init__(self, rotation, translation_vector):
        r = np.asmatrix(rotation.rotation_matrix)
        r_shape = r.shape
        t = np.asmatrix(translation_vector.translation_vector)

        # Sanity checks
        if r_shape[0] != t.shape[0]:
            raise ValueError("Rotation Matrix and Translation Vector \
                              have different number of rows")

        if rotation.base_frame != translation_vector.base_frame:
            raise ValueError("Rotation Matrix and Translation Vector \
                              have different base frames")

        self.base_frame = r.base_frame
        self.to_frame = r.to_frame
        # Used short form of rotation and translation to avoid later on
        # having something like: self.rotation_matrix.rotation_matrix
        # and because we are using block matrices instead of a
        # regular transform matrix with last row consisting of zeros and
        # one 1 (Scale and shape transforms are not needed) to make things
        # faster to calculate.
        self._r = r
        self._t = t

    def __mul__(self, point):
        '''
            Allow multiplication by a point in R^n space
            Goal: discourage multiplication of transform matrices that
                  is less efficient than transforming a point to a new
                  base frame and transform that point to a new base frame

            Not: (aT^b * bT^c * cT^d) * dP
            Yes: aT^b * (bT^c * (cT^d * dP))
        '''

        p = np.asmatrix(point)
        return self.r.rotation_matrix * p + self.t.translation_vector

    @property
    def r(self):
        return self._r

    @r.setter
    def r(self, r):
        if r.shape == self.r.shape:
            self._r = r

    @property
    def t(self):
        return self._t

    @t.setter
    def t(self, t):
        if t.shape == self.t.shape:
            self._t = t


# Convenience classes for safe use of proper matrix and vector sizes
class Transform3D(Transform):

    def __init__(self, rotation, translation):
        if rotation.rotation_matrix.shape != (3, 3):
            raise ValueError("A 3D Transformation Matrix has to have a \
                              3x3 Rotation Matrix and 3x1 Translation Vector")

        super().__init__(rotation, translation)


class Transform2D(Transform):

    def __init__(self, rotation, translation):
        if rotation.rotation_matrix.shape != (2, 2):
            raise ValueError("A 2D Transformation Matrix has to have a \
                              2x2 Rotation Matrix and 2x1 Translation Vector")

        super().__init__(rotation, translation)


def compose_transforms(*args):
    '''
        Helper function in case we want to have a
        direct transform matrix (aT^k) between two frames that are k
        transform matrices appart

        Given for help but shouldn't be used.

        params: iterable with at least two Transform Matrices
    '''

    base_frame = args[0].r.base_frame
    to_frame = args[-1].r.to_frame

    r = args[0].r.rotation_matrix
    t = args[0].t.translation_vector

    # block matrix multiplication T = [R, t; [zeros], 1]
    # Left side multiplication: ((aT^b * bT^c) * cT^d) * ...
    for tr in args[1:]:
        r = r * tr.r.rotation_matrix
        t = r * tr.t.translation_vector + t

    new_r = RotationMatrix(base_frame, to_frame, r)
    new_t = TranslationVector(base_frame, t)
    return Transform(new_r, new_t)
