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

""" Utilities for state estimators """

import jax
import jax.numpy as jnp
import jax.scipy as jsp

from jax.flatten_util import ravel_pytree

from .. import linearize
from ..utils import make_ode_rhs


def discretize_forward_zoh(A, B, dt):
    """
    Discretize a continuous-time forward model `dot_x = A x + B u` using zero-order
    hold (ZOH) discretization.

    Parameters:
    A : jnp.ndarray
        The state matrix.
    B : jnp.ndarray
        The input matrix.
    dt : float
        The time step.

    Returns:
    Ad : jnp.ndarray
        The discretized state matrix.
    Bd : jnp.ndarray
        The discretized input matrix.

    The discretized system follows the dynamics:

    x[k+1] = Ad x[k] + Bd u[k]
    """
    Ad = jsp.linalg.expm(A * dt)
    # Assume A is nonsingular (TODO: handle singular A)
    Bd = jnp.linalg.inv(A) @ (Ad - jnp.eye(A.shape[0])) @ B
    return Ad, Bd


def discretize_forward_euler(A, B, dt):
    """
    Discretize a continuous-time forward model `dot_x = A x + B u` using forward Euler
    discretization.

    Parameters:
    A : jnp.ndarray
        The state matrix.
    B : jnp.ndarray
        The input matrix.
    dt : float
        The time step.

    Returns:
    Ad : jnp.ndarray
        The discretized state matrix.
    Bd : jnp.ndarray
        The discretized input matrix.

    The discretized system follows the dynamics:

    x[k+1] = Ad x[k] + Bd u[k]
    """
    nx = A.shape[0]
    Ad = jnp.eye(nx) + A * dt
    Bd = B * dt
    return Ad, Bd


def discretize_Q_zoh(G, Q, A, dt):
    """
    For a linear system `dot_x = A x + B u + G w`, where `w` is a white noise process
    with covariance Q, if discretization is performed using zero-order hold (ZOH) with a
    sampling interval `dt`, then the discretised system is given by:
    ```
    x[k+1] = Ad x[k] + Bd u[k] + w[k],
    ```
    This function computes the covariance `Qd` of `w[k]` using Van Loan's formula [1].

    [1] Van Loan, Charles. Computing integrals involving the matrix exponential.
    IEEE transactions on automatic control, 23.3 (1978): 395-404.
    """
    nx = A.shape[0]
    GQGT = G @ Q @ G.T
    F = dt * jnp.block([[-A, GQGT], [jnp.zeros_like(A), A.T]])
    eF = jsp.linalg.expm(F)
    ur = eF[:nx, nx:]  # upper right part
    lr = eF[nx:, nx:]  # lower right part
    Qd = jnp.matmul(lr.T, ur)
    return 0.5 * (Qd + Qd.T)


def discretize_Q_euler(G, Q, dt):
    """
    For a linear system `dot_x = A x + B u + G w`, where `w` is a white noise process
    with covariance Q, if discretization is performed using a forwar Euler method with
    sampling interval `dt`, then the discretised system is given by:
    ```
    x[k+1] = Ad x[k] + Bd u[k] + w[k],
    ```
    This function computes the covariance `Qd` of `w[k]`.
    """
    GQGT = G @ Q @ G.T
    Qd = GQGT * dt
    return Qd


def linearize_plant(plant, x_eq, u_eq):
    """
    Linearize a plant around provided equilibrium point (x_eq, u_eq)

    Parameters:
    plant : LeafSystem or Diagram representing the plant
            The plant to be linearized.
    x_eq : jnp.ndarray
            The equilibrium point for the plant's state.
    u_eq : jnp.ndarray
            The equilibrium point for the plant's input.

    Returns:
    y_eq : jnp.ndarray
        The plant's output at equilibrium point.
    linear_plant : an `LTISystem` representing the linear plant.
    """
    with plant.input_ports[0].fixed(u_eq):
        base_context = plant.create_context()
        _, unravel = ravel_pytree(base_context.continuous_state)
        eq_context = base_context.with_continuous_state(unravel(x_eq))
        y_eq = plant.output_ports[0].eval(eq_context)
        linear_plant = linearize(plant, eq_context)
    return y_eq, linear_plant


@staticmethod
def linearize_and_discretize_continuous_plant(
    plant,
    x_eq,
    u_eq,
    dt,
    Q,
    R,
    G=None,  # if None, assume u = u+w, so G = B
    discretization_method="zoh",
    discretized_noise=False,
):
    """
    Utility to linearize and discretize a continuous plant.
    See documentation for methods calling this for more information; for example,
    `make_kalman_filter_for_continuous_plant`, and
    `make_infinite_horizon_kalman_filter_for_continuous_plant`
    """
    y_eq, linear_plant = linearize_plant(plant, x_eq, u_eq)

    A, B, C, D = linear_plant.A, linear_plant.B, linear_plant.C, linear_plant.D

    nx, nu = B.shape
    ny, _ = D.shape

    if G is None:
        G = B

    # Convert to discrete-time
    Cd, Dd = C, D

    if discretization_method == "euler":
        Ad, Bd = discretize_forward_euler(A, B, dt)
        if discretized_noise:
            Gd = G
            Rd = R
            Qd = Q
        else:
            Gd = jnp.eye(nx)
            Rd = R / dt
            Qd = discretize_Q_euler(G, Q, dt)

    elif discretization_method == "zoh":
        Ad, Bd = discretize_forward_zoh(A, B, dt)
        if discretized_noise:
            Gd = G
            Rd = R
            Qd = Q
        else:
            Gd = jnp.eye(nx)
            Rd = R / dt
            Qd = discretize_Q_zoh(G, Q, A, dt)

    else:
        raise ValueError(
            f"Discretization method {discretization_method} not "
            f" supported. Please use `euler` or `zoh`."
        )

    return (y_eq, Ad, Bd, Cd, Dd, Gd, Qd, Rd)


@staticmethod
def prepare_continuous_plant_for_nonlinear_kalman_filter(
    plant,
    dt,
    G_func,
    Q_func,
    R_func,
    x_hat_0,
    discretization_method,
    discretized_noise,
):
    nu = Q_func(0.0).shape[0]

    nx = x_hat_0.size

    ode_rhs = make_ode_rhs(plant, nu)

    def rhs(x_k, u_k):
        # forward operator of the plant doesn't take time,
        # so use a dummy value for time argument
        return ode_rhs(x_k, u_k, 0.0)

    rhs_jac_x = jax.jacfwd(rhs)

    def forward_euler(x_k, u_k, dt=dt):
        dot_x = rhs(x_k, u_k)
        x_kp1 = x_k + dot_x * dt
        return x_kp1

    def forward_zoh(x_k, u_k, dt=dt):
        dot_x = rhs(x_k, u_k)
        A = rhs_jac_x(x_k, u_k).reshape((nx, nx))
        x_kp1 = x_k + jnp.dot(
            jnp.matmul(jnp.eye(nx) - jsp.linalg.expm(-dt * A), jnp.linalg.inv(A)),
            dot_x,
        )
        return x_kp1

    # generate the unravel utility function
    with plant.input_ports[0].fixed(jnp.zeros(nu)):
        base_context = plant.create_context()
        _, unravel = ravel_pytree(base_context.continuous_state)

    def observation(x_k, u_k):
        with plant.input_ports[0].fixed(u_k):
            base_context = plant.create_context()
            context = base_context.with_continuous_state(unravel(x_k))
            y_k = plant.output_ports[0].eval(context)
        return y_k

    # TODO: `forward` method for an RK4 integrator and/or diffrax ODE solver
    # could be beneficial for unscneted Kalman Filter.

    if discretization_method == "euler":
        forward = forward_euler
        if discretized_noise:
            Gd_func = G_func
            Rd_func = R_func

            def Qd_func(t, x_k, u_k):
                return Q_func(t)

        else:

            def Gd_func(t):
                return jnp.eye(nx)

            def Rd_func(t):
                return R_func(t) / dt

            def Qd_func(t, x_k, u_k):
                G = G_func(t)
                Q = Q_func(t)
                return discretize_Q_euler(G, Q, dt)

    elif discretization_method == "zoh":
        forward = forward_zoh
        if discretized_noise:
            Gd_func = G_func
            Rd_func = R_func

            def Qd_func(t, x_k, u_k):
                return Q_func(t)

        else:

            def Gd_func(t):
                return jnp.eye(nx)

            def Rd_func(t):
                return R_func(t) / dt

            def Qd_func(t, x_k, u_k):
                G = G_func(t)
                Q = Q_func(t)
                A = rhs_jac_x(x_k, u_k).reshape((nx, nx))
                return discretize_Q_zoh(G, Q, A, dt)  # use Van Loan's approximation

    else:
        raise ValueError(
            f"Discretization method {discretization_method} is not "
            f" supported. Please use `euler` or `zoh`."
        )

    return (forward, observation, Gd_func, Qd_func, Rd_func)
