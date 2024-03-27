import numpy as np
from src.math.Quaternion import Quaternion
from typing import Tuple

"""
Extended Kalman Filter
======================
In this module, we will use the Extended Kalman Filter to compute the attitude in quaternion form from data 
from a nine-axis inertial sensor that integrates a gyroscope, accelerometer, and magnetometer.

"""


class EKF_AHRS:
    """
        Extended Kalman Filter to estimate orientation as Quaternion.

        Examples
        ======================

    """

    def __init__(self,
                 sample_rate: float = 200.0,
                 frame: str = 'NED',
                 **kwargs):
        # 地面坐标系的定义：x轴指向北，y轴指向西，z轴指向天；
        self.sample_rate = sample_rate
        self.frame = frame  # Local tangent plane coordinate frame
        self.dt = kwargs.get('sample_dt', 1.0 / self.sample_rate)

        # Initial values of state variables
        self.x_k_minus_1 = np.array(kwargs.get('q0', [1, 0, 0, 0])).reshape(-1, 1)
        self.P_k_minus_1 = np.identity(kwargs.get('P', 0.01 * np.identity(4)))  # Initial state covariance
        # Prior Estimate 先验估计
        self.P_k_prior = np.identity(4)
        self.x_k_prior = np.array([1, 0, 0, 0])
        # Posterior Estimate 后验估计
        self.x_k_posterior = np.array([1, 0, 0, 0])
        self.P_k_posterior = np.identity(4)

        # Process Noise Covariance Matrix 过程噪声协方差矩阵
        self.Q_noise = kwargs.get('Q_noise', 0.1 * np.eye(4))

        # Observation Noise Covariance Matrix 观测噪声协方差矩阵
        self.accel_noise = kwargs.get('accel_noise', 3.8 * np.eye(3))
        self.mag_noise = kwargs.get('mag_noise', 0.5 * np.eye(3))

        if frame.upper() == 'NED':
            self.a_ref = np.array([0.0, 0.0, -1.0])
        elif frame.upper() == 'ENU':
            self.a_ref = np.array([0.0, 0.0, 1.0])
        else:
            raise ValueError(f"Invalid frame '{frame}'. Try 'NED' or 'ENU'")

    def Omega(self, gyro: np.ndarray) -> np.ndarray:
        """
        This operator is constantly used at different steps of the EKF.

        Q = [cos(θ/2),n*sin(θ/2)]
        So the differential equation for Q with respect to time t is as follows:
        dQ = 1/2 * Omega * Q[qw,qx,qy,qz]

        Parameters
        ----------
        gyro : numpy.ndarray
            Three-dimensional vector.

        Returns
        -------
        Omega : numpy.ndarray
            Omega matrix.

        """
        wx, wy, wz = gyro
        Omega = np.array([
            [0, -wx, -wy, -wz],
            [wx, 0, wz, -wy],
            [wy, -wz, 0, wx],
            [wz, wy, -wx, 0]
        ])

        return Omega

    def A_k(self, gyro: np.ndarray) -> np.ndarray:
        """
        Jacobian of linearized predicted state.
        .. math::
            \\mathbf{F} = \\frac{\\partial\\mathbf{f}(\\mathbf{q}_{t-1})}{\\partial\\mathbf{q}} =
            \\begin{bmatrix}
            1 & - \\frac{\\Delta t}{2} \\omega_x & - \\frac{\\Delta t}{2} \\omega_y & - \\frac{\\Delta t}{2} \\omega_z\\\\
            \\frac{\\Delta t}{2} \\omega_x & 1 & \\frac{\\Delta t}{2} \\omega_z & - \\frac{\\Delta t}{2} \\omega_y\\\\
            \\frac{\\Delta t}{2} \\omega_y & - \\frac{\\Delta t}{2} \\omega_z & 1 & \\frac{\\Delta t}{2} \\omega_x\\\\
            \\frac{\\Delta t}{2} \\omega_z & \\frac{\\Delta t}{2} \\omega_y & - \\frac{\\Delta t}{2} \\omega_x & 1
            \\end{bmatrix}

        Parameters
        ----------
        omega : numpy.ndarray
            Angular velocity in rad/s.

        Returns
        -------
        F : numpy.ndarray
            Jacobian of state.
        """
        Omega_t = self.Omega(gyro)
        A_k = np.identity(4) + 0.5 * self.dt * Omega_t
        return A_k

    def State_Transition_Model(self, q: np.ndarray, gyro: np.ndarray) -> np.ndarray:
        """
        Linearized function of Process Model (Prediction.)

        .. math::
            \\mathbf{f}(\\mathbf{q}_{t-1}) = \\Big(\\mathbf{I}_4 + \\frac{\\Delta t}{2}\\boldsymbol\\Omega_t\\Big)\\mathbf{q}_{t-1} =
            \\begin{bmatrix}
            q_w - \\frac{\\Delta t}{2} \\omega_x q_x - \\frac{\\Delta t}{2} \\omega_y q_y - \\frac{\\Delta t}{2} \\omega_z q_z\\\\
            q_x + \\frac{\\Delta t}{2} \\omega_x q_w - \\frac{\\Delta t}{2} \\omega_y q_z + \\frac{\\Delta t}{2} \\omega_z q_y\\\\
            q_y + \\frac{\\Delta t}{2} \\omega_x q_z + \\frac{\\Delta t}{2} \\omega_y q_w - \\frac{\\Delta t}{2} \\omega_z q_x\\\\
            q_z - \\frac{\\Delta t}{2} \\omega_x q_y + \\frac{\\Delta t}{2} \\omega_y q_x + \\frac{\\Delta t}{2} \\omega_z q_w
            \\end{bmatrix}
        [q_w * \\omega_x - q_x * omega_x - q_y * omega_y - q_z * omega_z,
        q_x * omega_x + q_w * omega_y + q_z * omega_y - q_y * omega_z,
        q_y * omega_x - q_z * omega_x + q_w * omega_y + q_x * omega_z,
        q_z * omega_x + q_y * omega_y - q_x * omega_z + q_w * omega_z]

        Parameters
        ----------
        q : numpy.ndarray
            A-priori quaternion.
        gyro : numpy.ndarray
            Angular velocity, in rad/s.

        Returns
        -------
        q : numpy.ndarray
            Linearized estimated quaternion in **Prediction** step.
        """
        Omega_t = self.Omega(gyro)
        update_result = (np.identity(4) + 0.5 * self.dt * Omega_t) @ q
        return update_result

    # 对于实时处理；之后增加离线处理；
    def ekf_update(self, accel: np.ndarray, gyro: np.ndarray, mag: np.ndarray = None) -> np.ndarray:
        """
        Estimate the quaternions given sensor data.

        Attributes ``gyr``, ``acc`` MUST contain data. Attribute ``mag`` is optional.

        Parameters
        ----------
        accel : numpy.ndarray
            Sample of tri-axial Accelerometer in m/s^2.

        gyro : numpy.ndarray
            Sample of tri-axial Gyroscope in rad/s.

        mag : numpy.ndarray
            Sample of tri-axial Magnetometer in uT.

        Returns
        -------
        Q : numpy.ndarray
            M-by-4 Array with all estimated quaternions, where M is the number
            of samples.

        """

        # Measureing Data
        gyro = np.array(gyro, dtype=np.float64)
        accel = np.array(accel, dtype=np.float64).reshape(-1, 1)
        accel = accel / np.linalg.norm(accel)

        # ----- Prediction -----
        self.x_k_prior = self.State_Transition_Model(self.x_k_minus_1, gyro)
        self.x_k_prior = Quaternion.normalize(self.x_k_prior)
        A_k = self.A_k(gyro)
        self.P_k_prior = A_k @ self.P_k_minus_1 @ A_k.T + self.Q_noise
        # ----- Correction -----
        h1 = Quaternion.sensor_to_ground(self.a_ref, self.x_k_prior)
        H1 = self.Jacobian_H1(self.x_k_prior)
        Kk1 = self.P_k_prior @ H1.T @ np.linalg.inv(H1 @ self.P_k_prior @ H1.T + self.accel_noise)
        state1 = Kk1 @ (accel - h1)
        if mag is None:
            self.x_k_posterior = self.x_k_prior + state1
            self.P_k_posterior = (np.identity(4) - Kk1 @ H1) @ self.P_k_prior
        else:
            state1[3][0] = 0  # 不影响偏航角 将q3置为0 No effect on yaw angle. Set q3 to zero.
            self.x_k_posterior = self.x_k_prior + state1
            self.P_k_posterior = (np.identity(4) - Kk1 @ H1) @ self.P_k_prior
            mag = np.array(mag, dtype=np.float64).reshape(-1, 1)
            mag = accel / np.linalg.norm(mag)
            h2, H2 = self.Jacobian_H2(mag, self.x_k_prior)
            Kk2 = self.P_k_prior @ H2.T @ np.linalg.inv(H2 @ self.P_k_prior @ H2.T + self.mag_noise)
            state2 = Kk2 @ (mag - h2)
            state2[1][0] = 0  # No effect on roll. Set q1 to zero.
            state2[2][0] = 0  # No effect on pitch. Set q2 to zero.
            self.x_k_posterior = self.x_k_posterior + state2
            self.P_k_posterior = (np.identity(4) - Kk2 @ H2) @ self.P_k_posterior
            self.x_k_posterior = Quaternion.normalize(self.x_k_posterior)
        # ----- update params -----

        self.x_k_minus_1 = self.x_k_posterior
        self.P_k_minus_1 = self.P_k_posterior

        return self.x_k_posterior

    def Jacobian_H1(self, q: np.ndarray) -> np.ndarray:
        q0, q1, q2, q3 = q.squeeze()
        H1 = np.array([
            [-2 * q2, 2 * q3, -2 * q0, 2 * q1],
            [2 * q1, 2 * q0, 2 * q3, 2 * q2],
            [2 * q0, -2 * q1, -2 * q2, 2 * q3],
        ])

        return H1

    def Jacobian_H2(self, mag: np.ndarray, q: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        h_ground = Quaternion.sensor_to_ground(mag, q)
        b_ground = np.array([
            [np.sqrt(h_ground[0][0] ** 2 + h_ground[1][0] ** 2)],
            [0],
            [h_ground[2][0]],
        ])
        bx, by, bz = b_ground.squeeze()
        h2 = Quaternion.ground_to_sensor(b_ground, q)
        q0, q1, q2, q3 = q.squeeze()
        H2 = np.array([
            [2 * q0 * bx - 2 * q2 * bz, 2 * q1 * bx + 2 * q3 * bz, -2 * q2 * bx - 2 * q0 * bz,
             -2 * q3 * bx + 2 * q1 * bz],
            [-2 * q3 * bx + 2 * q1 * bz, 2 * q2 * bx + 2 * q0 * bz, 2 * q1 * bx + 2 * q3 * bz,
             -2 * q0 * bx + 2 * q2 * bz],
            [2 * q2 * bx + 2 * q0 * bz, 2 * q3 * bx - 2 * q1 * bz, 2 * q0 * bx - 2 * q2 * bz,
             2 * q1 * bx + 2 * q3 * bz]
        ])
        return h2, H2
