import sys
import cv2
import json
import numpy as np
import subprocess as sp

from Real_CUGAN.upcunet_v3 import RealWaifuUpScaler
from time import time as ttime

from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QMainWindow
from AUST_UI import Ui_Form


class FFprobe():
    def __init__(self):
        self.filepath = ''
        self._video_info = {}

    def parse(self, filepath):
        self.filepath = filepath
        try:
            res = sp.check_output(
                ['ffprobe', '-i', self.filepath, '-print_format', 'json', '-show_format', '-show_streams', '-v',
                 'quiet'])
            res = res.decode('utf8')
            self._video_info = json.loads(res)
            # print('_video_info ',self._video_info)
        except Exception as e:
            print(e)
            raise Exception('获取视频信息失败')


    def video_full_frame(self):
        stream = self._video_info['streams'][0]
        return stream['nb_frames']

    def video_info(self):

        stream = self._video_info['streams']

        print(stream[0])
        if 'color_space' in stream[0]:
            color_space=stream[0]['color_space']
        else:
            color_space=2
        if 'color_transfer' in stream[0]:
            color_transfer=stream[0]['color_transfer']
        else:
            color_transfer=2
        if 'color_primaries' in stream[0]:
            color_primaries=stream[0]['color_primaries']
        else:
            color_primaries=2

        item = {
            'color_space':color_space,
            'color_transfer':color_transfer,
            'color_primaries':color_primaries
        }

        return item


class Signal(QObject):
    text_update = pyqtSignal(str)

    def write(self, text):
        self.text_update.emit(str(text))
        # loop = QEventLoop()
        # QTimer.singleShot(100, loop.quit)
        # loop.exec_()
        QApplication.processEvents()


class video_SR_message(object):
    def __init__(self, video_path, method, scale, weight_path, tile, cache, alpha, half, device):
        self.Video_path = video_path
        self.Method = method
        self.Scale = scale
        self.Weight_path = weight_path
        self.Tile = tile
        self.Cache = cache
        self.Alpha = alpha
        self.Half = half
        self.Device = device

    # 通过函数传递
    def return_video_path(self):
        return self.Video_path

    def return_method(self):
        return self.Method

    def return_scale(self):
        return self.Scale

    def return_weight_path(self):
        return self.Weight_path

    def return_tile(self):
        return self.Tile

    def return_cache(self):
        return self.Cache

    def return_alpha(self):
        return self.Alpha

    def return_half(self):
        return self.Half

    def return_device(self):
        return self.Device


class video_ffmpeg_message(QObject):
    def __init__(self, vcode, yuv, profile, preset, crf, bitrate, crf_or_bit, free, vformat):
        self.Vcode = vcode
        self.Yuv = yuv
        self.Profile = profile
        self.Preset = preset
        self.CRF = crf
        self.Bitrate = bitrate
        self.Free = free
        self.Crf_or_Bit = crf_or_bit
        self.Vformat = vformat

    def return_vcode(self):
        return self.Vcode

    def return_yuv(self):
        return self.Yuv

    def return_profile(self):
        return self.Profile

    def return_preset(self):
        return self.Preset

    def return_crf(self):
        return self.CRF

    def return_bitrate(self):
        return self.Bitrate

    def return_crf_or_bit(self):
        return self.Crf_or_Bit

    def return_free(self):
        return self.Free

    def return_vformat(self):
        return self.Vformat


class Video_SR_Thread(QThread):
    signal = pyqtSignal()

    def __init__(self, v_SR_object, v_ff_object):
        super().__init__()

        self.Video_path = v_SR_object.return_video_path()
        self.Method = v_SR_object.return_method()
        self.Scale = v_SR_object.return_scale()
        self.Weight_path = 'Real_CUGAN/models/' + v_SR_object.return_weight_path()
        self.Tile = v_SR_object.return_tile()
        self.Cache = v_SR_object.return_cache()
        self.Alpha = v_SR_object.return_alpha()

        if (v_SR_object.return_half() == 'True'):
            self.Half = True
        else:
            self.Half = False
        self.Device = v_SR_object.return_device()

        self.Vcode = v_ff_object.return_vcode()
        self.Yuv = v_ff_object.return_yuv()
        self.Profile = v_ff_object.return_profile()
        self.Preset = v_ff_object.return_preset()
        self.CRF = v_ff_object.return_crf()
        self.Bitrate = v_ff_object.return_bitrate()
        self.Crf_or_Bit = v_ff_object.return_crf_or_bit()
        self.Free = v_ff_object.return_free()
        self.Vformat = v_ff_object.return_vformat()


    def run(self):
        for video_name in self.Video_path:
            print(video_name)
            cap = cv2.VideoCapture(video_name)

            fps = cap.get(5)
            frames_num = int(cap.get(7))
            src_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            src_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

            out_height = src_height * int(self.Scale)
            out_width = src_width * int(self.Scale)

            upscaler = RealWaifuUpScaler(self.Scale, self.Weight_path, half=self.Half, device=self.Device)

            ffprobe = FFprobe()
            ffprobe.parse(video_name)

            v_info=ffprobe.video_info()#视频色彩信息获取


            tmp = video_name.split(".")
            video_no_audio = ".".join(tmp[:-1]) + '_no_audio.' + self.Vformat  # 无音频源
            out_video = ".".join(tmp[:-1]) + '_4K.' + self.Vformat  # 音视频合并
            FFMPEG_BIN = "ffmpeg.exe"


            command_out = [FFMPEG_BIN,
                           '-loglevel', 'quiet',
                           '-i', video_name,
                           '-f', 'rawvideo',
                           '-pix_fmt', 'rgb24',
                           '-color_range','tv',
                           '-sws_flags', 'accurate_rnd+full_chroma_int+bitexact',
                           '-']
            print(command_out)
            command_in = [FFMPEG_BIN,
                          '-loglevel', 'quiet',
                          '-y',  # (optional) overwrite output file if it exists
                          '-f', 'rawvideo',
                          '-s', str(out_width) + 'x' + str(out_height),
                          '-pix_fmt', 'rgb24',
                          '-r', str(fps),  # frames per second
                          '-i', '-',  # The imput comes from a pipe
                          '-preset:v', self.Preset,
                          '-color_range','tv',
                          '-sws_flags', 'accurate_rnd+full_chroma_int+bitexact',
                          '-c:v', self.Vcode,
                          '-profile:v', self.Profile,
                          '-pix_fmt', self.Yuv]

            if self.Crf_or_Bit == True:
                command_in.append('-crf')
                command_in.append(self.CRF)
            else:
                command_in.append('-b:v')
                command_in.append(self.Bitrate + 'M')

            if self.Free != '':
                X26N = self.Free.split(" ")[0]
                X26N_message = self.Free.split(" ")[1]
                command_in.append(X26N)
                command_in.append(X26N_message)

            if v_info['color_space'] != 2:
                command_in.append('-vf')
                command_in.append('scale=out_color_matrix=' + v_info['color_space'])
                command_in.append('-colorspace')
                command_in.append(v_info['color_space'])

            if v_info['color_transfer'] != 2:
                command_in.append('-color_trc')
                command_in.append(v_info['color_transfer'])

            if v_info['color_primaries'] != 2:
                command_in.append('-color_primaries')
                command_in.append(v_info['color_primaries'])

            command_in.append(video_no_audio)
            print(command_in)
            pipe_out = sp.Popen(command_out, stdout=sp.PIPE, bufsize=10 ** 8)

            pipe_in = sp.Popen(command_in, stdin=sp.PIPE)

            num = 0
            while True:
                t0 = ttime()

                raw_image = pipe_out.stdout.read(src_width * src_height * 3)
                if not raw_image:
                    break
                raw_image = (np.frombuffer(raw_image, np.uint8).reshape([src_height, src_width, 3]))


                raw_image = upscaler(raw_image[:, :, [2, 1, 0]], tile_mode=int(self.Tile), cache_mode=int(self.Cache),
                                     alpha=float(self.Alpha))[:, :, ::-1]  # 超分辨率

                pipe_in.stdin.write(raw_image.astype(np.uint8).tobytes())

                t1 = ttime()
                num += 1
                time_use = t1 - t0
                time_message = 'Processing:' + str(num) + ' / ' + 'total_frames:' + str(
                    frames_num) + ' ' + '    speed:' + '%.3f' % time_use + 's/f' + '    Time remaining:' + str(
                    int(((frames_num - num) * time_use) / 3600)) + 'h ' + str(
                    int((((frames_num - num) * time_use) % 3600) / 60)) + 'min ' + str(
                    int(((frames_num - num) * time_use) % 60)) + 'sce'
                print(time_message)
            print('完成视频的帧合成,正在关闭管道，请稍等')
            pipe_in.stdin.close()
            pipe_out.stdout.close()
            pipe_in.wait()
            pipe_out.wait()
            print('完成视频的帧合成,正在进行音视频合成，请稍等')
            command_merge = sp.Popen(
                'ffmpeg -y -loglevel quiet -i ' + video_no_audio + ' -i ' + video_name + ' -map 0:v:0 -map 1:a:0 -c:v copy -strict -2 -c:a flac ' + out_video + '',
                shell=True)
            print('完成音视频合并，音频格式统一无损转换为flac格式')

        self.signal.emit()


class MyMainForm(QMainWindow, Ui_Form):

    def __init__(self, parent=None):

        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)

        MyMainForm.setCentralWidget(self, self.widget_4)

        sys.stdout = Signal()

        sys.stdout.text_update.connect(self.updatetext)

        self.Button_start.clicked.connect(self.video_SR_click)
        self.Button_CRF.clicked.connect(self.crf_bitrate)
        self.Button_Bitrate.clicked.connect(self.bitrate_crf)

    def updatetext(self, text):
        """
            更新textBrowser
        """
        cursor = self.textBrowser.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.textBrowser.append(text)
        self.textBrowser.setTextCursor(cursor)
        self.textBrowser.ensureCursorVisible()

    def video_SR_click(self):
        video_count = self.in_path.count()  # 获取视频列表,这里获得的是数量
        video_path = []
        for i in range(video_count):
            video_path.append(self.in_path.item(i).text())
        method = self.Box_method.currentText()
        scale = self.Box_scale.currentText()
        weight_path = self.Box_model.currentText()
        tile = self.Box_tile.currentText()
        cache = self.Box_cache.currentText()
        alpha = self.number_alpha.text()
        half = self.Box_half.currentText()
        device = "cuda:" + ((self.Box_device.currentText())[0])  # 类似“cuda:0”的字符串
        # 超分参数设置
        Video_SR_message = video_SR_message(video_path, method, scale, weight_path, tile, cache, alpha, half, device)


        vcode = self.encode_vcode.currentText()
        yuv = self.Box_yuv.currentText()
        profile = self.Box_profile.currentText()
        preset = self.Box_preset.currentText()
        crf = self.lineEdit_CRF.text()
        bitrate = self.lineEdit_Bitrate.text()
        free = self.lineEdit_free.text()
        vformat = self.Box_format.currentText()

        crf_or_bit = True
        if (self.Button_Bitrate.isChecked() == True):
            crf_or_bit = False

        # 压制参数设置
        Video_ffmpeg_message = video_ffmpeg_message(vcode, yuv, profile, preset, crf, bitrate, crf_or_bit, free,
                                                    vformat)
        self.Button_start.setEnabled(False)
        self.Button_start.setText('超分ing')

        self.V_SR_Thread = Video_SR_Thread(Video_SR_message, Video_ffmpeg_message)
        self.V_SR_Thread.signal.connect(self.set_btn_start)  # 关联信号的开关复原

        self.V_SR_Thread.start()

    def set_btn_start(self):
        self.Button_start.setText('一键启动')
        self.Button_start.setEnabled(True)

    def crf_bitrate(self):
        self.Button_Bitrate.setChecked(False)

    def bitrate_crf(self):
        self.Button_CRF.setChecked(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainForm()
    myWin.show()
    sys.exit(app.exec_())