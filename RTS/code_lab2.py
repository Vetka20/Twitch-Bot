# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 07:55:34 2021

@author: k501
"""



import numpy as np
from matplotlib import pyplot as plt



#%% ---- p 1
def sync_model(Fs):
    T = 1/4160
    dt = 1/Fs
    t = np.arange(0,39*T,dt)
    
    n = len(t)
    sync_A = 11*np.ones(n)
    
    
    bool_array = (t >= 4*T) * (t <= 6*T)
    sync_A[bool_array] = 244
    
    bool_array = (t >= 8*T) * (t <= 10*T)
    sync_A[bool_array] = 244
    
    bool_array = (t >= 12*T) * (t <= 14*T)
    sync_A[bool_array] = 244
    
    bool_array = (t >= 16*T) * (t <= 18*T)
    sync_A[bool_array] = 244
    
    bool_array = (t >= 20*T) * (t <= 22*T)
    sync_A[bool_array] = 244
    
    bool_array = (t >= 24*T) * (t <= 26*T)
    sync_A[bool_array] = 244
    
    bool_array = (t >= 28*T) * (t <= 30*T)
    sync_A[bool_array] = 244
    
    return sync_A


Fs = 11025
so = sync_model(Fs)

# plt.figure()
# plt.plot(so)



#%% ---- p 2
n = len(so)
zero_samples = np.zeros(n)
s = np.concatenate( (zero_samples, so, zero_samples) )
# plt.figure()
# plt.plot(s)


#%% ---- p 3
from scipy.signal import firwin, freqz, filtfilt

numtaps = 101    # Определяет порядок фильтра.
cutoff = 2400    # Частота среза.
b = firwin(numtaps, cutoff, fs=Fs) 
a = [1]


# # Строим АЧХ фильтра (чтобы быть уверенными, 
# #    что фильтр расчитан правильно)
# f, h = freqz(b, a, fs = Fs)
# plt.figure()
# plt.plot(f,abs(h))
# plt.xlabel('f')
# plt.ylabel('|h|')


# Сигнал псле фильтрации.
# s_after_LPF = lfilter(b,a,s)
s_after_LPF = filtfilt(b,a,s)
# plt.figure()
# plt.plot(s_after_LPF)


#%% ---- p 4   (АМ модуляция)
A_t = s_after_LPF / max(s_after_LPF)
f_sub = 2.4e3

n = len(A_t)
dt = 1/Fs
t = np.arange(n) * dt

s_AM = A_t * np.cos(2*np.pi*f_sub*t)

# plt.figure()
# plt.plot(t, s_AM)

# # plt.figure()
# # plt.plot(t, A_t)

#%% ---- p 5   (повышаем частоту дискретизации)
from scipy.signal import resample

n = len(s_AM)
up_ = 25
s_AM = resample(s_AM, up_*n)

# plt.figure()
# plt.plot(s_AM)


#%%  ---- p 6  (частотная модуляция)
def fm_mod(signal,f0,f_dev,Fs):
    '''
    fm_mod    Осуществляет частотную модуляцию входного сигнала 
         Input:
      signal - 1D numpy array (закон изменения частоты) 
      f0 - частота несущей, Гц
      f_dev - частота девиации, Гц
      Fs - частота дискретизации, Гц
      
          Output:
      fm_mod - отсчеты ЧМ сигнала
      
          Comment:
      Чтобы девиация частоты сформированного сигнала соответствовала
      значению f_dev, значения вектора signal должны быть в диапазоне [-1,1].
    ''' 
    
     
    # Численно проинтегрируем закон изменения частоты (signal).
    nSamples = len(signal)
    dt = 1/Fs                               # Шаг дискретизации.
    s = np.concatenate( ( np.array([0]),
                          signal*dt) 
                       )
    int_of_signal = np.cumsum(s)            # Интегрируем функцию частоты.
    t = np.arange(0,nSamples+1)*dt                     # Массив значений времени.
     
    # Формируем ЧМ сигнал.
    pi = np.pi
    fm_signal = np.cos(2*pi*f0*t + 2*pi*f_dev*int_of_signal)
    return fm_signal

f0 = 70e3
f_dev = 17e3
Fs_new = up_*Fs
s_fm = fm_mod(s_AM,f0,f_dev,Fs_new)

# plt.figure()
# plt.plot(s_fm)

# plt.plot(s_AM,'r')




#%%  ---- p 7  (Зашумляем)
n_fm = len(s_fm)
std_ = np.std(s_fm)
snr = 0.7
noise_ = np.random.normal(loc=0.0, scale=std_/snr, size=(n_fm,))

s_fm = s_fm+noise_

# plt.figure()
# plt.plot(s_fm)


#%%  ---- p 8  (фильтрация)

numtaps = 101    		         # Определяем порядок фильтра.
cutoff = [53e3, 87e3]            # Частоты среза.
b = firwin(numtaps, cutoff, fs=Fs_new,
           pass_zero=False) 
a = [1]


# # Проверяем АЧХ фильтра
# f, h = freqz(b, a, fs = Fs_new)
# plt.figure()
# plt.plot(f,abs(h))
# plt.xlabel('f')
# plt.ylabel('|h|')

# Сигнал псле фильтрации.
s_after_filt = filtfilt(b,a,s_fm)

# plt.figure()
# plt.plot(s_after_filt)



#%%  ---- p 9  (ЧМ демодуляция)

from scipy.signal import hilbert
def fm_demod(s_FM,f0,f_dev,Fs):
    '''
    Осуществляет частотную демодуляцию входного сигнала 

          Input:
      s_FM - numpy массив (отсчеты частотно-модулированного сигнала)        
      f0 - несущая частота (Гц), 
      f_dev - частота девиации (Гц), 
      Fs - частота дискретизации (Гц).
    
          Output:
      signal - numpy массив (отсчеты демодулированного сигнала)
              
          Комментарии:
      Используется вычисление аналитического сигнала с помощью функции
          hilbert.
      Функция fm_demod нормирует выходной сигнал на частоту девиации f_dev. 
      Если значение f_dev указано верно, то значения массива signal будут 
      в диапазоне [-1,1].
    '''
    
    dt = 1/Fs                          # Шаг дискретизации.
    t = np.arange(0,len(s_FM))*dt      # Массив значений времени.
    # Вычисляем аналитический сигнал для s_FM.
    Analytic_s = hilbert(s_FM)
    
    # Переносим спектр на нулевую частоту (вычисляем комплексную огибающую).
    Complex_envelope = Analytic_s*np.exp(-1j*2*np.pi*f0*t)
    # Вычисляем фазовую функцию.
    fi = np.angle(Complex_envelope)
    # Осуществляем развертку фазы.
    fi = np.unwrap(fi)
    # Находим функцию частоты (рад/c) как производную от фазовой функции. 
    signal = np.diff(fi)/dt
    # Нормируем на девиацию частоты.
    signal = signal/(2*np.pi)/f_dev
    return signal


s_AM_ = fm_demod(s_after_filt,f0,f_dev,Fs_new)

# plt.figure()
# plt.plot(s_AM_)


#%%  ---- p 10  (Понижаем частоту дискертизации)

n = len(s_AM_)
s_AM_ = resample(s_AM_, int(n/up_) )

# plt.figure()
# plt.plot(s_AM_)





#%% ---- p 11 (Амплитудная демодуляция, модуль + ФНЧ)
def am_demod(s_AM, Fs):
    '''
    Осуществляет амплитудную демодуляцию входного сигнала 

          Input:
      s_AM - numpy массив (отсчеты АМ сигнала)        
      Fs - частота дискретизации (Гц).
    
          Output:
      signal - numpy массив (отсчеты демодулированного сигнала)
              
          Комментарии:
      Используется схема "модуль+ФНЧ"
    '''
    s_abs = np.abs(s_AM)
    
    numtaps = 101    # Определяет порядок фильтра.
    cutoff = 2400    # Частота среза.
    b = firwin(numtaps, cutoff, fs=Fs) 
    a = [1]
    
    signal = filtfilt(b,a,s_abs)
    return signal

s_ = am_demod(s_AM_, Fs)

# plt.figure()
# plt.plot(t, s_)


#%% ---- p 12 (Вычисляем нормированную корреляцию)

from scipy.stats import pearsonr

n = len(s_)
no = len(so)

n_positions = n-no+1
R = np.zeros(n_positions)
for i in range(n_positions):
    fragm = s_[i:i+no]
    ncc, _ = pearsonr(so, fragm)
    R[i] = ncc
    
# plt.figure()
# plt.plot(R)


#%% ---- p 13 (индексы превышения порога)
thresh = 0.8
index = np.where(R > thresh)
index = index[0]

# print(index)

#
if len(index) == 0:
    index = 0
else:
    args = np.argmax(R[index])
    index = index[args]
true_index = no
err = abs(index-true_index)

# print(index)
print('err = ', err)






