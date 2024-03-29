import datetime
import os
import random
import sys
import cv2 as cv
import numpy as np

sys.path.append(os.path.dirname(__file__))

from SecBase import Img_base
from SecBase import Img_show
from SecCore import Img_core


class stageSec:

    def __init__(self):
        self.Base = Img_base()
        self.Show = Img_show()
        self.Core = Img_core()

        self.Print_Save = True

    def process(self, path_read, path_write, combina, radius):
        print("_______________________________________________")
        print("0    前期参数设置")
        gray_aver = np.zeros((9, 5), dtype=int)  
        nature_aver = np.zeros((9, 5), dtype=int)  
        nature_aver = nature_aver.astype(str)
        img_ori = self.Show.img_read(path_read)
        cv.imwrite(path_write + 'img_0ori.jpeg', img_ori)
        dst_init = self.Base.get_gray_round(img_ori)
        print("当前环境灰度值为：", self.Base.gray_round)
        print("_______________________________________________")
        print("1    获取区域内的定位点")
        num_flag = 0
        while True:
            num_flag += 1  
            dst_init -= 10  
            self.gray_value = dst_init
            img_dst = self.Show.img_dst(img_ori, dst_init)
            img_dst = self.Show.img_erosion(img_dst, 3)
            cv.imwrite(path_write + 'img_1dst.jpeg', img_dst)
            judge, img_gray, circle, circle_x, circle_y = self.Core.img_location_first(img_ori, img_dst, num=20, flag=0)
            if judge == 1:
                cv.imwrite(path_write + 'img_2ROI.jpeg', img_gray)
                print("检测到定位点，阈值为：", dst_init)
                break
            elif judge == 0:
                print("阈值为%03s" % dst_init + "\t" + "未检测到定位点")
            if num_flag >= 10:
                cv.imwrite(path_write + 'img_final.jpeg', img_ori)
                print("**错误：难以准确识别定位点")
                return False, gray_aver, nature_aver
            else:
                continue
        print("_______________________________________________")
        print("2    初次矫正图像角度")
        img_rota, img_rota_dst, middle_index = self.Core.img_correct_first(img_ori, img_dst, circle_x, circle_y)

        print("_______________________________________________")
        print("3    再次矫正图像角度")
        point_x, point_y, dis_error, locat_x, locat_y = self.Core.img_correct_second(img_rota, img_rota_dst, circle_x,
                                                                                     circle_y, flag=1)
        if locat_x == circle_x and locat_y == circle_y:
            return False, gray_aver, nature_aver
        print("_______________________________________________")
        print("4    圈定试剂点")
        gray_aver, nature_aver, img_rota, judge_1 = self.Core.img_get_gray(img_rota, gray_aver, nature_aver,
                                                                           locat_x, locat_y, point_x, point_y,
                                                                           dis_error, radius)

        font = cv.FONT_HERSHEY_SIMPLEX
        img_rota = cv.putText(img_rota, "Gray_Threshold: %s" % (self.gray_value), (50, 120), font, 3, (255, 255, 255),
                              6)
        img_rota = cv.putText(img_rota, "ROI_Down: %s" % (self.Core.gray_down), (50, 250), font, 3, (255, 255, 255), 6)
        img_rota = cv.putText(img_rota, "Dip_Angle: %.3f" % (self.Core.dip_angle), (50, 380), font, 3, (255, 255, 255),
                              6)
        img_rota = cv.putText(img_rota, "Gray_Surrounding: %.3f" % (self.Base.gray_round), (50, 510), font, 3,
                              (255, 255, 255), 6)

        cv.imwrite(path_write + 'img_final.jpeg', img_rota)

        now = datetime.datetime.now()
        time_now = now.strftime("%Y-%m-%d_%H-%M-%S")
        path_split = path_write.split('/')
        path_split[len(path_split) - 2] = "img_history"
        path_history = ""
        for i in range(len(path_split)):
            path_history = os.path.join(path_history, path_split[i])
        path_split[len(path_split) - 2] = "img_input"
        path_input = ""
        for i in range(len(path_split)):
            path_input = os.path.join(path_input, path_split[i])
        cv.imwrite(path_history + "%s_ori.jpeg" % time_now, img_ori)
        cv.imwrite(path_history + "%s_fin.jpeg" % time_now, img_rota)

        print("_______________________________________________")
        print("5    输出最终数据")
        print("参数-二值化阈值： %s" % (self.gray_value))
        print("参数-ROI下移区间： %s" % (self.Core.gray_down))
        print("参数-图像矫正角度： %.3f" % (self.Core.dip_angle))
        print("参数-环境灰度值： %.3f" % (self.Base.gray_round))
        print("发光矩阵：\r", gray_aver)
        print("性质矩阵：\r", nature_aver)

        return True, gray_aver, nature_aver
