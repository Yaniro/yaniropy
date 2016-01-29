import numpy as np


class Controller(object):
    '''
        Helper base class to provide common interface for future
        controllers. Even if it is a class with two methods
        https://www.youtube.com/watch?v=o9pEzgHorH0
    '''

    def __init__(self, control_law=None):
        self.control_law = control_law

    def compensate(self, *args):
        self.control_law(args)


class PidController(Controller):

    def __init__(self, kp, ki, kd, t=1, max_i_out=500, min_i_out=-500):
        super().__init__(self.control_law)
        self.tune(kp, ki, kd)
        self.t = t
        self.max_i_out = max_i_out
        self.min_i_out = min_i_out
        self.reset()

    def control_law(self, errors):
        self.cumulative_error += errors
        d_error = (self.previous_error - errors) / self.t
        self.previous_error = errors

        i_result = [self.cut_out_i(n) for n in self.ki * self.cumulative_error]
        result = self.ki * errors + i_result + self.kd * d_error

        return result

    def tune(self, kp, ki, kd):
        if not len(kp) == len(ki) == len(kd):
            raise ValueError("Controller contants must have same length")

        self._kp = np.asarray(kp, np.float64)
        self._ki = np.asarray(ki, np.float64)
        self._kd = np.asarray(kd, np.float64)

    def reset(self):
        self.cumulative_error = np.zeros((len(self.ki), 1), np.float64)
        self.previous_error = np.zeros((len(self.kd), 1), np.float64)

    def cut_out_i(self, value):
        return max(self.min_i_out, min(self.max_i_out, value))

    # Properties used for sanity checks
    @property
    def kp(self):
        return self._kp

    @kp.setter
    def kp(self, kp):
        if len(kp) == len(self.kp):
            self._kp = kp
        else:
            raise ValueError("Proportional contants length doesn't match initial setup")

    @property
    def ki(self):
        return self._ki

    @ki.setter
    def kp(self, ki):
        if len(ki) == len(self.ki):
            self._ki = ki
        else:
            raise ValueError("Integral contants length doesn't match initial setup")

    @property
    def kd(self):
        return self._kd

    @ki.setter
    def kp(self, kd):
        if len(kd) == len(self.kd):
            self._kd = kd
        else:
            raise ValueError("Derivative contants length doesn't match initial setup")

    @property
    def t(self):
        return self._t

    @t.setter
    def t(self, t):
        if t >= 0:
            self._t = t
        else:
            raise ValueError("Sample period must be bigger than 0")

    @property
    def max_i_out(self):
        self._max_i_out

    @max_i_out.setter
    def max_i_out(self, max_i_out):
        if max_i_out > self.min_i_out:
            self._max_i_out = max_i_out
        else:
            raise ValueError("Max integral cut out must be bigger than min cout out")

    @property
    def min_i_out(self):
        return self._min_i_out

    @min_i_out.setter
    def min_i_out(self, min_i_out):
        if min_i_out < self.max_i_out:
            self._min_i_out = min_i_out
        else:
            raise ValueError("Min integral cut out must be smaller than max cout out")
