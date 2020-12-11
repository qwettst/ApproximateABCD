import numpy as np
import pandas as pd


def function(x, c, d):
    return np.sin(c * x + d)

def se_(y, yReplica):
    return np.abs(y - yReplica).sum()


def funCconstD(fig, indFig, sX, sY, sC, sD):
    minErrA = []
    d = sD['start'].iloc[0]
    ax1 = fig.add_subplot(2, 2, indFig)
    step = sC['step'].iloc[0]
    step = 0.1
    while d <= sD['end'].iloc[0]:
        seDf = []
        c = sC['start'].iloc[0]
        while c < sC['end'].iloc[0]:
            yReplica = []
            yReplica = function(sX, c, d)
            if not np.isnan(np.sum(yReplica)):
                se = se_(sY, yReplica)
                seDf.append((c, se))
            c += step
        if len(seDf) != 0:
            seDf = pd.DataFrame(seDf, columns=['iter', 'SE'])
            ax1.plot(seDf['iter'], seDf['SE'], label="d= " + str(d))
            minInd = seDf['SE'].idxmin()
            minErrA.append((seDf['iter'].iloc[minInd], d, seDf['SE'].iloc[minInd]))
        d += sD['step'].iloc[0]
    minErrA = pd.DataFrame(minErrA, columns=['c', 'd', 'SE'])
    return ax1, minErrA


def funDconstC(fig, indFig, sX, sY, sC, sD):
    minErrB = []
    c = sC['start'].iloc[0]
    ax2 = fig.add_subplot(2, 2, indFig)
    step = sD['step'].iloc[0]
    step = 0.1
    while c <= sC['end'].iloc[0]:
        seDf = []
        d = sD['start'].iloc[0]
        while d < sD['end'].iloc[0]:
            yReplica = []
            yReplica = function(sX, c, d)
            if not np.isnan(np.sum(yReplica)):
                se = se_(sY, yReplica)
                seDf.append((d, se))
            d += step
        if len(seDf) != 0:
            seDf = pd.DataFrame(seDf, columns=['iter', 'SE'])
            ax2.plot(seDf['iter'], seDf['SE'], label="c= " + str(c))
            minInd = seDf['SE'].idxmin()
            minErrB.append((c, seDf['iter'].iloc[minInd], seDf['SE'].iloc[minInd]))
        c += sC['step'].iloc[0]
    minErrB = pd.DataFrame(minErrB, columns=['c', 'd', 'SE'])
    return ax2, minErrB


def sse_AB(sX, sY):
    sumXY = 0
    sumX = 0
    sumXX = 0
    sumY = 0
    n = len(sX)
    for i in range(len(sX)):
        sumXY += sX[i] * sY[i]
        sumX += sX[i]
        sumY += sY[i]
        sumXX += sX[i]*sX[i]
    b = (n * sumXY - sumX*sumY) / (n * sumXX - sumX*sumX)
    a = (sumY - b * sumX) / n

    return a, b
