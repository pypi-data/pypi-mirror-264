import numpy as np
from .Extend_Kalman_Filter import EKF_AHRS


class Orientation:
    def __init__(self,
                 sample_rate: float = 200,
                 frame: str = 'NED',
                 method: str = 'EKF',
                 **kwargs):
        # Sample_rate and Sample_dt
        self.sample_rate = sample_rate
        self.dt = kwargs.get('sample_dt', 1.0 / self.sample_rate)
        # Method
        self.frame = frame  # Local tangent plane coordinate frame
        self.method = method  # Sensor Fusion Algorithm

        # EKF_methods
        EKF_methods = {'EKF', 'Ekf', 'ekf'}
        if self.method in EKF_methods:
            self.ekf = EKF_AHRS(sample_rate, **kwargs)

    def EKF(self, accel: np.ndarray, gyro: np.ndarray, mag: np.ndarray = None) -> np.ndarray:
        q = self.ekf.ekf_update(accel, gyro, mag)
        return q