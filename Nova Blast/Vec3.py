from __future__ import annotations

import numpy as np


class Vec3():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def norm(self) -> float:
        """
        返回此向量的长度\n
        :return: 向量长度
        """
        a = np.array((self.x, self.y, self.z))
        return np.linalg.norm(a)

    def unitVec(self) -> Vec3:
        """
        返回在此向量方向上的单位向量\n
        :return: 单位向量
        """
        norm = self.norm()
        if norm == 0:
            return Vec3(0, 0, 0)
        else:
            return Vec3(self.x / norm, self.y / norm, self.z / norm)

    @staticmethod
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

    @staticmethod
    def add(v1: Vec3, v2: Vec3) -> Vec3:
        """
        返回两个向量之和\n
        :param v1: 向量1
        :param v2: 向量2
        :return: 向量和
        """
        return Vec3(v1.x + v2.x, v1.y + v2.y, v1.z + v2.z)

    @staticmethod
    def minus(v1: Vec3, v2: Vec3) -> Vec3:
        """
        返回两个向量之差\n
        :param v1: 向量1
        :param v2: 向量2
        :return: 向量差
        """
        return Vec3(v1.x - v2.x, v1.y - v2.y, v1.z - v2.z)

    @staticmethod
    def numMul(v: Vec3, k: float) -> Vec3:
        """
        向量数乘\n
        :param v: 向量
        :param k: 标量
        :return: 数乘后得到的向量
        """
        return Vec3(v.x * k, v.y * k, v.z * k)

    @staticmethod
    def dist2D(v1: Vec3, v2: Vec3) -> float:
        """
        将向量投影至XOY平面后计算向量距离\n
        :param v1: 向量1
        :param v2: 向量2
        :return: 只考虑前两维的向量距离
        """
        p = Vec3(v1.x, v1.y, 0)
        q = Vec3(v2.x, v2.y, 0)
        return Vec3.dist(p, q)
