import sys
import os

from configparser import ConfigParser

from PyQt5.QtGui import QTextCursor,QIcon
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from AUST_UI import Ui_MainWindow

from Signal import Signal

from method import every_set_object
from render import autorun

class MyMainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)

        self.real_path = os.path.dirname(os.path.realpath(sys.argv[0]))

        self.pic_clear.clicked.connect(self.clear_pic_list)
        self.pic_clearall.clicked.connect(self.clear_all_pic_list)
        self.pic_input.clicked.connect(self.input_pic_list)

        self.select_of.clicked.connect(self.outfolder)

        #绑定信息框
        sys.stdout = Signal()
        sys.stdout.text_update.connect(self.updatetext)

        self.autorun_Thread=None#预加载线程

        self.start_render.clicked.connect(self.render_start)
        self.stop_render.clicked.connect(self.quit_thread)

        self.load_config()

    def updatetext(self, text):
        """
            更新textEdit
        """
        cursor = self.te_show.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.te_show.insertPlainText(text)
        self.te_show.setTextCursor(cursor)
        self.te_show.ensureCursorVisible()

    def clear_pic_list(self):
        self.pic_list.takeItem(self.pic_list.row(self.pic_list.currentItem()))

    def clear_all_pic_list(self):
        self.pic_list.clear()
        self.out_folder.clear()

    def input_pic_list(self):
        files = QFileDialog.getOpenFileNames(self,
                                             "多文件选择",
                                             "./",
                                             "pics (*.jpg *.png *.webp)")
        for file in files[0]:
            self.pic_list.addItem(file)

    def outfolder(self):
        directory = QFileDialog.getExistingDirectory(self,
                                                      "选取文件夹",
                                                      "./")  # 起始路径
        valid_out_folder=True
        if ' ' in directory:
            valid_out_folder = False

        if valid_out_folder == True:
            self.out_folder.setText(directory)
        else:
            QMessageBox.information(self, "提示信息", "输出文件夹路径不能有空格字符，请重新选择。")

    def every_set(self):
        pics = []
        pics_num = self.pic_list.count()
        for i in range(pics_num):
            pics.append(self.pic_list.item(i).text())

        outfolder = self.out_folder.text()

        use_sr=self.rb_SR.isChecked()
        gpuid=self.cb_gpuid_sr.currentText()
        tilesize=self.cb_tilesize.currentText()
        tta=self.rb_tta.isChecked()

        sr_name=self.cb_SR.currentText()
        cgncnn_model=self.cb_model_cgncnn.currentText()
        cgncnn_syncgap=self.cb_syncgap_cgncnn.currentText()
        cgncnn_num_streams=self.cb_ns_cgncnn.currentText()

        egncnn_model=self.cb_model_esrncnn.currentText()

        wfncnn_model=self.cb_model_wfncnn.currentText()
        wfncnn_num_streams=self.cb_ns_wfncnn.currentText()

        srmdncnn_model=self.cb_model_srmdncnn.currentText()

        save_alpha=self.rb_save_alpha.isChecked()

        output_format=self.cb_PicFormat.currentText()
        jpg_q=self.sb_quality_jpg.text()
        png_c=self.sb_compress_png.text()

        everyset=every_set_object(pics, outfolder, use_sr, gpuid, tilesize,tta,sr_name,cgncnn_model,cgncnn_syncgap,cgncnn_num_streams,
                 egncnn_model,wfncnn_model,wfncnn_num_streams,srmdncnn_model,save_alpha,output_format,jpg_q,png_c)
        return everyset

    def save_config(self):
        conf = ConfigParser()
        every_setting = self.every_set()
        conf.add_section('main')
        conf.set('main', 'pics', str(every_setting.pics))
        conf.set('main', 'outfolder', str(every_setting.outfolder))

        conf.add_section('sr')
        conf.set('sr', 'use_sr', str(every_setting.use_sr))
        conf.set('sr', 'sr_gpu_id', str(every_setting.gpuid))
        conf.set('sr', 'tilesize', str(every_setting.tilesize))
        conf.set('sr', 'tta', str(every_setting.tta))

        conf.set('sr', 'sr_name', str(every_setting.sr_name))

        conf.set('sr', 'cgncnn_model', str(every_setting.cgncnn_model))
        conf.set('sr', 'cgncnn_syncgap', str(every_setting.cgncnn_syncgap))
        conf.set('sr', 'cgncnn_num_streams', str(every_setting.cgncnn_num_streams))

        conf.set('sr', 'egncnn_model', str(every_setting.egncnn_model))

        conf.set('sr', 'wfncnn_model', str(every_setting.wfncnn_model))
        conf.set('sr', 'wfncnn_num_streams', str(every_setting.wfncnn_num_streams))

        conf.set('sr', 'srmdncnn_model', str(every_setting.srmdncnn_model))

        conf.add_section('set')
        conf.set('set', 'save_alpha', str(every_setting.save_alpha))
        conf.set('set', 'output_format', str(every_setting.output_format))
        conf.set('set', 'jpg_q', str(every_setting.jpg_q))
        conf.set('set', 'png_c', str(every_setting.png_c))

        with open(self.real_path+'/config.ini', 'w', encoding='utf-8') as f:
            conf.write(f)
        print("已自动保存当前设置，下次启动软件时自动加载")

    def load_config(self):
        if not os.path.exists(self.real_path+"/config.ini"):
            print('加载预设失败,自定义预设文件不存在\n')
        else:
            try:

                conf = ConfigParser()
                conf.read(self.real_path+"\config.ini", encoding="utf-8")

                self.out_folder.setText(conf['main']['outfolder'])

                self.rb_SR.setChecked(conf['sr'].getboolean('use_sr'))

                self.cb_gpuid_sr.setCurrentText(conf['sr']['sr_gpu_id'])

                self.cb_tilesize.setCurrentText(conf['sr']['tilesize'])
                self.rb_tta.setChecked(conf['sr'].getboolean('tta'))

                self.cb_SR.setCurrentText(conf['sr']['sr_name'])

                self.cb_model_cgncnn.setCurrentText(conf['sr']['cgncnn_model'])
                self.cb_syncgap_cgncnn.setCurrentText(conf['sr']['cgncnn_syncgap'])
                self.cb_ns_cgncnn.setCurrentText(conf['sr']['cgncnn_num_streams'])

                self.cb_model_esrncnn.setCurrentText(conf['sr']['egncnn_model'])

                self.cb_model_wfncnn.setCurrentText(conf['sr']['wfncnn_model'])
                self.cb_ns_wfncnn.setCurrentText(conf['sr']['wfncnn_num_streams'])

                self.cb_model_srmdncnn.setCurrentText(conf['sr']['srmdncnn_model'])

                self.rb_save_alpha.setChecked(conf['set'].getboolean('save_alpha'))
                self.cb_PicFormat.setCurrentText(conf['set']['output_format'])

                self.sb_quality_jpg.setValue(conf['set'].getint('jpg_q'))
                self.sb_compress_png.setValue(conf['set'].getint('png_c'))


                print("已加载上一次软件关闭前的设置\n")
            except:
                print('加载预设失败\n')

    def render_start(self):
        self.start_render.setEnabled(False)
        self.start_render.setText('渲染ing')
        self.stop_render.setEnabled(False)
        self.stop_render.setText('终止任务')

        everysetting=self.every_set()
        allowRun=True
        for pic in everysetting.pics:
            if os.path.dirname(pic) == everysetting.outfolder:
                allowRun = False
                print('输出文件夹不能与输入视频的文件夹同目录,已自动终止运行')
                QMessageBox.information(self, "提示信息", "输出文件夹不能与输入视频的文件夹同目录")
                break
        if allowRun ==True:
            self.autorun_Thread = autorun(everysetting, 'start')
            self.autorun_Thread.signal.connect(self.set_btn_run)
            self.autorun_Thread.start()

    def quit_thread(self):
          if self.autorun_Thread != None:
              self.autorun_Thread.stop_()

          self.start_render.setEnabled(True)
          self.start_render.setText('启动渲染')
          self.stop_render.setEnabled(True)
          self.stop_render.setText('终止任务')
          print('已终止当前任务，如果程序还在运行（高占用）的话请检查任务管理器后台')

    def set_btn_run(self):#一键运行开关控制
        self.start_render.setEnabled(True)
        self.start_render.setText('启动渲染')
        self.stop_render.setEnabled(True)
        self.stop_render.setText('终止任务')

    def closeEvent(self, event):
        self.quit_thread()
        self.save_config()
        super().closeEvent(event)

if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('logo.png'))
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())