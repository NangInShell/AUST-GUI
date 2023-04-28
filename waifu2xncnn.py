from waifu2x_ncnn_py.waifu2x_ncnn_vulkan import Waifu2x

def waifu2x_ncnn(model,gpu_id,tta,num_threads,tilesize):
    model_switch = {
        'cunet_noise0': [0, 1, 'models-cunet'],
        'cunet_noise0_scale2.0x': [0, 2, 'models-cunet'],
        'cunet_noise1': [1, 1, 'models-cunet'],
        'cunet_noise1_scale2.0x': [1, 2, 'models-cunet'],
        'cunet_noise2': [2, 1, 'models-pro'],
        'cunet_noise2_scale2.0x': [2, 2, 'models-cunet'],
        'cunet_noise3': [3, 1, 'models-cunet'],
        'cunet_noise3_scale2.0x': [3, 2, 'models-cunet'],
        'cunet_scale2.0x': [-1, 2, 'models-cunet'],
        'anime_noise0_scale2.0x': [0, 2, 'models-upconv_7_anime_style_art_rgb'],
        'anime_noise1_scale2.0x': [1, 2, 'models-upconv_7_anime_style_art_rgb'],
        'anime_noise2_scale2.0x': [2, 2, 'models-upconv_7_anime_style_art_rgb'],
        'anime_noise3_scale2.0x': [3, 2, 'models-upconv_7_anime_style_art_rgb'],
        'anime_scale2.0x': [-1, 2, 'models-upconv_7_anime_style_art_rgb'],
        'photo_noise0_scale2.0x': [0, 2, 'models-upconv_7_photo'],
        'photo_noise1_scale2.0x': [1, 2, 'models-upconv_7_photo'],
        'photo_noise2_scale2.0x': [2, 2, 'models-upconv_7_photo'],
        'photo_noise3_scale2.0x': [3, 2, 'models-upconv_7_photo'],
        'photo_scale2.0x': [-1, 2, 'models-upconv_7_photo']
    }
    noise, scale, version = model_switch[model] \
        if model in model_switch else [0, 1, 'models-cunet']

    waifu2x = Waifu2x(gpuid=int(gpu_id),tta_mode=bool(tta),tilesize=int(tilesize),model=str(version),noise=int(noise),scale=int(scale),num_threads=int(num_threads))
    return waifu2x.process_cv2