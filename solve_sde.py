#!/usr/bin/python
# -*- coding: utf-8 -*- #
"""
Simple stochastic differential equation solver
"""

import numpy as np
import pylab as pl

__author__ = 'Lampros Mountrakis'
__version__ = '0.1b'

randn = np.random.randn


def solve_sde(alfa=None, beta=None, X0=None, dt=1.0, N=100, t0=0.0, DW=None):
    """


            Kloeden - Numerical Solution of stochastic differential
            equations (Springer 1992)  page XXX.
            Strong order 1.0 Runge Kutta scheme.
            http://en.wikipedia.org/wiki/Runge%E2%80%93Kutta_method_%28SDE%29

            dX = a(X,t)*dt + b(X, t)*dW

    Syntax:
    ----------
    solve_sde(alfa=None, beta=None, X0=None, dt=None, N=100, t0=0, DW=None)


    Parameters:
    ----------
        alfa  : a lambda function with two arguments, the X state and the time
                defines the differential equation.
        beta  : a lambda function with two arguments, the X state and the time
                defines the stochastic part of the SDE.
        X0    : Initial conditions of the SDE. Mandatory for SDEs
                with variables > 1 (default: gaussian np.random)
        dt    : The timestep of the solution
                (default: 1)
        N     : The number of timesteps (defines the length of the timeseries)
                (default: 100)
        t0    : The initial time of the solution
                (default: 0)
        DW    : The Wiener function in lambda notation
                (default: gaussian np.random number generator, \
                    [lambda Y, dt: randn(len(X0)) * np.sqrt(dt)] )


    Examples:
    ----------

    == Simple Wiener Process:
    dX = 0 + 1*dW


    alfa = lambda X,t: 0
    beta = lambda X,t: 1
    t, Y = solve_sde(alfa=alfa, beta=beta, dt=1, N=1000)



    == Stochastic Lorenz Equation:
    dX = s (Y - X) + Y * dW1
    dY = (r X - Y - X*Z) + dW2
    dZ = (X*Y - b Z)  + dW3


    xL = lambda X, t: 10.0 * (X[1] - X[0])  ;
    yL = lambda X, t: 28.0 * X[0] - X[1] - X[0] * X[2] ;
    zL = lambda X, t: X[0] * X[1] - 8.0/3.0 * X[2] ;

    alfa = lambda X, t: np.array( [xL(X,t), yL(X,t), zL(X,t)] );
    beta = lambda X, t: np.array( [     X[1],      1,      1] );
    X0 = [3.4, -1.3, 28.3];
    t, Y = solve_sde(alfa=alfa, beta=beta, X0=X0, dt=0.01, N=10000)

"""
    if alfa is None or beta is None:
        print "Error: SDE not defined."
        return
    X0 = randn(np.array(alfa(0, 0)).shape or 1) if X0 is None else np.array(X0)
    DW = (lambda Y, dt: randn(len(X0)) * np.sqrt(dt)) if DW is None else DW
    Y, ti = np.zeros((N, len(X0))), np.arange(N)*dt + t0
    Y[0, :], Dn, Wn = X0, dt, 1

    for n in range(N-1):
        t = ti[n]
        a, b, DWn = alfa(Y[n, :], t), beta(Y[n, :], t), DW(Y[n, :], dt)
        # print Y[n,:]
        Y[n+1, :] = Y[n, :] + a*Dn + b*DWn*Wn + \
                    0.5*(beta(Y[n, :] + a * Dn + b*np.sqrt(Dn), t) - b) * \
                    (DWn**2.0 - Dn)/np.sqrt(Dn)
    return ti, Y


if __name__ == '__main__':
    pl.subplot(211)  # Simple Wiener Process
    alfa_wp = lambda X, t: 0
    beta_wp = lambda X, t: 1
    tWP1, YWP1 = solve_sde(alfa=alfa_wp, beta=beta_wp, dt=1, N=100)
    pl.plot(tWP1, YWP1[:, 0], label='$dt=1$')
    tWP2, YWP2 = solve_sde(alfa=alfa_wp, beta=beta_wp, dt=.1, N=1000)
    pl.plot(tWP2, YWP2[:, 0], label='$dt=10^{-1}$')
    tWP3, YWP3 = solve_sde(alfa=alfa_wp, beta=beta_wp, dt=.01, N=10000)
    pl.plot(tWP3, YWP3[:, 0], label='$dt=10^{-2}$')
    pl.title('Wiener process')
    pl.xlabel('t')
    pl.ylabel('X(t)')
    pl.legend(loc='best')
    pl.subplot(212)  # Stochastic Lorenz Equation:
    xL = lambda Y, t: 10.0 * (Y[1] - Y[0])
    yL = lambda Y, t: 28.0 * Y[0] - Y[1] - Y[0] * Y[2]
    zL = lambda Y, t: Y[0] * Y[1] - 8.0/3.0 * Y[2]
    alfa_sl = lambda Y, t: np.array([xL(Y, t), yL(Y, t), zL(Y, t)])
    beta_sl = lambda Y, t: np.array([0.5*Y[1], 1, 1])
    Y0 = [3.4, -1.3, 28.3]
    tSLE, YSLE = solve_sde(alfa=alfa_sl, beta=beta_sl, X0=Y0, dt=0.01, N=5000)
    # pl.plot(t, Y[:,0], label='X(t)')
    # pl.plot(t, Y[:,1], label='Y(t)')
    # pl.plot(t, Y[:,2], label='Z(t)')
    pl.subplot(223)
    pl.plot(YSLE[:, 0], YSLE[:, 1])
    pl.xlabel('X(t)')
    pl.ylabel('Y(t)')
    pl.title('Geometric stochastic Lorenz system')
    pl.subplot(224)
    pl.plot(YSLE[:, 0], YSLE[:, 2])
    pl.xlabel('X(t)')
    pl.ylabel('Z(t)')
    pl.show()
