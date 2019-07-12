import time
import psutil
import matplotlib.pyplot as plt

#matplot notebook

plt.rcParams['animation.html'] = 'jshtml'
fig = plt.figure()
ax = fig.add_subplot(111)
fig.show()
i = 0

psutil.cpu_percent()

x, y = [], []
while True:
    x.append(i)
    y.append(psutil.cpu_percent())
    ax.plot(x,y,color='b')
    fig.canvas.draw()

    #limitare:
    ax.set_xlim(left=max(0, i-50), right=i+50)

    time.sleep(60)
    i += 1
