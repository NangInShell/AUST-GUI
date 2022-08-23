import sys
import cv2
import numpy as np
import subprocess as sp
import ffmpy
import  ffmpeg

from Real_CUGAN.upcunet_v3_2 import RealWaifuUpScaler
from time import time as ttime

from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QMainWindow
from Window import Ui_Form

class Signal(QObject):

    text_update = pyqtSignal(str)

    def write(self, text):
        self.text_update.emit(str(text))
        # loop = QEventLoop()
        # QTimer.singleShot(100, loop.quit)
        # loop.exec_()
        QApplication.processEvents()


class video_upscale_message(object):
    def __init__(self, video_path, scale, weight_path, tile_mode, cache_mode, alpha, half, device):
        self.Video_path = video_path
        self.Scale = scale
        self.Weight_path = weight_path
        self.Tile_mode = tile_mode
        self.Cache_mode = cache_mode
        self.Alpha = alpha
        self.Half = half
        self.Device = device

    # 通过函数传递
    def return_video_path(self):
        return self.Video_path

    def return_scale(self):
        return self.Scale

    def return_weight_path(self):
        return self.Weight_path

    def return_tile_mode(self):
        return self.Tile_mode

    def return_cache_mode(self):
        return self.Cache_mode

    def return_alpha(self):
        return self.Alpha

    def return_half(self):
        return self.Half

    def return_device(self):
        return self.Device


class Video_Upscale_Message_Thread(QThread):
    signal = pyqtSignal()


    def __init__(self, v_object):
        super().__init__()
        self.Video_path = v_object.return_video_path()
        self.Scale = v_object.return_scale()
        self.Weight_path = v_object.return_weight_path()
        self.Tile_mode = v_object.return_tile_mode()
        self.Cache_mode = v_object.return_cache_mode()
        self.Alpha = v_object.return_alpha()
        self.Half = v_object.return_half()
        self.Device = v_object.return_device()



    def run(self):



      for video_name in self.Video_path.splitlines():
        video_name_fix=video_name[8:]# 因为输入的文件地址格式有问题
        print(video_name_fix)
        cap = cv2.VideoCapture(video_name_fix)

        fps = cap.get(5)

        frames_num = int(cap.get(7))

        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

        upscaler = RealWaifuUpScaler(self.Scale, self.Weight_path, half=self.Half, device=self.Device)

        tmp = video_name_fix.split(".")
        video_no_audio=".".join(tmp[:-1])+'_no_audio.mp4'
        out_video = ".".join(tmp[:-1]) + '_4K.mp4'
        FFMPEG_BIN = "ffmpeg.exe"

        command_out = [FFMPEG_BIN,
                   '-i', video_name_fix,
                   '-f', 'rawvideo',
                   '-pix_fmt', 'rgb24',
                   '-']
        print(command_out)
        command_in = [FFMPEG_BIN,
                    '-y',  # (optional) overwrite output file if it exists
                    '-f', 'rawvideo',
                    '-s', '3840x2160',
                    '-pix_fmt', 'rgb24',
                    '-r', '24',  # frames per second
                    '-i', '-',  # The imput comes from a pipe
                    '-c:v', 'libx264',
                    '-pix_fmt', 'yuv420p10le',
                    video_no_audio ]
        print(command_in)
        pipe_out = sp.Popen(command_out, stdout=sp.PIPE, bufsize=10 ** 8)
        pipe_in = sp.Popen(command_in, stdin=sp.PIPE)

        num = 0
        while True:
            t0 = ttime()
            raw_image = pipe_out.stdout.read(1920 * 1080 * 3)
            if not raw_image:
                print('完成视频的帧合成')
                break
            raw_image = (np.frombuffer(raw_image, np.uint8).reshape([1080, 1920, 3]))
            raw_image = upscaler(raw_image[:, :, [2, 1, 0]], tile_mode=3, cache_mode=0, alpha=1)[:, :, ::-1]#超分辨率
            pipe_in.stdin.write(raw_image.astype(np.uint8).tobytes())
            t1 = ttime()
            num += 1
            time_use=t1 - t0
            time_message='Processing:'+str(num) + ' / ' + 'total_frames:'+str(frames_num)+' '+'    speed:'+'%.3f'%time_use+'s/f'+ '    Time remaining:'+str(int(((frames_num-num)*time_use)/3600))+'h '+ str(int((((frames_num-num)*time_use)%3600)/60))+'min ' +str(int(((frames_num-num)*time_use)%60))+'sce'
            print(time_message)

        pipe_in.stdin.close()
        pipe_out.stdout.close()
        pipe_in.wait()
        pipe_out.wait()

        ff = ffmpy.FFmpeg(
            inputs={video_name_fix: None, video_no_audio: None},
            outputs={out_video: '-map 0:a:0 -map 1:v:0 -strict -2 -c:a flac -c:v copy'}
        )
        print(ff.cmd)
        ff.run()
        print('音视频合并完成')
      self.signal.emit()



class MyMainForm(QMainWindow, Ui_Form):

    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)
        MyMainForm.setCentralWidget(self,self.widget_9)

        sys.stdout = Signal()
        sys.stdout.text_update.connect(self.updatetext)

        self.pushButton_1.clicked.connect(self.click_split)

    def updatetext(self, text):
        """
            更新textBrowser
        """
        cursor = self.textBrowser_show.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.textBrowser_show.append(text)
        self.textBrowser_show.setTextCursor(cursor)
        self.textBrowser_show.ensureCursorVisible()

    def click_split(self):
        video_path = self.textEdit_input.toPlainText()

        scale = self.comboBox_1.currentText()
        weight_path = self.comboBox_2.currentText()
        title_mode = self.comboBox_3.currentText()
        cache_mode = self.comboBox_4.currentText()
        alpha = self.comboBox_5.currentText()
        half=False
        device="cuda:0"

        Video_message = video_upscale_message(video_path, scale, weight_path, title_mode, cache_mode, alpha, half, device)
        self.pushButton_1.setEnabled(False)

        self.pushButton_1.setText('超分ing')
        self.Split_Thread = Video_Upscale_Message_Thread(Video_message)
        self.Split_Thread.signal.connect(self.set_btn_1)  # 关联信号的开关复原
        self.Split_Thread.start()

    def set_btn_1(self):
        self.pushButton_1.setText('一键视频超分')
        self.pushButton_1.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainForm()
    myWin.show()
    sys.exit(app.exec_())
