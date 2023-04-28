from realesrgan_ncnn_py import Realesrgan

def esrgan_ncnn(model,gpu_id,tta,tilesize):
    model_switch = {
        'realesr-animevideov3-x2': 0,
        'realesr-animevideov3-x3': 1,
        'realesr-animevideov3-x4': 2,
        'realesrgan-x4plus': 3,
        'realesrgan-x4plus-anime': 4
    }
    model_id = model_switch[model] \
        if model in model_switch else 0

    realesrgan = Realesrgan(gpuid=int(gpu_id),tta_mode=tta,tilesize=int(tilesize),model=int(model_id))
    return realesrgan.process_cv2