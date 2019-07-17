#!/usr/bin/env python
# coding: utf-8
import os
import uuid
import random
import threading

import librosa
import numpy as np
import pandas as pd
import librosa.display
import matplotlib.pyplot as plt

import multiprocessing as mp

def discard(x, fs):
    ini = 2.5
    end = 9.5
    return x[int(fs*ini):int(fs*end)]

def noise_injection(x):
    noise_factor = random.uniform(0.001, 0.005)
    noise = np.random.randn(len(x))
    noise /= np.max(noise)
    new_x = x + noise_factor*noise
    
    return new_x

def inversion(x):
    return np.ascontiguousarray(x[::-1])

def pitch_shift(x):
    semitones = random.randint(-1,1)
    return librosa.effects.pitch_shift(x, 8000, n_steps=semitones)

def time_change(x, time_factor):
    return librosa.effects.time_stretch(x, time_factor)

def plot_diff(x, other_x):
    # waveform
    plt.figure(figsize=(18,5))
    plt.subplot(2,2,1)
    plt.title('Áudio original')
    librosa.display.waveplot(x)
    plt.subplot(2,2,2)
    plt.title('Áudio modificado')
    librosa.display.waveplot(other_x)
    
    #spec
    X = librosa.amplitude_to_db(np.abs(librosa.stft(x)), ref=np.max)
    other_X = librosa.amplitude_to_db(np.abs(librosa.stft(other_x)), ref=np.max)
    plt.subplot(2,2,3)
    plt.title('Áudio original')
    librosa.display.specshow(X, y_axis='log')
    plt.subplot(2,2,4)
    plt.title('Áudio modificado')
    librosa.display.specshow(other_X, y_axis='log')
    plt.tight_layout()

def get_audio_path(fold, name):
    return 'UrbanSound8K/audio/fold{}/{}'.format(fold, name)

def norm_maxmin(base_audio, sound):
    return np.min(base_audio) + ((sound-np.min(sound))*(np.max(base_audio)-np.min(base_audio)))/(np.max(sound)-np.min(sound)) - np.mean(sound)

def merge_sounds(x, sound_path, multiply=False):
    random_sound = load_and_resample(sound_path)
    new_x = np.copy(x)
    random_normal = norm_maxmin(x, random_sound)
    
    rand = random.uniform(0, 0.4)
    random_normal *= rand

    ini = random.randint(0, len(x)-len(random_sound)) # garante que todo o sample do urbanSound cabe
    new_x[ini:ini+len(random_sound)] += random_normal
    
    new_x -= np.mean(new_x)

    return new_x

def load_and_resample(urban_sound):
    sound, fs = librosa.core.load(urban_sound)
    sound8k = librosa.core.resample(sound, fs, 8000)
    return sound8k

def nothing():
    return

def main_(src_dir, dest_dir, prefix, num_iter):
    # O dataset tem vários áudios de barulhos urbanos e etc. Esses áudios vão ser usados aleatoriamente pra geração de novos
    # áudios
    # 
    # 
    # #### classID:
    # * 0 = air_conditioner   (não será utilizado)
    # * 1 = car_horn
    # * 2 = children_playing
    # * 3 = dog_bark
    # * 4 = drilling
    # * 5 = engine_idling
    # * 6 = gun_shot         
    # * 7 = jackhammer
    # * 8 = siren
    # * 9 = street_music   
    # 
    # #### salience
    # * 1 - foreground
    # * 2 - background

    df = pd.read_csv('UrbanSound8K/metadata/UrbanSound8K.csv')
    # remoção de colunas que não servem
    df.drop(['fsID', 'start', 'end', 'class'], 1)
    # remoção de linhas que representam áudios de tiros e de ar condicionado
    df[(df['classID'] != 0)]

    ## ok, hora do megazord
    # 0 - noise injection(x, noise_factor)
    # 1 - inversion(x)
    # 2 - pitch_shift(x, semitones)
    # 3 - merge_sounds(x, random_sound)

    functions = {0: noise_injection, 1: inversion, 2: pitch_shift, 3: merge_sounds, 4: nothing}
    labels = {0: "noise_injection", 1: "inversion", 2: "pitch_shift", 3: "merge_sounds", 4: "nothing"}
    total_rows = df.shape[0]-1

    for i in range(num_iter):
        sample_list = os.listdir(src_dir)
        num_samples = len(sample_list)

        #sample = sample_list[random.randint(0,num_samples-1)]
        sample = sample_list[i%num_samples]
        print("Sample escolhida {}".format(sample))

        x, fs = librosa.core.load('{}/{}'.format(src_dir, sample), mono=True)
        if fs != 8000:
            x = librosa.core.resample(x, fs, 8000)
        x = discard(x, 8000)

        # primeiro, quantas funções vão ser usadas em conjunto
        num_funcs = random.randint(1,18)

        # escolhendo as funções que vão ser aplicadas
        funcs = []
        new_x = np.copy(x)
        for i in range(num_funcs):
            func = random.randint(0,3)
            print("\tFunção {}".format(labels[func]))

            if func == 3:
                row = random.randint(0,total_rows)
                choice = random.choice([True, False])
                new_x = functions[func](x, get_audio_path(df.loc[row]['fold'], df.loc[row]['slice_file_name']))
            else:
                new_x = functions[func](new_x)
        new_name = str(uuid.uuid4())
        print("Salvando áudio {}".format(new_name))
        new_x = np.float32(new_x)
        librosa.output.write_wav('{}/{}_{}.wav'.format(dest_dir, prefix, new_name), new_x, 8000)

if __name__ == '__main__':
    #main_('vazamento/train', 'benchmark/train', 'cv', 80000)   
    #main_('vazamento/test', 'benchmark/test', 'cv', 20000)
    #main_('sem_vazamento/train', 'benchmark/train', 'sv', 80000)   
    #main_('sem_vazamento/test', 'benchmark/test', 'sv', 20000)



    # paralelizando o processamento
    pool = mp.Pool(mp.cpu_count())
    pool.apply(main_, args=('sem_vazamento/test', 'benchmark/test', 'sv', 7300))
    pool.close()

    pool = mp.Pool(mp.cpu_count())
    pool.apply(main_, args=('sem_vazamento/train', 'benchmark/train', 'sv', 80000))
    pool.close()

    
