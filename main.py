import numpy as np
import time
from result import *


def set_dis(C, ob):
    """
    :param C: Cell number
    :param ob: Obstacle list
    :return: An array. The value of each cell means the closest distance to the obstacle
    """
    dis = np.ones((1, C), dtype=float)
    dis[0, ob] = 0
    its = [(ob[i]+ob[i+1])/2 for i in range(len(ob)-1)]  # intersection
    its.append(C)
    a = 0
    for i in range(0, C):
        if dis[0, i] == 0:  # obstacle
            continue
        if i > its[a]:
            a += 1
        dis[0, i] = abs(i - ob[a])
    return dis
    pass


def esdf(M, N, obstacle_list):
    """
    :param M: Row number
    :param N: Column number
    :param obstacle_list: Obstacle list
    :return: An array. The value of each cell means the closest distance to the obstacle
    """
    map_1 = np.ones((M, 1), dtype=float)
    for c in range(0, N):
        # find obstacles on current column
        ob_c = [i[0] for i in obstacle_list if i[1] == c]
        if not ob_c:  # no obstacle on current column
            dis_c = np.full((1, M), 2*M)
        else:
            dis_c = set_dis(M, ob_c)  # calculate vertical distance
        map_1 = np.append(map_1, dis_c.T, axis=1)
    map_1 = map_1[:, 1:]**2  # vertical distance ^2

    map_2 = map_1.copy()
    for r in range(0, M):
        l = 0  # left parabola in count
        # use 2*N instead of inf
        low_env = np.array([-(2*N)**2, (2*N)**2], dtype=float)
        for i in range(1, N):
            # intersection
            ist = ((i**2 + map_1[r, i]) - (l**2 + map_1[r, l]))/(2*(i-l))
            # intersect on left to previous intersection, then previous intersection is invalid
            if ist <= low_env[l]:
                l -= 1
                i -= 1
            else:                  # intersect on right to previous intersection, then both two intersection are valid
                l += 1
                low_env[l] = ist
                low_env = np.append(low_env, (2*N)**2)
        low_env = np. floor(low_env)
        l = 0
        for i in range(0, N):      # calculate finaldistances
            while low_env[l+1] < i:
                l += 1
            map_2[r, i] = (l-i)**2 + map_1[r, l] # horizontal distance ^2 + vertical distance ^2
    return(np.sqrt(map_2))
    pass


if __name__ == '__main__':
    st = time.time()
    for _ in range(int(2e4)):
        assert np.array_equal(esdf(M=3, N=3, obstacle_list=[[0, 1], [2, 2]]), res_1)
        assert np.array_equal(esdf(M=4, N=5, obstacle_list=[[0, 1], [2, 2], [3, 1]]), res_2)

    et = time.time()
    print(et-st)
