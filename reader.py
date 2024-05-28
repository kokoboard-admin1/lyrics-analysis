import pickle
import matplotlib.pyplot as plt
import japanize_matplotlib
import numpy as np

def graf(title,data_a,data_b):
    log_increase_rates_a = [np.log(data_a[i] / data_a[i-1]) if i != 0 else 0 for i in range(len(data_a))]
    log_increase_rates_b = [np.log(data_b[i] / data_b[i-1]) if i != 0 else 0 for i in range(len(data_b))]
    plt.plot(log_increase_rates_a, label='ポジティブ値の変化')
    plt.plot(log_increase_rates_b, label='ネガティブ値の変化')
    plt.xlabel('時間')
    plt.ylabel('データ')
    plt.title(title)
    plt.legend()
    plt.show()

fi = open('data.pickle', mode='br')
b = pickle.load(fi)

for i in b:
    graf(i[0],i[1],i[2])