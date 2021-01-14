import numpy as np
from Vec3 import Vec3


def dist(v1: Vec3, v2: Vec3) -> float:
    """
    计算向量之间的距离\n
    :param v1: 向量1
    :param v2: 向量2
    :return: 向量之间的距离
    """
    p = (v1.x, v1.y, v1.z)
    q = (v2.x, v2.y, v2.z)
    p = np.array(p)
    q = np.array(q)
    return np.linalg.norm(p - q)


def minus(v1: Vec3, v2: Vec3) -> Vec3:
    """
    返回两个向量之差\n
    :param v1: 向量1
    :param v2: 向量2
    :return: 向量差
    """
    return Vec3(v1.x - v2.x, v1.y - v2.y, v1.z - v2.z)


def add(v1: Vec3, v2: Vec3) -> Vec3:
    """
    返回两个向量之和\n
    :param v1: 向量1
    :param v2: 向量2
    :return: 向量和
    """
    return Vec3(v1.x + v2.x, v1.y + v2.y, v1.z + v2.z)


def numMul(v: Vec3, k: float) -> Vec3:
    """
    向量数乘\n
    :param v: 向量
    :param k: 标量
    :return: 数乘后得到的向量
    """
    return Vec3(v.x * k, v.y * k, v.z * k)
