import torch
from torch import optim
from torch.autograd import Variable
import numpy as np
import pickle
from utils import Hps
from utils import DataLoader
from utils import Logger
from utils import myDataset
from utils import SingleDataset
from solver import Solver
import argparse

#python main.py -dataset_path /data/home_ext/arshdeep/vctk_h5py/vctk_random20_setok2.h5 -index_path ./vctk_random20_setok2_index.json -output_model_path /data/home_ext/arshdeep/models2/single_sample_model.pkl > /data/home_ext/arshdeep/logs/train2_1219.txt

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--train', default=True, action='store_true')
    parser.add_argument('--test', default=False, action='store_true')
    parser.add_argument('--single', default=True, action='store_true')
    parser.add_argument('--load_model', default=False, action='store_true')
    parser.add_argument('--is_h5', default=True, action='store_true')
    parser.add_argument('-flag', default='train')
    parser.add_argument('-hps_path', default='./hps/vctk.json')
    parser.add_argument('-load_model_path', default='/home/julian/Documentos/PI_JCL/Experimentos/Experimento_5/single_sample_model_3_spanish_speakers.pkl-149999')
    parser.add_argument('-dataset_path', default='/home/julian/Documentos/PI_JCL/Classifier/clf_test.h5')
    parser.add_argument('-index_path', default='/home/julian/Documentos/PI_JCL/Classifier/index.json')
    parser.add_argument('-output_model_path', default='./models/model_single_sample.pkl')
    parser.add_argument('--test_clf', default=False, action='store_true')
    args = parser.parse_args()
    hps = Hps()
    hps.load(args.hps_path)
    hps_tuple = hps.get_tuple()
    if not args.single:
        dataset = myDataset(args.dataset_path,
                args.index_path,
                seg_len=hps_tuple.seg_len)
    else:
        dataset = SingleDataset(args.dataset_path,
                args.index_path,
                seg_len=hps_tuple.seg_len, is_h5=args.is_h5)

    data_loader = DataLoader(dataset,1)

    solver = Solver(hps_tuple, data_loader)

    # if args.test_clf:
    #     solver.probar_clf_bueno('/home/julian/Documentos/PI_JCL/audios/voice_integrador_OLD_JOSE_DANIEL/wav48/p101/p101_001.wav')

    if args.load_model:
        solver.load_model(args.load_model_path)
    if args.train:
        # solver.train(args.output_model_path, args.flag, mode='pretrain_G')
        solver.train(args.output_model_path, args.flag, mode='pretrain_D')
        # solver.train(args.output_model_path, args.flag, mode='train')
        # solver.train(args.output_model_path, args.flag, mode='patchGAN')

