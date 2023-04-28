from realcugan_ncnn_py import Realcugan

def cugan_ncnn(model,gpu_id,tta,num_threads,syncgap,tilesize):
    model_switch = {
        'pro-conservative-up2x': [0, 2, 'models-pro'],
        'pro-conservative-up3x': [0, 3, 'models-pro'],
        'pro-denoise3x-up2x': [3, 2, 'models-pro'],
        'pro-denoise3x-up3x': [3, 3, 'models-pro'],
        'pro-no-denoise-up2x': [-1, 2, 'models-pro'],
        'pro-no-denoise-up3x': [-1, 3, 'models-pro'],
        'up2x-latest-conservative': [0, 2, 'models-se'],
        'up2x-latest-denoise1x': [1, 2, 'models-se'],
        'up2x-latest-denoise2x': [2, 2, 'models-se'],
        'up2x-latest-denoise3x': [3, 2, 'models-se'],
        'up2x-latest-no-denoise': [-1, 2, 'models-se'],
        'up3x-latest-conservative': [0, 3, 'models-se'],
        'up3x-latest-denoise3x': [3, 3, 'models-se'],
        'up3x-latest-no-denoise': [-1, 3, 'models-se'],
        'up4x-latest-conservative': [0, 4, 'models-se'],
        'up4x-latest-denoise3x': [3, 4, 'models-se'],
        'up4x-latest-no-denoise': [-1, 4, 'models-se'],
    }
    noise, scale, version = model_switch[model] \
        if model in model_switch else [0, 2, 'models-se']

    #realcugan = Realcugan(gpuid=int(gpu_id), scale=int(scale), noise=int(noise), tta_mode=bool(tta), num_threads=int(num_threads),syncgap=int(syncgap),model=str(version),tilesize=int(tilesize))
    realcugan = Realcugan(gpuid=0, scale=2, noise=3)
    return realcugan.process_cv2