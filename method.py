from PyQt5.QtCore import QObject

# from realcugan_ncnn_py import Realcugan
# from realesrgan_ncnn_py import Realesrgan
# from waifu2x_ncnn_py import Waifu2x
# from srmd_ncnn_py import SRMD
#
# def cugan_ncnn(model,gpu_id,tta,num_threads,syncgap,tilesize):
#     model_switch = {
#         'pro-conservative-up2x': [0, 2, 'models-pro'],
#         'pro-conservative-up3x': [0, 3, 'models-pro'],
#         'pro-denoise3x-up2x': [3, 2, 'models-pro'],
#         'pro-denoise3x-up3x': [3, 3, 'models-pro'],
#         'pro-no-denoise-up2x': [-1, 2, 'models-pro'],
#         'pro-no-denoise-up3x': [-1, 3, 'models-pro'],
#         'up2x-latest-conservative': [0, 2, 'models-se'],
#         'up2x-latest-denoise1x': [1, 2, 'models-se'],
#         'up2x-latest-denoise2x': [2, 2, 'models-se'],
#         'up2x-latest-denoise3x': [3, 2, 'models-se'],
#         'up2x-latest-no-denoise': [-1, 2, 'models-se'],
#         'up3x-latest-conservative': [0, 3, 'models-se'],
#         'up3x-latest-denoise3x': [3, 3, 'models-se'],
#         'up3x-latest-no-denoise': [-1, 3, 'models-se'],
#         'up4x-latest-conservative': [0, 4, 'models-se'],
#         'up4x-latest-denoise3x': [3, 4, 'models-se'],
#         'up4x-latest-no-denoise': [-1, 4, 'models-se'],
#     }
#     noise, scale, version = model_switch[model] \
#         if model in model_switch else [0, 2, 'models-se']
#
#     realcugan = Realcugan(gpuid=int(gpu_id), scale=int(scale), noise=int(noise), tta_mode=tta, num_threads=int(num_threads),syncgap=int(syncgap),model=str(version),tilesize=int(tilesize))
#     return realcugan.process_cv2
#
# def esrgan_ncnn(model,gpu_id,tta,tilesize):
#     model_switch = {
#         'realesr-animevideov3-x2': 0,
#         'realesr-animevideov3-x3': 1,
#         'realesr-animevideov3-x4': 2,
#         'realesrgan-x4plus': 3,
#         'realesrgan-x4plus-anime': 4
#     }
#     model_id = model_switch[model] \
#         if model in model_switch else 0
#
#     realesrgan = Realesrgan(gpuid=gpu_id,tta_mode=tta,tilesize=tilesize,model=model_id)
#     return realesrgan.process_cv2
#
# def waifu2x_ncnn(model,gpu_id,tta,num_threads,tilesize):
#     model_switch = {
#         'cunet_noise0': [0, 1, 'models-cunet'],
#         'cunet_noise0_scale2.0x': [0, 2, 'models-cunet'],
#         'cunet_noise1': [1, 1, 'models-cunet'],
#         'cunet_noise1_scale2.0x': [1, 2, 'models-cunet'],
#         'cunet_noise2': [2, 1, 'models-pro'],
#         'cunet_noise2_scale2.0x': [2, 2, 'models-cunet'],
#         'cunet_noise3': [3, 1, 'models-cunet'],
#         'cunet_noise3_scale2.0x': [3, 2, 'models-cunet'],
#         'cunet_scale2.0x': [-1, 2, 'models-cunet'],
#         'anime_noise0_scale2.0x': [0, 2, 'models-upconv_7_anime_style_art_rgb'],
#         'anime_noise1_scale2.0x': [1, 2, 'models-upconv_7_anime_style_art_rgb'],
#         'anime_noise2_scale2.0x': [2, 2, 'models-upconv_7_anime_style_art_rgb'],
#         'anime_noise3_scale2.0x': [3, 2, 'models-upconv_7_anime_style_art_rgb'],
#         'anime_scale2.0x': [-1, 2, 'models-upconv_7_anime_style_art_rgb'],
#         'photo_noise0_scale2.0x': [0, 2, 'models-upconv_7_photo'],
#         'photo_noise1_scale2.0x': [1, 2, 'models-upconv_7_photo'],
#         'photo_noise2_scale2.0x': [2, 2, 'models-upconv_7_photo'],
#         'photo_noise3_scale2.0x': [3, 2, 'models-upconv_7_photo'],
#         'photo_scale2.0x': [-1, 2, 'models-upconv_7_photo']
#     }
#     noise, scale, version = model_switch[model] \
#         if model in model_switch else [0, 1, 'models-cunet']
#
#     waifu2x = Waifu2x(gpuid=gpu_id,tta_mode=tta,tilesize=tilesize,model=version,noise=noise,scale=scale,num_threads=num_threads)
#     return waifu2x.process_cv2
#
# def srmd_ncnn(model,gpu_id,tta,tilesize):
#     model_switch = {
#         'srmd_x2': [0, 2, 'models-srmd'],
#         'srmd_x3': [0, 3, 'models-srmd'],
#         'srmd_x4': [0, 4, 'models-srmd'],
#         'srmdnf_x2': [-1, 2, 'models-srmd'],
#         'srmdnf_x3': [-1, 3, 'models-srmd'],
#         'srmdnf_x4': [-1, 4, 'models-srmd'],
#     }
#     noise, scale, version = model_switch[model] \
#         if model in model_switch else [0, 1, 'models-srmd']
#
#     srmd = SRMD(gpuid=gpu_id,tta_mode=tta,tilesize=tilesize,model=version,noise=noise,scale=scale)
#     return srmd.process_cv2

class every_set_object(QObject):
    def __init__(self, pics, outfolder, use_sr, gpuid, tilesize,tta,sr_name,cgncnn_model,cgncnn_syncgap,cgncnn_num_streams,
                 egncnn_model,wfncnn_model,wfncnn_num_streams,srmdncnn_model,save_alpha,output_format,jpg_q,png_c):
        self.pics=pics
        self.outfolder = outfolder
        self.use_sr = use_sr
        self.gpuid = gpuid
        self.tilesize = tilesize
        self.tta = tta
        self.sr_name = sr_name
        self.cgncnn_model = cgncnn_model
        self.cgncnn_syncgap = cgncnn_syncgap
        self.cgncnn_num_streams = cgncnn_num_streams
        self.egncnn_model = egncnn_model
        self.wfncnn_model = wfncnn_model
        self.wfncnn_num_streams = wfncnn_num_streams
        self.srmdncnn_model = srmdncnn_model
        self.save_alpha = save_alpha
        self.output_format = output_format
        self.jpg_q = jpg_q
        self.png_c = png_c