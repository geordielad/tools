#!/usr/bin/python
import unittest
import numpy as np

def vertmode(N2, Z, n, make_plot):
    # function [Vmode, Hmode, c] = vertmode(N2, Z, n, make_plot)
    # Takes input N2 -> Buoyancy frequency squared (@ mid pts of Z)
    #              Z -> Vertical co-ordinate
    #              n -> No. of modes to isolate
    # Max. number of nodes is length(Z)-1
    # Returns
    #             Vmode -> Vertical structure for vertical velocity
    #             Hmode -> Vertical structure for horizontal velocities, pressure
    # c(i) -> Gravity Wave speed of i-th mode

    #    if ~exist('make_plot','var'), make_plot = 1; end

    lz = len(Z)
    if Z.shape[0] == 1:
        Z = Z.T

    if n > (lz-1):
        print('\n n too big. Reducing to (length(Z) - 1)')
        n = lz - 1

    # Following Chelton (1998)
    # Q'AW = (lambda)W

    D = np.zeros_like(Z)
    D[0] = Z[1]/2
    D[1:-1] = (Z[2:]-Z[0:-2])/2
    D[-1] = (Z[-1] - Z[-2])/2
    Zmid = (Z[:-1] + Z[1:])/2

    Q1 = np.zeros(lz-1)

    for k in range(len(Q1)):
        Q1[k] = 2/(D[k]*D[k+1]*(D[k] + D[k+1]))

    Q = np.diag(Q1/N2)
    A = -1*(np.diag(D[:-1]) + np.diag(D[1:])) + \
        np.diag(D[:-2], 1) + np.diag(D[2:], -1)

    [e, G] = np.linalg.eig(np.dot(Q, A))

    c = np.sqrt(-1/e)
    ind = np.argsort(c)  # ascending order

    F = np.zeros([lz-2, lz-1])

    for i in range(F.shape[1]):
        F[:, i] = (c[i]**2/9.81)*(np.diff(G[:, i])/np.diff(Zmid))

    Hmode = np.fliplr(F[:, ind[lz-n:lz-1]])
    Vmode = np.fliplr(G[:, ind[lz-n:lz-1]])

    print(Hmode.shape)
    # Fill in Hmode at lowest depth
    Hmode = np.vstack([Hmode, Hmode[-2, :]])
    c = np.flipud(c[ind[lz-n:lz-1]])

    return [Vmode, Hmode, c]

    # Normalize by max. amplitude
    #Hmode = Hmode./np.repmat(max(abs(Hmode)), len(Hmode), 1)
    #Vmode = Vmode./np.repmat(max(abs(Vmode)), len(Vmode), 1)

    # Normalize by energy (following Wunsch(1999)
    # why am I doing this using Hmode norm?
    norm = np.sqrt(sum(avg1(Vmode)**2 * np.repmat(np.diff(Zmid), 1, n)))
    Vnorm = Vmode / np.repmat(norm, lz-1, 1)
    norm = np.sqrt(sum(avg1(Hmode)**2 * np.repmat(np.diff(Zmid), 1, n)))
    Hnorm = Hmode / np.repmat(norm, lz-1, 1)

    # Plot first n modes
    if make_plot:
        import matplotlib.pyplot as plt
        plt.figure()
        ax[0] = plt.subplot(131)
        plt.plot(N2, Zmid)
        plt.title('N^2')
        plt.ylabel('Z (m)')
        #if Z > 0: set(gca,'ydir','reverse')

        ax[2] = plt.subplot(132)
        plt.plot(Vmode, Zmid)
        plt.hold(True)
        plt.axvline(0)
        ylabel('Z (m)')
        title('Vertical Structure of Vertical Velocity')
        plt.legend(str(np.arange(n)+1))
        #if Z > 0: set(gca,'ydir','reverse')
        #beautify

        ax[3] = plt.subplot(133)
        plt.plot(Hmode, Zmid)
        set(gca, 'ydir', 'reverse')
        plt.hold(True)
        plt.axvline(0)
        plt.axvline(4000)
        ylabel('Z (m)')
        title('Vertical Structure of Horizontal Velocity')
        legend(str(np.arange(n)+1))
        linkaxes(ax, 'y')

        if Z > 0:
            set(gca, 'ydir', 'reverse')

    return [Vmode, Hmode, c]


def avg1(a):
    return (a[:-1]+a[1:])/2


class oceanTests(unittest.TestCase):
    def test_vertmode(self):
        # create z-vector
        Z = np.linspace(0, 1, 50)

        # constant Nsquared
        N2 = np.ones_like(Z[:-1])

        # z-vector for calculated mode
        Zmode = avg1(Z)

        # number of modes to calculate
        n = 4

        # calculate modes
        [Vmode, Hmode, c] = vertmode(N2, Z, n, 0)

        # test normalization
        hchk = np.sum(avg1(Hmode)**2 * np.repmat(np.diff(Zmode), 1, n))
        vchk = np.sum(avg1(Vmode * np.repmat(N2, 1, n))**2 \
                      * np.repmat(np.diff(Zmode), 1, n))

        #print('\n u mode normalization: \n')
        #print(hchk)
        #print('\n w mode normalization: \n')
        #print(vchk)

        # check against sine / cosines
#        Vchk = np.sin()