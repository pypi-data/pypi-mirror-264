import numpy as np
def eulerangle(b, scalar_first=True,**kwargs):
    if scalar_first:
        a = 3*b
    else:
        # Quat[x,y,z,w] 实部在后
        a= 4*b
    c = kwargs.get("c",6)

    return a*c

if __name__ == "__main__":
    value = eulerangle(4,c=4)
    print(value)