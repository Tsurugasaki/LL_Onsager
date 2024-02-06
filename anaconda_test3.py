import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np 

# 初期値
k = 1
L = 1
N = 21
dx = L/N
T = 100
dt = 0.001

u = np.zeros((T,N)) #全てに0を入れておく

for t in range(0,T):
    for x in range(0,N-1):
        if t == 0:
            u[t][x] = -20*x*dx*(x*dx-1)
        else:
            if x == 0 or x == N-1:
                u[t][x] = 0
            else:
                u[t][x] = k*dt/(dx**2)*(u[t-1][x+1]-2*u[t-1][x]+u[t-1][x-1]) + u[t-1][x]

plt_x = np.linspace(0,L,N)

fig = plt.figure()
ims = []
for i in range(0,T):
    im = plt.plot(plt_x,u[i],color='#4169e1')
    ims.append(im)

ani = animation.ArtistAnimation(fig, ims, interval=200)

plt.show()