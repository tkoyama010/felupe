# -*- coding: utf-8 -*-
"""
 _______  _______  ___      __   __  _______  _______ 
|       ||       ||   |    |  | |  ||       ||       |
|    ___||    ___||   |    |  | |  ||    _  ||    ___|
|   |___ |   |___ |   |    |  |_|  ||   |_| ||   |___ 
|    ___||    ___||   |___ |       ||    ___||    ___|
|   |    |   |___ |       ||       ||   |    |   |___ 
|___|    |_______||_______||_______||___|    |_______|

This file is part of felupe.

Felupe is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Felupe is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Felupe.  If not, see <http://www.gnu.org/licenses/>.

"""

import numpy as np

from types import SimpleNamespace

from ..math import (
    dot,
    ddot,
    ddot44,
    ddot444,
    transpose,
    majortranspose,
    inv,
    dya,
    cdya,
    cdya_ik,
    cdya_il,
    det,
    eigh,
    identity,
    trace,
    dev,
)


class Composite:
    def __init__(self, *args):

        self.materials = args
        self.kind = SimpleNamespace(**{"df": None, "da": None})

    def stress(self, *args, **kwargs):
        return np.sum([m.stress(*args) for m in self.materials], 0)

    def elasticity(self, *args, **kwargs):
        return np.sum([m.elasticity(*args, **kwargs) for m in self.materials], 0)


class Material:
    def __init__(self, stress, elasticity):
        """Updated-Lagrange / Eulerian Material class:
        stress = Kirchhoff stress tau = J sigma
        elasticity = associated 4th-order elasticity tensor J c4
        """

        self.stress = stress
        self.elasticity = elasticity
        self.kind = SimpleNamespace(**{"df": None, "da": None})


class InvariantBased:
    def __init__(self, umat, tol=np.finfo(float).eps):
        self.umat = umat
        self.kind = SimpleNamespace(**{"df": 0, "da": 0})
        self.b = 0

    def update(self, b):

        if np.all(b == self.b):
            pass
        else:
            self.invariants = np.array(
                [trace(b), (trace(b) ** 2 - trace(dot(b, b))) / 2, det(b)]
            )
            self.W_a, self.W_ab = self.umat(self.invariants)

    def stress(self, b):
        self.update(b)

        tau = np.zeros_like(b)

        I1, I2, I3 = self.invariants
        W1, W2, W3 = self.W_a

        if not np.all(W1 == 0):
            tau += 2 * W1 * b

        if not np.all(W2 == 0):
            tau += 2 * W2 * (I1 * b - dot(b, b))

        if not np.all(W3 == 0):
            eye = identity(b)
            tau += 2 * W3 * I3 * eye

        return tau

    def elasticity(self, b):
        self.update(b)

        ndim, ngauss, nelems = b.shape[-3:]
        Jc4 = np.zeros((ndim, ndim, ndim, ndim, ngauss, nelems))

        I = identity(b)

        I1, I2, I3 = self.invariants
        W1, W2, W3 = self.W_a
        W11 = self.W_ab[0, 0]
        W22 = self.W_ab[1, 1]
        W33 = self.W_ab[2, 2]
        W12 = self.W_ab[0, 1]
        W13 = self.W_ab[0, 2]
        W23 = self.W_ab[1, 2]

        a00 = W11 + W2 + I1 * W12
        a11 = W22
        a22 = W33 * I3 ** 2 + W3 * I3
        a01 = -(W12 + I1 * W22)
        a02 = W13 * I3 + W23 * I3 * I1
        a12 = -W23 * I3
        b00 = -W2
        b22 = W3 * I3

        if not np.all(a00 == 0):
            Jc4 += 4 * a00 * dya(b, b)

        if not np.all(a11 == 0):
            Jc4 += 4 * a11 * dya(dot(b, b), dot(b, b))

        if not np.all(a22 == 0):
            Jc4 += 4 * a22 * dya(I, I)

        if not np.all(a01 == 0):
            Jc4 += 4 * a01 * (dya(b, dot(b, b)) + dya(dot(b, b), b))

        if not np.all(a02 == 0):
            Jc4 += 4 * a02 * (dya(b, I) + dya(I, b))

        if not np.all(a12 == 0):
            Jc4 += 4 * a12 * (dya(dot(b, b), I) + dya(I, dot(b, b)))

        if not np.all(b00 == 0):
            Jc4 += 4 * b00 * cdya(b, b)

        if not np.all(b22 == 0):
            Jc4 += 4 * b22 * cdya(I, I)

        return Jc4


class PrincipalStretchBased:
    def __init__(self, umat, tol=np.finfo(float).eps):
        self.umat = umat
        self.kind = SimpleNamespace(**{"df": 0, "da": 0})
        self.b = 0
        self.tol = tol

    def update(self, b):
        if np.all(b == self.b):
            pass
        else:
            wb, vb = eigh(b)

            self.stretches = np.sqrt(wb)
            self.bases = np.array([dya(N, N, mode=1) for N in transpose(vb)])

            self.W_a, self.W_ab = self.umat(self.stretches)

    def stress(self, b):
        self.update(b)

        return np.sum(
            [Wa * la * ma for Wa, la, ma in zip(self.W_a, self.stretches, self.bases)],
            0,
        )

    def elasticity(self, b):
        self.update(b)

        ndim, ngauss, nelems = b.shape[-3:]
        Jc4 = np.zeros((ndim, ndim, ndim, ndim, ngauss, nelems))

        for a in range(3):
            Wa = self.W_a[a]
            Ma = self.bases[a]
            la = self.stretches[a]

            Jc4 -= Wa / la * dya(Ma, Ma)

            for b in range(3):
                Wb = self.W_a[b]
                Wab = self.W_ab[a, b]
                Mb = self.bases[b]
                lb = self.stretches[b]

                Jc4 += Wab * dya(Ma, Mb)

                if b != a:
                    la[abs(la - lb) < self.tol] += self.tol
                    Gab = cdya(Ma, Mb) + cdya(Mb, Ma)
                    Jc4 += (Wa * la - Wb * lb) / (la ** 2 - lb ** 2) * Gab

        return Jc4


class Hydrostatic:
    def __init__(self, bulk):
        self.bulk = bulk
        self.kind = SimpleNamespace(**{"df": None, "da": None})

    def dUdJ(self, J):
        return self.bulk * (J - 1)

    def d2UdJdJ(self, J):
        return self.bulk

    def stress(self, F, J, b, invb):
        return self.dUdJ(J) * J * identity(b)

    def elasticity(self, F, J, b, invb):
        eye = identity(b)
        p = self.dUdJ(J)
        q = p + self.d2UdJdJ(J) * J
        return J * (q * dya(eye, eye) - 2 * p * cdya(eye, eye))


class AsIsochoric:
    def __init__(self, material_isochoric):
        self.isochoric = material_isochoric
        self.kind = SimpleNamespace(**{"df": None, "da": None})

    def stress(self, F, J, b, invb):
        bu = J ** (-2 / 3) * b
        tb = self.isochoric.stress(bu)
        return dev(tb)

    def elasticity(self, F, J, b, invb):
        eye = identity(b)
        p4 = cdya(eye, eye) - dya(eye, eye) / 3

        bu = J ** (-2 / 3) * b
        tb = self.isochoric.stress(bu)

        Jc4b = self.isochoric.elasticity(bu)
        if np.all(Jc4b == 0):
            PJc4bP = Jc4b
        else:
            PJc4bP = ddot444(p4, Jc4b, p4)

        return (
            PJc4bP
            - 2 / 3 * (dya(tb, eye) + dya(eye, tb))
            + 2 / 9 * trace(tb) * dya(eye, eye)
            + 2 / 3 * trace(tb) * cdya(eye, eye)
        )
