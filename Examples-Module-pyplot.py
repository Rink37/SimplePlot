import SimplePlot as plt
import numpy as np

# Infinite lines

t = np.linspace(-10, 10, 100)
sig = 1 / (1+np.exp(-t))

hlines = [{'y':0, 'ls':'--'}, {'y':0.5, 'ls':':'}, {'y':1, 'ls':'--'}]
vlines = {'c':'grey', 'ls':'-'}
lines = {'o':(0,0.5), 's':0.25, 'ls':(0, (5,5))}
plt.plot({'xs':t, 'ys':sig, 'label':r'$\sigma(t) = \frac{1}{1+e^{-t}}$', 'xlabel':'t', 'xlim':[-10, 10], 'hline':hlines, 'vline':vlines, 'line':lines})

# Simple Plot

plt.plot({'xs':[0,1,2,3], 'ys':[1,2,3,4], 'markerstyle':'o', 'colour':'r', 'ylabel':'some numbers'})

# Text and mathtext using pyplot

t = np.arange(0.0, 2.0, 0.01)
s = np.sin(2*np.pi*t)

plt.plot({'xs':t, 'ys':s, 'title':r'$\mathcal{A}\sin(\omega t)$', 'xlabel':'Time [s]', 'ylabel':'Voltage [mV]', 'text':[0, -1, r'Hello, world!']})

# Multiple lines using pyplot 

t = np.arange(0, 5, 0.2)

plt.plot({'xs':[t,t,t], 'ys':[t,t**2,t**3], 'colour':['r', 'b', 'g'], 'markerstyle':['', 's', '^'], 'linestyle':['--', '', '']})

#Two subplots using pyplot

def f(t):
    return np.exp(-t)*np.cos(2*np.pi*t)

t1 = np.arange(0, 5, 0.1)
t2 = np.arange(0, 5, 0.02)

plt.plot([{'xs':[t1, t2], 'ys':[f(t1), f(t2)], 'colour':['tab:blue', 'black'], 'markerstyle':['o', None], 'linestyle':['', '-']},
          {'xs':t2, 'ys':np.cos(2*np.pi*t2), 'colour':'tab:orange', 'linestyle':'--'}], [[1,2], [1,2]])