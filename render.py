import time

from PyQt5.QtCore import *
import cv2

from PyQt5.QtCore import QThread
import os
import sys
import subprocess as sp

from time import time as ttime

class autorun(QThread):
    signal = pyqtSignal()
    def __init__(self, every_setting, run_mode):
        super().__init__()
        self.every_setting=every_setting
        self.directory = os.path.dirname(os.path.realpath(sys.argv[0]))
        self.is_running=True
        self.run_mode=run_mode

    def stop_(self):
        self.is_running = False

    def save_img(self,final_opt_path,result):
        if self.every_setting.output_format=='jpg':
            return cv2.imwrite(final_opt_path, result,[int(cv2.IMWRITE_JPEG_QUALITY),int(self.every_setting.jpg_q)])
        if self.every_setting.output_format=='png':
            return cv2.imwrite(final_opt_path, result, [int(cv2.IMWRITE_PNG_COMPRESSION), int(self.every_setting.png_c)])

    def run(self):
            pic_folder = self.every_setting.outfolder
            if os.path.exists(pic_folder) == False:
                os.makedirs(pic_folder)
            num = 1

            for pic in self.every_setting.pics:
                if self.is_running==False:
                    break
                    print('已经终止当前进程')

                print('正在运行队列中第'+str(num)+'个图片')

                pic_name = (pic.rsplit("/", 1))[-1]
                pic_name = (pic_name.rsplit(".", 1))[0]  # 只保留文件名的参数

                final_opt_path = os.path.join(pic_folder, pic_name + '.' + self.every_setting.output_format)

                img =cv2.imread(pic,cv2.IMREAD_UNCHANGED)
                if img.shape[2] == 3:#RGB
                    t0 = ttime()
                    result = self.every_setting.sr_render(img)
                    self.save_img(final_opt_path,result)
                    t1 = ttime()
                    time_use = t1 - t0
                    print('文件名:'+pic+' 已完成'+'渲染时间: '+str(time_use)+'\n')
                elif img.shape[2] == 4:#RGBA
                    t0 = ttime()
                    img_r=self.every_setting.sr_render(img)
                    img_a=cv2.imread(pic, flags=-1)

                    height_r, width_r = img_r.shape[:2]

                    a_frame = cv2.resize(img_a, (width_r, height_r))
                    b, g, r, a = cv2.split(a_frame)
                    r, g, b = cv2.split(img_r)
                    result = cv2.merge((r, g, b, a))
                    final_opt_path = os.path.join(pic_folder, pic_name + '.png')
                    self.save_img(final_opt_path, result)
                    t1 = ttime()
                    time_use = t1 - t0
                    print('文件名:' + pic + ' 已完成' + '渲染时间: ' + str(time_use)+'\n')
                else:
                    print(pic+"为软件不支持的图片格式，可向开发者提供样例用于更新")
                num=num+1
                self.signal.emit()
