import os
import sys

sys.path.append(os.path.dirname(__file__))

from Code.CameraCode.SecProcess import stageSec
from Code.CameraCode.FirAcquire import stageFir
from Code.Em5822Code.Em5822 import Em5822_out
from Code.UpDownLoadCode.DownLoad import downLoad
from Code.ToolCode.PrintLog import Print_Log
from Code.TempCode.TempRun import tempRun


class functionMenu:
    def __init__(self):
        self.temp = tempRun()

    def func(self, *args, **kwargs):
        if kwargs["func"] == "model1":
            data = self.temp.modelZero(*args)
            return data
        elif kwargs["func"] == "model2":
            data = self.temp.modelOne(*args)
            return data
        elif kwargs["func"] == "model3":
            data = self.temp.modelTwo(*args)
            return data
        elif kwargs["func"] == "model4":
            data = self.temp.modelThree(*args)
            return data
        else:
            pass




class cameraFunction:
    def __init__(self):
        self.staFir = stageFir()
        self.staSec = stageSec()

    def LedInit(self):
        flag = self.staFir.Led_init()
        return flag

    def CameraInit(self):
        flag = self.staFir.Camera_init()
        return flag

    def ClearCache(self, path_cache):
        self.staFir.clear_cache(path_cache)

    def ImgCheck(self, path_cache):
        num = self.staFir.img_check(path_cache)
        return num

    def ImgMerge(self, path_cache, path_save, name):
        self.staFir.img_merge(path_cache, path_save, name)

    def CamSec(self, path_read, path_write, combina, radius):
        flag, gray, nature = self.staSec.process(path_read, path_write, combina, radius)
        return flag, gray, nature


class em5822Function:
    def __init__(self):
        self.em5822 = Em5822_out()

    def Em5822Flag(self,newData):
        self.em5822.comFlagModi(newData)

    def Em5822Init(self,address):
        flag = self.em5822.em5822_init(address)
        return flag

    def Em5822Out(self, Base, Nature, Data_Light):
        flag = self.em5822.em5822_out(Base, Nature, Data_Light)
        return flag


class downFunction:
    def __init__(self):
        self.down = downLoad()

    def upDownLoad(self, original, final, identifier):
        flag = self.down.Move(original, final, identifier)
        return flag


class priFunction:
    def __init__(self):
        self.logPri = Print_Log()

    def Previos(self, adresss):
        flag = self.logPri.logPrevious(adresss)
        return flag

    def Upper(self, time):
        flag = self.logPri.logUpper(time)
        return flag
