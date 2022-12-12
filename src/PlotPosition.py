import numpy as np
import matplotlib.pyplot as plt
import ImportCSVData as dt
from matplotlib.widgets import Button

file = 'results/12-12-2022_11-20-17_R-1_SYNC-true_POSITIONS.csv'
data = dt.getData(file)

rounds = dt.getElmentsAtIndex(data, 0)
rounds = dt.getRounds(rounds)
x = dt.getXByRound(0, data)
y = dt.getYByRound(0, data)
clusterSizes = dt.getClusterSizes(list(zip(x,y)))
xmean = np.mean(x)
ymean = np.mean(y)
print(clusterSizes)

fig, ax = plt.subplots()
fig.subplots_adjust(bottom=0.2)
l, = ax.plot(x, y, 'o')
g, = ax.plot(xmean, ymean, 'o')
ax.grid(True)

axround = fig.add_axes([0.4, 0.05, 0.15, 0.075])
axround.get_xaxis().set_visible(False)
axround.get_yaxis().set_visible(False)
txt = axround.text(0.15,0.4, "Round: " + str(0))

class Index:
    ind = 0

    def next(self, event):
        self.ind += 1
        self.ind = self.ind % len(rounds)
        self.refresh()

    def prev(self, event):
        self.ind -= 1
        self.ind = self.ind % len(rounds)
        self.refresh()
    
    def refresh(self):
        xdata = dt.getXByRound(rounds[self.ind], data)
        ydata = dt.getYByRound(rounds[self.ind], data)
        l.set_xdata(xdata)
        l.set_ydata(ydata)
        xmean = np.mean(xdata)
        ymean = np.mean(ydata)
        g.set_xdata(xmean)
        g.set_ydata(ymean)
        txt.set_text("Round: " + str(rounds[self.ind]))
        plt.draw()

    def annotateData(): #TODO
        ax.annotate()

callback = Index()
axprev = fig.add_axes([0.7, 0.05, 0.1, 0.075])
axnext = fig.add_axes([0.81, 0.05, 0.1, 0.075])
bnext = Button(axnext, 'Next')
bnext.on_clicked(callback.next)
bprev = Button(axprev, 'Previous')
bprev.on_clicked(callback.prev)
plt.show()