import torch
from torch import optim
from torch.autograd import Variable
import numpy as np
import pickle
from utils import Hps
from preprocess.tacotron.norm_utils import spectrogram2wav, get_spectrograms
from scipy.io.wavfile import write
import glob
import os
import argparse
from solver import Solver
import logging

logging.basicConfig(level=logging.DEBUG)

def find_test_case(source, target, source_list, target_list, output):
    if source:
        if target:
            logging.debug('Performing a One vs. One convertion')
            one_vs_one(source, target)
            return 'OvO'
        else:
            logging.debug('Performing a One vs. All convertion')
            one_vs_all(source, target_list)
            return 'OvA'
    else:
        if target:
            logging.debug('Performing an All vs. One convertion')
            all_vs_one(source_list, target)
            return 'AvO'
        else:
            logging.debug('Performing an All vs. All convertion')
            all_vs_all(source_list, target_list)
            return 'AvA'

def one_vs_one(source, target):
    # Print log
    logging.debug('Converting audio %s to target %s', source, target)
    
    

    # Create output path
    source_file_name = source.split('/')
    source_file_name = source_file_name[len(source_file_name) - 1]
    source_file_name = source_file_name.split(".")[0]

    
    str_path = source_file_name + "_to_t" + target + ".wav"
    #f'{source_file_name}_to_t{target}.wav'

    output_path = os.path.join(conversions_dir, str_path)

    # Get features and variables to perform the conversion
    _, spec = get_spectrograms(source)
    spec_expand = np.expand_dims(spec, axis=0)
    spec_tensor = torch.from_numpy(spec_expand).type(torch.FloatTensor)
    c = Variable(torch.from_numpy(np.array([int(target)]))).cuda()

    # Convert audio to target speaker
    result = solver.test_step(spec_tensor, c, gen=args.use_gen)
    result = result.squeeze(axis=0).transpose((1, 0))

    # Generate and save converted audio
    wav_data = spectrogram2wav(result)
    write(output_path, rate=args.sample_rate, data=wav_data)

def one_vs_all(source, target_list):
    with open(target_list, 'r') as f:
        target_list = f.read().splitlines()

    for target in target_list:
        one_vs_one(source, target)

def all_vs_one(source_list, target):
    with open(args.source_list, 'r') as f:
        source_list = f.read().splitlines()
    
    for source in source_list:
        one_vs_one(source, target)

def all_vs_all(source_list, target_list):
    with open(target_list, 'r') as f:
        target_list = f.read().splitlines()

    with open(args.source_list, 'r') as f:
        source_list = f.read().splitlines()

    for source in source_list:
        for target in target_list:
            one_vs_one(source, target)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-hps', help='The path of hyper-parameter set', default='./model_convert/hps/vctk.json')
    parser.add_argument('-model', '-m', help='The path of model checkpoint', default='/home/julian/Documentos/PI_JCL/Experimentos/Experimento_5/single_sample_model_3_spanish_speakers.pkl-149999')
    parser.add_argument('-source', '-s', help='The path of source .wav file')
    parser.add_argument('-target', '-t', help='Target speaker id (integer). Same order as the speaker list when preprocessing (en_speaker_used.txt)')
    parser.add_argument('-output', '-o', help='output .wav path')
    parser.add_argument('-sample_rate', '-sr', default=16000, type=int)
    parser.add_argument('--use_gen', default=True, action='store_true')
    parser.add_argument('-source_list','-sl', help='Path of a file with a list of source audios', default='sources.txt')
    parser.add_argument('-target_list', '-tl', help='Path of a file with a list of target speakers', default='targets.txt')

    args = parser.parse_args()

    # Create a dir with the conversions
    conversions_dir = os.path.join(os.path.abspath(os.getcwd()), 'conversions')
    if not os.path.exists(conversions_dir):
        os.makedirs(conversions_dir)

    # Model setup
    hps = Hps()
    hps.load(args.hps)
    hps_tuple = hps.get_tuple()
    solver = Solver(hps_tuple, None)
    solver.load_model(args.model)

    # Convert
    find_test_case(args.source, args.target, args.source_list, args.target_list, args.output)