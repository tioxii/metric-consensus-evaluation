import numpy as np
import matplotlib.pyplot as plt
import ImportCSVData as dt
from matplotlib.widgets import Button

def main():
    file = 'positions/test.csv'
    data = dt.getData(file)

    rounds = dt.getElmentsAtIndex(data, 0)
    rounds = dt.getRounds(rounds)
    x = dt.getXByRound(0, data)
    y = dt.getYByRound(0, data)
    clusterSizes = dt.getClusterSizes(list(zip(x,y)))
    xmean = np.mean(x)
    ymean = np.mean(y)

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
        anns = []

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
            clusterSizes = dt.getClusterSizes(list(zip(xdata,ydata)))
            self.clearAnnotations()
            self.annotateData(clusterSizes)
            xmean = np.mean(xdata)
            ymean = np.mean(ydata)
            g.set_xdata(xmean)
            g.set_ydata(ymean)
            txt.set_text("Round: " + str(rounds[self.ind]))
            plt.draw()

        def annotateData(self, clusterSizes):
            for i, txt in enumerate(clusterSizes):
                ann = ax.annotate(txt[1], txt[0])
                self.anns.append(ann)
        
        def clearAnnotations(self):
            for x in self.anns:
                x.remove()
            self.anns = []

    callback = Index()
    axprev = fig.add_axes([0.7, 0.05, 0.1, 0.075])
    axnext = fig.add_axes([0.81, 0.05, 0.1, 0.075])
    bnext = Button(axnext, 'Next')
    bnext.on_clicked(callback.next)
    bprev = Button(axprev, 'Previous')
    bprev.on_clicked(callback.prev)
    plt.show()

if __name__ == '__main__':
    main()