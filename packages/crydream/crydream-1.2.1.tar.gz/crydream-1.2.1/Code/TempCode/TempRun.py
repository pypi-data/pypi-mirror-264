import numpy as np


class tempRun:
    def __init__(self):
        pass

    def sample(self, *args):
        a, b = args[:2]
        print(a, b)
        flag = True
        DataOne = "123"
        DataTwo = np.zeros((9, 5), dtype=int)
        matrices_dict = {
            "flag": flag,
            "DataOne": DataOne,
            "DataTwo": DataTwo
        }
        print(matrices_dict)
        return matrices_dict

    def modelZero(self, *args):
        a, b = args[:2]
        print(a, b)
        flag = True
        DataOne = "123"
        DataTwo = np.zeros((9, 5), dtype=int)
        matrices_dict = {
            "flag": flag,
            "DataOne": DataOne,
            "DataTwo": DataTwo
        }
        print(matrices_dict)
        return matrices_dict

    def modelOne(self, *args):
        flag = True
        return flag

    def modelTwo(self, *args):
        flag = True
        return flag

    def modelThree(self, *args):
        flag = True
        return flag
