import numpy as np


def sensor_to_ground(sensor_vector, Quat, scalar_first=True):
    if scalar_first:
        # Quat[w,x,y,z] 实部在前
        w, x, y, z = np.array(Quat).squeeze()
    else:
        # Quat[x,y,z,w] 实部在后
        x, y, z, w = np.array(Quat).squeeze()

    sensor_to_ground = np.array([
        [1 - 2 * y ** 2 - 2 * z ** 2, 2 * x * y - 2 * w * z, 2 * x * z + 2 * w * y],
        [2 * x * y + 2 * w * z, 1 - 2 * x ** 2 - 2 * z ** 2, 2 * y * z - 2 * w * x],
        [2 * x * z - 2 * w * y, 2 * y * z + 2 * w * x, 1 - 2 * x ** 2 - 2 * y ** 2]
    ])

    ground_vector = np.dot(sensor_to_ground, sensor_vector)
    return ground_vector
if __name__ == "__main__":

    a= np.array([1,2,3,4]).reshape(-1,1)
    b =np.array([1,2,3]).reshape(-1,1)
    c=sensor_to_ground(b,a)
    print(c)
