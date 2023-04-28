from srmd_ncnn_py.srmd_ncnn_vulkan import SRMD

def srmd_ncnn(model,gpu_id,tta,tilesize):
    model_switch = {
        'srmd_x2': [10, 2, 'models-srmd'],
        'srmd_x3': [10, 3, 'models-srmd'],
        'srmd_x4': [10, 4, 'models-srmd'],
        'srmdnf_x2': [-1, 2, 'models-srmd'],
        'srmdnf_x3': [-1, 3, 'models-srmd'],
        'srmdnf_x4': [-1, 4, 'models-srmd'],
    }
    noise, scale, version = model_switch[model] \
        if model in model_switch else [0, 1, 'models-srmd']

    srmd = SRMD(gpuid=int(gpu_id),tta_mode=bool(tta),tilesize=int(tilesize),model=str(version),noise=int(noise),scale=int(scale))
    return srmd.process_cv2