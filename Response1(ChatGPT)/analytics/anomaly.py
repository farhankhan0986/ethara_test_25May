from collections import deque
from statistics import mean, pstdev

class ZScoreDetector:

    def __init__(self, window=100):

        self.values = deque(maxlen=window)

    def update(self, value):

        self.values.append(value)

        if len(self.values) < 10:
            return False, 0

        average = mean(self.values)
        std_dev = pstdev(self.values)

        if std_dev == 0:
            return False, 0

        z_score = (value - average) / std_dev

        return abs(z_score) > 2.5, z_score