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
                raise TypeError("A RotationMatrix has to be a square matrix")

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


class RotationMatrix3D(RotationMatrix):

    def __init__(self, base_frame, to_frame, R=[]):
        super().__init__(base_frame, to_frame, n=3)
        if R:
            if np.asmatrix(R).shape == (3, 3):
                self._rotation_matrix = np.asmatrix(R, np.float64)
            else:
                raise TypeError("A 3D Rotation Matrix has to be 3x3")


class RotationMatrix2D(RotationMatrix):

    def __init__(self, base_frame, to_frame, R=[]):
        super().__init__(base_frame, to_frame, n=2)
        if R:
            if np.asmatrix(R).shape == (2, 2):
                self._rotation_matrix = np.asmatrix(R, np.float64)
            else:
                raise TypeError("A 2D Rotation Matrix has to be 2x2")


class TranslationVector(object):

    def __init__(self, base_frame, t=[], n=4):
        self.base_frame = base_frame
        if t:
            self._translation = np.asmatrix(t, np.float64)
        else:
            self._translation = np.asmatrix(np.zeros(n, 1), np.float64)

    def __add__(self, t):
        if hasattr(t, 'translation'):
            return self.translation + t.translation
        else:
            return self.translation + t

    @property
    def translation(self):
        return self._translation

    @translation.setter
    def translation(self, t):
        tr = np.asmatrix(t, np.float64)
        if tr.shape == self.translation.shape:
            self._translation = tr


class Translation3D(TranslationVector):

    def __init__(self, base_frame, t=[]):
        super().__init__(base_frame, n=3)
        if t:
            tr = np.asmatrix(t, np.float64)
            if tr.shape == (3, 1):
                self._translation = tr
            else:
                raise TypeError("A 3D translation vector has to be 3x1")


class Translation2D(TranslationVector):

    def __init__(self, base_frame, t=[]):
        super().__init__(base_frame, n=2)
        if t:
            tr = np.asmatrix(t, np.float64)
            if tr.shape == (2, 1):
                self._translation = np.asmatrix(t, np.float64)
            else:
                raise TypeError("A 2D translation vector has to be 2x1")
