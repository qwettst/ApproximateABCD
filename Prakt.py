import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import ConsultFun as csltFn


def function(x, a, b, c, d):
    return a + b * np.sin(c * x + d)


def functionZ(x, c, d):
    return np.sin(c * x + d)


def se_(y, yReplica):
    return np.abs(y - yReplica).sum()


if __name__ == '__main__':
    # Данные X и Y, изначальная функция
    X1 = []
    i = 0
    while i <= 3:
        X1.append(i)
        i += 0.1
    X1 = np.array(X1)
    y = np.sin(X1)

    # Параметр D - const, c - изменяется
    startC = -10
    endC = 10
    stepC = (endC - startC) / len(y)

    startD = 0
    endD = 2
    stepD = 0.1

    sC = []
    sD = []

    sC.append((startC, endC, stepC))
    sD.append((startD, endD, stepD))

    sC = pd.DataFrame(sC, columns=['start', 'end', 'step'])
    sD = pd.DataFrame(sD, columns=['start', 'end', 'step'])

    fig = plt.figure()
    ax1 = fig.add_subplot(2, 2, 1)
    ax2 = fig.add_subplot(2, 2, 2)
    ax3 = fig.add_subplot(2, 2, 3)

    # График С
    ax1, minErrA = csltFn.funCconstD(fig, 1, X1, y, sC, sD)
    ax1.plot(minErrA['c'], minErrA['SE'], 'ro')

    # Параметр C - const, d - изменяется
    startC = 0
    endC = 1
    stepC = 0.1

    startD = -10
    endD = 10
    stepD = (endD - startD) / len(y)

    sC['start'].iloc[0] = startC
    sC['end'].iloc[0] = endC
    sC['step'].iloc[0] = stepC

    sD['start'].iloc[0] = startD
    sD['end'].iloc[0] = endD
    sD['step'].iloc[0] = stepD

    # График D
    ax2, minErrB = csltFn.funDconstC(fig, 2, X1, y, sC, sD)
    ax2.plot(minErrB['d'], minErrB['SE'], 'ro')

    # Минимальная ошибка, minnErrA = minErrB
    min = minErrA['SE'].idxmin()
    c = minErrA['c'].iloc[min]
    d = minErrA['d'].iloc[min]

    sZ = functionZ(X1, c, d)
    a, b = csltFn.sse_AB(sZ, y)  # МНК, для параметров a и b

    yReplica = a + b * sZ  # Аппроксимация

    i = X1.min()
    step_i = (X1.max() - i) / 100
    arr_x = []
    arr_y = []
    while i <= X1.max():
        arr_x.append(i)
        arr_y.append(function(i, a, b, c, d))
        i += step_i

    ax1.set_xlabel(u'c')
    ax1.set_ylabel(u'se')
    ax1.set_title("Сумма ошибок func(c)")
    # ax1.legend()

    ax2.set_xlabel(u'd')
    ax2.set_ylabel(u'se')
    ax2.set_title("Сумма ошибок func(d)")
    # ax2.legend()

    ax3.plot(X1, y, 'ro')
    ax3.plot(arr_x, arr_y,
             label='y=' + str(round(a, 3)) + '+ ' + str(round(b, 3)) + '*sin(' + str(round(c, 3)) + '*x+' + str(
                 round(d, 2)) + ')')
    ax3.set_xlabel(u'x')
    ax3.set_ylabel(u'y')
    ax3.set_title("func")
    ax3.legend()

    oshibka = 100 * 1 / len(X1) * np.abs(y - yReplica).sum() / (1 / len(X1) * y.sum())

    se = se_(y, yReplica)

    print('c=' + str(round(c, 3)) + '  d= ' + str(round(d, 3)) + ' SE= ' + str(round(minErrA['SE'].iloc[min], 3)))
    print('oshibka=' + str(oshibka))
    print('se= ' + str(se))
    plt.show()
    plt.show()
