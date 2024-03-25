# Copyright (C) 2024 Collimator, Inc.
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation, version 3. This program is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General
# Public License for more details.  You should have received a copy of the GNU
# Affero General Public License along with this program. If not, see
# <https://www.gnu.org/licenses/>.

""" Implements Discrete-time Infinite Horizon Kalman Filter LeafSystem """

import numpy as np
from ...backend import numpy_api as cnp

from .utils import linearize_and_discretize_continuous_plant

from .kalman_filter_base import KalmanFilterBase

from ...lazy_loader import LazyLoader

control = LazyLoader(
    "control", globals(), "control"
)  # For formatting state-space systems


class InfiniteHorizonKalmanFilter(KalmanFilterBase):
    """
    Infinite Horizon Kalman Filter for the following system:

    ```
    x[n+1] = A x[n] + B u[n] + G w[n]
    y[n]   = C x[n] + D u[n] + v[n]

    E(w[n]) = E(v[n]) = 0
    E(w[n]w'[n]) = Q
    E(v[n]v'[n]) = R
    E(w[n]v'[n]) = N = 0
    ```

    Input ports:
        (0) u[n] : control vector at timestep n
        (1) y[n] : measurement vector at timestep n

    Output ports:
        (1) x_hat[n] : state vector estimate at timestep n

    Parameters:
        dt: float
            Time step of the discrete-time system
        A: ndarray
            State transition matrix
        B: ndarray
            Input matrix
        C: ndarray
            Output matrix
        D: ndarray
            Feedthrough matrix
        G: ndarray
            Process noise matrix
        Q: ndarray
            Process noise covariance matrix
        R: ndarray
            Measurement noise covariance matrix
        x_hat_0: ndarray
            Initial state estimate
    """

    def __init__(
        self,
        dt,
        A,
        B,
        C,
        D,
        G,
        Q,
        R,
        x_hat_0,
        name=None,
    ):
        # Note: This class inherits from KalmanFilterBase. Since the infinite horizon
        # kalman filter does not need P_hat and track it, a dummy_P_hat_0 is set as
        # Identity matrix of size 1, and used wherever KalmanFilterBase demands
        # P_hat-like matrices

        self.dummy_P_hat_0 = cnp.eye(1)
        super().__init__(dt, x_hat_0, self.dummy_P_hat_0, name)

        self.A = A
        self.B = B
        self.C = C
        self.D = D
        self.G = G
        self.Q = Q
        self.R = R

        self.nx, self.nu = B.shape
        self.ny = C.shape[0]

        L, P, E = control.dlqe(A, G, C, Q, R)

        self.K = np.linalg.solve(A, L)

        self.A_minus_LC = A - np.matmul(L, C)
        self.B_minus_LD = B - np.matmul(L, D)
        self.L = L

    def _correct(self, time, x_hat_minus, P_hat_minus, *inputs):
        u, y = inputs
        u = cnp.atleast_1d(u)
        y = cnp.atleast_1d(y)

        C, D = self.C, self.D

        x_hat_plus = x_hat_minus + cnp.dot(
            self.K, y - cnp.dot(C, x_hat_minus) - cnp.dot(D, u)
        )  # n|n

        return x_hat_plus, self.dummy_P_hat_0

    def _propagate(self, time, x_hat_plus, P_hat_plus, *inputs):
        u, y = inputs
        u = cnp.atleast_1d(u)

        x_hat_minus = (
            cnp.dot(self.A_minus_LC, x_hat_plus)
            + cnp.dot(self.B_minus_LD, u)
            + cnp.dot(self.L, y)
        )  # n+1|n

        return x_hat_minus, self.dummy_P_hat_0

    #######################################
    # Make filter for a continuous plant  #
    #######################################

    @staticmethod
    def for_continuous_plant(
        plant,
        x_eq,
        u_eq,
        dt,
        Q,
        R,
        G=None,
        x_hat_bar_0=None,
        discretization_method="zoh",
        discretized_noise=False,
        name=None,
    ):
        """
        Obtain an Infinite Horizon Kalman Filter system for a continuous-time plant
        after linearization at equilibrium point (x_eq, u_eq)

        The input plant contains the deterministic forms of the forward and observation
        operators:

        ```
            dx/dt = f(x,u)
            y = g(x,u)
        ```

        Note: (i) Only plants with one vector-valued input and one vector-valued output
        are currently supported. Furthermore, the plant LeafSystem/Diagram should have
        only one vector-valued integrator. (ii) the user may pass a plant with
        disturbances as the input plant. However, computation of `y_eq` will be fraught
        with disturbances.

        A plant with disturbances of the following form is then considered
        following form:

        ```
            dx/dt = f(x,u) + G w                        --- (C1)
            y = g(x,u) +  v                             --- (C2)
        ```

        where:

            `w` represents the process noise,
            `v` represents the measurement noise,

        and

        ```
            E(w) = E(v) = 0
            E(ww') = Q
            E(vv') = R
            E(wv') = N = 0
        ```

        This plant with disturbances is linearized (only `f` and `g`) around the
        equilibrium point to obtain:

        ```
            d/dt (x_bar) = A x_bar + B u_bar + G w
            y_bar = C x_bar + D u_bar + v
        ```

        where,

        ```
            x_bar = x - x_eq
            u_bar = u - u_eq
            y_bar = y - y_bar
            y_eq = g(x_eq, u_eq)
        ```

        The linearized plant is then discretized via `euler` or `zoh` method to obtain:

        ```
            x_bar[n] = Ad x_bar[n] + Bd u_bar[n] + Gd w[n]           --- (L1)
            y_bar[n] = Cd x_bar[n] + Dd u_bar[n] + v[n]              --- (L2)

            E(w[n]) = E(v[n]) = 0
            E(w[n]w'[n]) = Qd
            E(v[n]v'[n]) = Rd
            E(w[n]v'[n]) = Nd = 0
        ```

        Note: If `discretized_noise` is True, then it is assumed that the user is
        providing Gd, Qd and Rd. If False, then Qd and Rd are computed from
        continuous-time Q, R, and G, and Gd is set to Identity matrix.

        An Infinite Horizon Kalman Filter estimator for the system of equations (L1)
        and (L2) is returned. This filter is in the `x_bar`, `u_bar`, and `y_bar`
        states.

        This returned system will have

        Input ports:
            (0) u_bar[n] : control vector at timestep n, relative to equilibrium
            (1) y_bar[n] : measurement vector at timestep n, relative to equilibrium

        Output ports:
            (1) x_hat_bar[n] : state vector estimate at timestep n, relative to
                               equilibrium

        Parameters:
            plant : a `Plant` object which can be a LeafSystem or a Diagram.
            x_eq: ndarray
                Equilibrium state vector for discretization
            u_eq: ndarray
                Equilibrium control vector for discretization
            dt: float
                Time step for the discretization.
            Q: ndarray
                Process noise covariance matrix.
            R: ndarray
                Measurement noise covariance matrix.
            G: ndarray
                Process noise matrix. If `None`, `G=B` is assumed making disrurbances
                additive to control vector `u`, i.e. `u_disturbed = u_orig + w`.
            x_hat_bar_0: ndarray
                Initial state estimate relative to equilibrium.
                If None, an identity matrix is assumed.
            discretization_method: str ("euler" or "zoh")
                Method to discretize the continuous-time plant. Default is "euler".
            discretized_noise: bool
                Whether the user is directly providing Gd, Qd and Rd. Default is False.
                If True, `G`, `Q`, and `R` are assumed to be Gd, Qd, and Rd,
                respectively.
        """
        (
            y_eq,
            Ad,
            Bd,
            Cd,
            Dd,
            Gd,
            Qd,
            Rd,
        ) = linearize_and_discretize_continuous_plant(
            plant, x_eq, u_eq, dt, Q, R, G, discretization_method, discretized_noise
        )

        nx = x_eq.size

        if x_hat_bar_0 is None:
            x_hat_bar_0 = cnp.zeros(nx)

        # Instantiate an Infinite Horizon Kalman Filter for the linearized plant
        kf = InfiniteHorizonKalmanFilter(
            dt,
            Ad,
            Bd,
            Cd,
            Dd,
            Gd,
            Qd,
            Rd,
            x_hat_bar_0,
            name=name,
        )

        return y_eq, kf
