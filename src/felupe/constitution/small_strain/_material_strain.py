# -*- coding: utf-8 -*-
"""
This file is part of FElupe.

FElupe is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

FElupe is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with FElupe.  If not, see <http://www.gnu.org/licenses/>.
"""

import numpy as np

from ...math import identity, ravel, reshape, sym
from .._base import ConstitutiveMaterial


class MaterialStrain(ConstitutiveMaterial):
    """A strain-based user-defined material definition with a given function
    for the stress tensor and the (fourth-order) elasticity tensor.

    Take this code-block from the linear-elastic material formulation

    ..  code-block::

        from felupe.math import identity, cdya, dya, trace

        def linear_elastic(dε, εn, σn, ζn, λ, μ, **kwargs):
            '''3D linear-elastic material formulation.

            Arguments
            ---------
            dε : ndarray
                Incremental strain tensor.
            εn : ndarray
                Old strain tensor.
            σn : ndarray
                Old stress tensor.
            ζn : ndarray
                Old state variables.
            λ : float
                First Lamé-constant.
            μ : float
                Second Lamé-constant (shear modulus).
            '''

            # change of stress due to change of strain
            I = identity(dε)
            dσ = 2 * μ * dε + λ * trace(dε) * I

            # update stress and evaluate elasticity tensor
            σ = σn + dσ
            dσdε = 2 * μ * cdya(I, I) + λ * dya(I, I)

            # update state variables (not used here)
            ζ = ζn

            return dσdε, σ, ζ

        umat = MaterialStrain(material=linear_elastic, μ=1, λ=2)

    or this minimal header as template:

    ..  code-block::

        def fun(dε, εn, σn, ζn, **kwargs):
            return dσdε, σ, ζ

        umat = MaterialStrain(material=fun, **kwargs)

    See Also
    --------
    linear_elastic : 3D linear-elastic material formulation
    linear_elastic_plastic_isotropic_hardening : Linear-elastic-plastic material
        formulation with linear isotropic hardening (return mapping algorithm).
    LinearElasticPlasticIsotropicHardening : Linear-elastic-plastic material
        formulation with linear isotropic hardening (return mapping algorithm).

    """

    def __init__(self, material, dim=3, statevars=(0,), **kwargs):
        self.material = material
        self.statevars_shape = statevars
        self.statevars_size = [np.prod(shape) for shape in statevars]
        self.statevars_offsets = np.cumsum(self.statevars_size)
        self.nstatevars = sum(self.statevars_size)

        self.kwargs = {**kwargs, "tangent": None}

        self.dim = dim
        self.x = [np.eye(dim), np.zeros(2 * dim**2 + self.nstatevars)]

        self.stress = self.gradient
        self.elasticity = self.hessian

    def extract(self, x):
        "Extract the input and evaluate strains, stresses and state variables."

        # unpack deformation gradient F = dx/dX
        dim = self.dim
        dxdX, statevars = x

        # small-strain tensor as strain = sym(dx/dX - 1)
        dudx = dxdX - identity(dxdX)
        strain = sym(dudx)

        # separate strain and stress from state variables
        statevars_all = np.split(
            statevars, [*self.statevars_offsets, self.nstatevars + dim**2]
        )
        strain_old_1d, stress_old_1d = statevars_all[-2:]

        # list of state variables with original shapes
        shapes = self.statevars_shape
        statevars_old = [
            reshape(sv, shape).copy() for sv, shape in zip(statevars_all[:-2], shapes)
        ]

        # reshape strain and stress from (dim**2,) to (dim, dim)
        strain_old = strain_old_1d.reshape(dim, dim, *strain_old_1d.shape[1:])
        stress_old = stress_old_1d.reshape(dim, dim, *stress_old_1d.shape[1:])

        # change of strain
        dstrain = strain - strain_old

        return strain_old, dstrain, stress_old, statevars_old

    def gradient(self, x):
        strain_old, dstrain, stress_old, statevars_old = self.extract(x)
        self.kwargs["tangent"] = False

        dsde, stress_new, statevars_new_list = self.material(
            dstrain, strain_old, stress_old, statevars_old, **self.kwargs
        )

        strain_new_1d = (strain_old + dstrain).reshape(-1, *strain_old.shape[2:])
        stress_new_1d = stress_new.reshape(-1, *strain_old.shape[2:])

        statevars_new = np.concatenate(
            [*[ravel(sv) for sv in statevars_new_list], strain_new_1d, stress_new_1d],
            axis=0,
        )

        return [stress_new, statevars_new]

    def hessian(self, x):
        strain_old, dstrain, stress_old, statevars_old = self.extract(x)
        self.kwargs["tangent"] = True

        dsde = self.material(
            dstrain, strain_old, stress_old, statevars_old, **self.kwargs
        )[0]

        # ensure minor-symmetric elasticity tensor due to symmetry of strain
        dsde = (
            dsde
            + np.einsum("ijkl...->jikl...", dsde)
            + np.einsum("ijkl...->ijlk...", dsde)
            + np.einsum("ijkl...->jilk...", dsde)
        ) / 4

        return [dsde]
