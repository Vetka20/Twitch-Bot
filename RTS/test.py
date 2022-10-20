import numpy as np
import matplotlib.pyplot as plt
from pyparsing import line

t = np.arange(0,5,0.0001)
s_analog = 0*(t >= 0)*(t < 0.5) + 1*(t >= 0.5)*(t <= 3) + 0*(t > 3)*(t < 4) + 3*(t >= 4)*(t<=4.5) + 0*(t >4.5 )*(t <= 5)



#plt.figure()
#plt.plot(t,s_analog)
#plt.show()

#Функция для востановления отсчетов
def signal_recovery(kT,samples,T,t):
    n = len(kT) #Определяем количество итераций в цикле для каждого момента времени
    s = 0 #Определяем как начальное условия, после будем добавлять в него наши данные востановленного масива
    for i in np.arange(0,n):  #Цикл востановления который будет выполняться n раз                                               
        t1 = np.pi * (t - kT[i]) / T
        s += samples[i] * np.sin(t1) / t1 #Выполнен расчет востановленных значений
    
    #В востановленном сигнала на местах где были дискретные отсчеты появились значения NaN нужно их убрать
    nan_ind = np.where(np.isnan(s)) #Определения значений Nan
    for j in nan_ind[0]:
        s[j] = samples[ np.where( kT == t[j] ) ] #Замена значений NaN на значения из samples
    return s

def signal_discrete(s_analog,t,delta_t):
    n = len(t)
    kT = np.array([])
    s=np.array([])
    for i in t:
        if i % delta_t == 0:
            #s += s_analog[np.where( t == i )]
            s = np.append(s,s_analog[np.where( t == i )])
            kT = np.append(kT,i)
    return s , kT 

s, kT = signal_discrete(s_analog = s_analog, t = t, delta_t = 0.5)

#plt.figure()
#plt.stem(kT,s)
#plt.show()

s_recovery = signal_recovery(kT = kT, samples = s, T = 0.5, t= t)

plt.figure()
plt.plot(t,s_analog, label = "analog", color = 'red')
plt.plot(t,s_recovery, label = "recoery", color = 'green')
plt.stem(kT,s,label = "discrete", linefmt=':', basefmt=':')
plt.legend()
plt.xlabel("Время, с")
plt.ylabel("Амплитуда, В")
plt.title("")
plt.show()