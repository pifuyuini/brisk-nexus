# Clebsch-Gordan系数计算
# 算法部分
# copyright@pifuyuini
# version: 1.0.2
# 20241128更新：决定采用sympy的Rational保持分数的形式
# 20241202更新：由gpt作调整

# 导入必要的库
from sympy import Rational, Integer, Matrix, zeros, sqrt, sign, Symbol
import random

# 功能函数
def find_last_column_sign(matrix):
    """
    给定一个 n*(n-1) 的正交矩阵，前 n-1 列已知，计算最后一列的符号，并以整数形式返回。

    参数：
    matrix: sympy Matrix，形状为 (n, n-1)，表示前 n-1 列向量。

    返回：
    最后一列的符号，长度为 n 的整数列表，每个元素为 ±1。
    """
    # 获取矩阵的形状
    n, m = matrix.shape
    if m != n - 1:
        raise ValueError("输入的矩阵必须为 n*(n-1)。")
    # 构造前 n-1 列的正交矩阵
    Q = zeros(n, n)
    Q[:, :m] = matrix
    # 生成最后一列的候选向量
    candidate = Matrix([Rational(random.random()) for _ in range(n)])
    # 对候选向量进行正交化
    for i in range(m):
        candidate -= (Q[:, i].dot(candidate)) * Q[:, i]
    # 归一化
    candidate /= candidate.norm()
    # 规定第一个元素为正
    if candidate[0] < 0:
        candidate = -candidate
    # 提取符号并转换为整型
    signs = [int(sign(c)) for c in candidate]
    return signs

# 算法主体，CG系数类
class CG:
    '''
    计算给定 j1 和 j2 的 Clebsch-Gordan 系数的类。
    '''

    # 初始化参数，依照Cohen书，我们按(j1,j2)做划分
    def __init__(self, j1, j2):
        if j2 > j1:
            self.j1 = Rational(j2)
            self.j2 = Rational(j1)
            print('Exchage j1 and j2 !')
        else:
            self.j1 = Rational(j1)
            self.j2 = Rational(j2)        
        
    # 耦合出的所有J的取值
    def j_set(self):
        j1 = self.j1
        j2 = self.j2
        j_min = abs(j1 - j2)
        j_max = j1 + j2
        num_j = Integer(j_max - j_min + 1)
        j_list = [j_max - n for n in range(num_j)]
        return j_list
        
    # 耦合出的所有的M的取值
    def m_set(self):
        j1 = self.j1
        j2 = self.j2
        m_max = j1 + j2
        m_min = -m_max
        num_m = Integer(2 * m_max + 1)
        m_list = [m_max - n for n in range(num_m)]
        return m_list
    
    # 统计CG系数不重复的M
    def number_of_half_of_m(self):
        number_of_m = len(self.m_set())
        divisibility = number_of_m // 2
        if divisibility * 2 == number_of_m:
            number = divisibility
        else:
            number = divisibility + 1
        return number
        
    # 给定某个M，它对应的所有(m1,m2)的组合
    def m1m2(self, m):
        """
        找到满足 m1 + m2 = m 的所有组合，m1 和 m2 在各自范围内取值。

        参数:
        m: 总的 M 值。

        返回:
        满足条件的 (m1, m2) 组成的列表: [(m1, m2), ...]
        """
        j1 = self.j1
        j2 = self.j2
        m1_values = [j1 - i for i in range(Integer(2 * j1 + 1))]
        m2_values = [j2 - i for i in range(Integer(2 * j2 + 1))]
        points = []
        for m1 in m1_values:
            m2 = m - m1  # 由方程 m1 + m2 = M 得出 m2
            if m2 in m2_values:
                points.append((m1, m2))
        return points
        
    # 返回CG系数表，便于主函数生成
    def cg_table(self):
        j1 = self.j1
        j2 = self.j2

        cg = []
        
        # 顶格的cg系数：|j1+j2, j1+j2> = 1 * |j1, j2; j1, j2>
        cg_of_j1j2j1j2 = 1

        j_set = self.j_set()

        for n in range(len(j_set)):
            # 先算|J, J>的系数
            if n != 0:
                j = j_set[n]  # 对于每个n都是一个固定的J

                # 先求解数值，按照约定，我们求解的是它的平方
                order = n + 1  # 矩阵的阶数，也对应着j_set中的第order个角动量
                cg_this_j = []  # 这个J对应的所有CG系数的列表
                cg_this_j_first_group = []
                for row_num in range(1, order+1):
                    x = 1
                    for col_num in range(1, order):
                        x = x - abs(cg[n - col_num][int((order - n + col_num - 1) * (n - col_num + order) / 2) + (row_num - 1)])
                    cg_this_j_first_group.append(x)
                
                # 接下来求解符号
                matrix = []
                for row_num in range(1, order+1):
                    row = []
                    for col_num in range(1, order):
                        value = sqrt(abs(cg[n - col_num][int((order - n + col_num - 1) * (n - col_num + order) / 2) + (row_num - 1)])) * sign(cg[n - col_num][int((order - n + col_num - 1) * (n - col_num + order) / 2) + (row_num - 1)])
                        row.append(value)
                    row = row[::-1]
                    matrix.append(row)
                sympy_matrix = Matrix(matrix)
                signs = find_last_column_sign(sympy_matrix)
                for num in range(len(cg_this_j_first_group)):
                    cg_this_j_first_group[num] =  cg_this_j_first_group[num] * signs[num]
                # 至此完成了整个|J,J>的系数计算，存储在cg_this_j_first_group
                
                # 接下来用递推公式计算|J,M>的系数
                cg_this_j.extend(cg_this_j_first_group)
                num_m = self.number_of_half_of_m() - n  # 该J对应的M数
                for num_lowering in range(num_m-1):
                    m = self.m_set()[n] - num_lowering - 1
                    m1m2_list = self.m1m2(m)
                    cg_this_j_last_group = cg_this_j[::-1][0:len(self.m1m2(m+1))][::-1]
                    for num_m1m2 in range(len(m1m2_list)):
                        m1 = m1m2_list[num_m1m2][0]
                        m2 = m1m2_list[num_m1m2][1]
                        if -self.m1m2(m+1)[0][1] == j2:
                            if num_m1m2 == len(m1m2_list)-1:
                                term = ((j1 * (j1 + 1) - (m1 + 1) * m1) / (j * (j + 1) - m * (m + 1))) * cg_this_j_last_group[-1]
                                cg_this_j.append(term)
                            else:
                                term_m1 = ((j1 * (j1 + 1) - (m1 + 1) * m1) / (j * (j + 1) - m * (m + 1))) * cg_this_j_last_group[num_m1m2]
                                term_m2 = ((j2 * (j2 + 1) - (m2 + 1) * m2) / (j * (j + 1) - m * (m + 1))) * cg_this_j_last_group[num_m1m2+1]
                                a = sqrt(abs(term_m1)) * sign(term_m1)
                                b = sqrt(abs(term_m2)) * sign(term_m2)
                                sign_add_ab = sign(a + b)
                                cg_this_j.append(sign_add_ab * (a + b)**2)
                        else:
                            if num_m1m2 == 0:
                                term = ((j2 * (j2 + 1) - (m2 + 1) * m2) / (j * (j + 1) - m * (m + 1))) * cg_this_j_last_group[0]
                                cg_this_j.append(term)
                            elif num_m1m2 == len(m1m2_list)-1:
                                term = ((j1 * (j1 + 1) - (m1 + 1) * m1) / (j * (j + 1) - m * (m + 1))) * cg_this_j_last_group[-1]
                                cg_this_j.append(term)
                            else:
                                term_m1 = ((j1 * (j1 + 1) - (m1 + 1) * m1) / (j * (j + 1) - m * (m + 1))) * cg_this_j_last_group[num_m1m2-1]
                                term_m2 = ((j2 * (j2 + 1) - (m2 + 1) * m2) / (j * (j + 1) - m * (m + 1))) * cg_this_j_last_group[num_m1m2]
                                a = sqrt(abs(term_m1)) * sign(term_m1)
                                b = sqrt(abs(term_m2)) * sign(term_m2)
                                sign_add_ab = sign(a + b)
                                cg_this_j.append(sign_add_ab * (a + b)**2)
                # 至此完成了所有|J,M>系数的计算，全部存储于cg_this_j当中
                cg.append(cg_this_j)

            # 单独处理第一个J对应的情况
            else:
                j = j_set[0]  # 对于每个n都是一个固定的J
                cg_this_j = []
                cg_this_j.append(cg_of_j1j2j1j2)
                num_m = self.number_of_half_of_m() # 该J对应的M数
                for num_lowering in range(num_m-1):
                    m = self.m_set()[0] - num_lowering - 1
                    m1m2_list = self.m1m2(m)
                    cg_this_j_last_group = cg_this_j[::-1][0:len(self.m1m2(m+1))][::-1]
                    for num_m1m2 in range(len(m1m2_list)):
                        m1 = m1m2_list[num_m1m2][0]
                        m2 = m1m2_list[num_m1m2][1]
                        if -self.m1m2(m+1)[0][1] == j2:
                            if num_m1m2 == len(m1m2_list)-1:
                                term = ((j1 * (j1 + 1) - (m1 + 1) * m1) / (j * (j + 1) - m * (m + 1))) * cg_this_j_last_group[-1]
                                cg_this_j.append(term)
                            else:
                                term_m1 = ((j1 * (j1 + 1) - (m1 + 1) * m1) / (j * (j + 1) - m * (m + 1))) * cg_this_j_last_group[num_m1m2]
                                term_m2 = ((j2 * (j2 + 1) - (m2 + 1) * m2) / (j * (j + 1) - m * (m + 1))) * cg_this_j_last_group[num_m1m2+1]
                                a = sqrt(abs(term_m1)) * sign(term_m1)
                                b = sqrt(abs(term_m2)) * sign(term_m2)
                                sign_add_ab = sign(a + b)
                                cg_this_j.append(sign_add_ab * (a + b)**2)
                        else:
                            if num_m1m2 == 0:
                                term = ((j2 * (j2 + 1) - (m2 + 1) * m2) / (j * (j + 1) - m * (m + 1))) * cg_this_j_last_group[0]
                                cg_this_j.append(term)
                            elif num_m1m2 == len(m1m2_list)-1:
                                term = ((j1 * (j1 + 1) - (m1 + 1) * m1) / (j * (j + 1) - m * (m + 1))) * cg_this_j_last_group[-1]
                                cg_this_j.append(term)
                            else:
                                term_m1 = ((j1 * (j1 + 1) - (m1 + 1) * m1) / (j * (j + 1) - m * (m + 1))) * cg_this_j_last_group[num_m1m2-1]
                                term_m2 = ((j2 * (j2 + 1) - (m2 + 1) * m2) / (j * (j + 1) - m * (m + 1))) * cg_this_j_last_group[num_m1m2]
                                a = sqrt(abs(term_m1)) * sign(term_m1)
                                b = sqrt(abs(term_m2)) * sign(term_m2)
                                sign_add_ab = sign(a + b)
                                cg_this_j.append(sign_add_ab * (a + b)**2)
                cg.append(cg_this_j)
        # 至此完成了包含第一项的所有|J,M>系数的计算，全部存储于表CG当中
        return cg
