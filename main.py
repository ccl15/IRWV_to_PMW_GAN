import argparse
import os, importlib
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ["CUDA_VISIBLE_DEVICES"] = ''
#import tensorflow as tf
import numpy as np
from modules.data_processing import load_nc, save_nc


# model    
def create_model(model_name, sub_exp_name):
    model =  importlib.import_module(f'model_library.generators.{model_name}').Model()
    model.load_weights(f'model_library/saved_weight/{sub_exp_name}/generator')
    return model


def crop(total_width, crop_width):
    start = total_width//2 - crop_width//2
    end = start + crop_width
    return start, end

def main(input_path, nc_path):
    # creat model
    print('Creat model')
    model = create_model('generator_1_1', 'Grid_GAN')
    
    # crop size
    p0, p1 = crop(201, 96)

    # load path
    print(f'load data and predict')
    TC_files = sorted(os.listdir(input_path))
    for TC_file in TC_files:
        # read input file
        img, lons, lats, attrs = load_nc(f'{input_path}/{TC_file}')
        # predict PMW
        pred = np.squeeze(model(img[:,p0:p1,p0:p1,:], training=False))
        pred_full = np.zeros((201,201))
        pred_full[:] = np.nan
        pred_full[p0:p1, p0:p1] = pred
        # save ncfile
        fn_nc = f'{nc_path}/{TC_file}'
        save_nc(fn_nc, np.squeeze(img), pred_full, lons, lats, attrs)
        
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_path", default = "/TC")
    parser.add_argument( "-nc",  "--nc_path", default = "/nc")
    args = parser.parse_args()                    
    main(args.input_path, args.nc_path)
