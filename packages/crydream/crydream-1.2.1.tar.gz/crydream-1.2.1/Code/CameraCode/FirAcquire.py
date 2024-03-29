import sys
import os
sys.path.append(os.path.dirname(__file__))


import serial
import serial.tools.list_ports
from PIL import Image


class stageFir:
    def __init__(self):
        self.ser = ""
        self.Com = ""
        self.ComRun_flag = False

    def Led_init(self):
        self.ports_list = list(serial.tools.list_ports.comports())
        for comport in self.ports_list:
            if list(comport)[1][0:28] == "Dtech USB-Serial Controller":
                self.Com = "%s" % comport[0]
                print("串口%s可用！" % self.Com)
            else:
                continue
        if self.Com != "":
            try:  
                self.ser = serial.Serial(self.Com, 9600)  
                self.ComRun_flag = True  
                print("串口初始化完成！")
                return True
            except Exception as e:  
                print("串口不可用！")
                print(e)
                return False
        else:  
            return False

    def Camera_init(self):
        return True

    def clear_cache(self, path_cache):
        for i in os.listdir(path_cache):
            os.remove(path_cache + "%s" % i)
        print("缓存图片全部删除")

    def img_check(self, path_cache):
        if len(os.listdir(path_cache)) == 8:
            print("图片获取完毕")
            return 1
        else:
            return 0

    def img_merge(self, path_cache, path_save, name):
        self.img_path = [path_cache + 'img0.jpeg', path_cache + 'img1.jpeg',
                         path_cache + 'img2.jpeg', path_cache + 'img3.jpeg',
                         path_cache + 'img4.jpeg', path_cache + 'img5.jpeg',
                         path_cache + 'img6.jpeg', path_cache + 'img7.jpeg']
        img = Image.open(self.img_path[0])
        width, height = img.size
        target_shape = (4 * width, 2 * height)
        target_shape_new = (4 * width, 4 * width)
        background = Image.new('L', target_shape)
        background_new = Image.new('L', target_shape_new)
        for i, img_num in enumerate(self.img_path):
            image = Image.open(img_num)
            image = image.resize((width, height))
            row, col = i // 4, i % 4
            location = (col * width, row * height)
            background.paste(image, location)
            background_new.paste(background, (0, 0))
        background_new.save(path_save + "%s.jpeg" % name)
        img.close()
        self.clear_cache(path_cache)
