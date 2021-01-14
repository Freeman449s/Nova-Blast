from __future__ import annotations

from Vec3 import Vec3
import Global


class Particle():
    Q = 0.005  # 静电斥力常量
    K = 2e-6  # 劲度系数
    RELAXATION_LENGTH = 100  # 松弛长度

    def __init__(self, r: float, x: float, y: float, z: float, vx: float, vy: float, vz: float, darkTextureID: int):
        self.r = r
        self.position = Vec3(x, y, z)
        self.velocity = Vec3(vx, vy, vz)
        self.force = Vec3(0, 0, 0)
        self.darkTextureID = darkTextureID

    def updateMovement(self) -> None:
        """
        更新运动状态，基于Verlet积分法\n
        :return: 无返回值
        """
        if Global.forceSim != Global.ForceType.NONE:  # 启动力学模拟
            intermediateV = Vec3.add(self.velocity, Vec3.numMul(self.force, 0.5))  # 中间速度，Verlet积分法的v(t+1/2h)
            if Global.bSpeedUp:
                self.position = Vec3.add(self.position, Vec3.numMul(intermediateV, Global.speedUpRatio_particle))
            else:
                self.position = Vec3.add(self.position, intermediateV)
            self.position = Vec3.add(self.position, intermediateV)
            oldForce = self.force
            self.force = Vec3(0, 0, 0)
            for p in Global.particles:
                if p != self:
                    repulsiveForce = self.computeForce(p)
                    self.force = Vec3.add(self.force, repulsiveForce)
            self.velocity = Vec3.add(self.velocity, Vec3.numMul(Vec3.add(oldForce, self.force), 0.5))
        else:  # 不启用力学模拟
            if Global.bSpeedUp:
                self.position = Vec3.add(self.position, Vec3.numMul(self.velocity, Global.speedUpRatio_particle))
            else:
                self.position = Vec3.add(self.position, self.velocity)

    def computeForce(self, other: Particle) -> Vec3:
        """
        计算相互作用力\n
        :param other: 对方粒子
        :return: 力向量
        """
        dist2D = Vec3.dist2D(self.position, other.position)
        diffVec = Vec3.minus(self.position, other.position)  # 坐标差（向量）
        diffVec.z = 0  # 只在二维上分离粒子
        if Global.forceSim == Global.ForceType.ELECTROSTATIC_REPULSION:
            force_scalar = 1000 * Particle.Q
            if dist2D != 0:
                force_scalar = Particle.Q / dist2D
            force = Vec3.numMul(diffVec.unitVec(), force_scalar)
        else:
            force = Vec3.numMul(diffVec.unitVec(),
                                (diffVec.norm() - Particle.RELAXATION_LENGTH) * Particle.K * -1)
        return force
