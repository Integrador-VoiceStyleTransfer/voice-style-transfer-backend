# Voice conversion via disentangle context representation (Code for paper:https://arxiv.org/pdf/1804.02812.pdf )

# Steps for training:
1. Use make_dataset_vctk.py to convert the VCTK corpus into training data.
2. Use make_single_samples.py to make the data feed dictionary/log used in training.
3. Train using main.py
4. Generate converted samples using convert.py

## Audio convertion:
We have taken the original ``test.py`` from Chou's implementation an added a few options.

To perform a convertion you must execute the command

``python test.py -m {model_path} [args]``

The passed ``args`` define the conversion mode.

| Option | Source | Target |
|---|---|---|
| One vs. One | ``-s`` | ``-t`` |
| One vs. All | ``-s`` | ``-tl`` |
| All vs. One | ``-sl`` | ``-t`` |
| One vs. All | ``-sl`` | ``-tl`` |

Where
- ``-s`` source audio file.
- ``-sl`` source list file. Each line must be the path of the source audio file.
- ``-t`` target speaker id
- ``-tl`` target list file. Each line must be the id of the desired target speaker.



Path chou model 

/home/julian/Documentos/PI_JCL/Experimentos/Experimento 3/single_sample_model_20_english_speakers.pkl-149999


Path chou + 3 speakers spanish 

/home/julian/Documentos/PI_JCL/Experimentos/Experimento 4/single_sample_model_23_speakers.pkl-149999


Path model spanish

/home/julian/Documentos/PI_JCL/Experimentos/Experimento 5/single_sample_model_3_spanish_speakers.pkl-149999


####################################

3 SPANISH  

Target
0 #carlos
1 # jose
2 # leo


python test.py -m /home/julian/Documentos/PI_JCL/Experimentos/Experimento_5/single_sample_model_3_spanish_speakers.pkl-149999 -sl sources.txt -tl targets.txt


##########################################33


22 SPANISH ENGLISH

python test.py -m /home/julian/Documentos/PI_JCL/Experimentos/Experimento_4/single_sample_model_23_speakers.pkl-149999 -sl sources.txt -tl targets.txt


Target
0 #carlos
1 #jose
3 #leo
15 # 313 mujer gringa
19 # 345 hombre




20 SPEAKERS CHOU MODEL


Path chou model

python test.py -m /home/julian/Documentos/PI_JCL/Experimentos/Experimento_3/single_sample_model_20_english_speakers.pkl-149999 -sl sources.txt -tl targets.txt

Target

### 1  ####
18 # 270 hombre gring
1 # 228 mujer gringa


### 2 ####

14 # 254 hombre gringo
13 # 243 hombre gringo 


