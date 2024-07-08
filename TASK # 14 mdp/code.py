import numpy as np

xgridsize = 50
ygridsize = 50
T = 60
D = 9
tseek = 1

Pv = np.zeros((xgridsize + 1, ygridsize + 1, T + 1, D + 1))
Pfind = np.zeros((xgridsize + 1, ygridsize + 1, T + 1))
Pdest = np.zeros((xgridsize + 1, ygridsize + 1, xgridsize + 1, ygridsize + 1))
Reward = np.zeros((xgridsize + 1, ygridsize + 1, xgridsize + 1, ygridsize + 1))
Allowance = np.zeros((xgridsize + 1, ygridsize + 1))
tdrive = np.zeros((xgridsize + 1, ygridsize + 1, xgridsize + 1, ygridsize + 1))
policy = np.zeros((xgridsize + 1, ygridsize + 1, T + 1))

# ================================================
# Functions
# ================================================

def initialize():
    global Pv, Pfind, Pdest, Reward, Allowance, tdrive, policy

    with open("p_find_01_15_2013_1200_1300_x_y_t copy.csv", "r") as fh:
        for t in range(1, T + 1):
            for y in range(1, ygridsize + 1):
                for x in range(1, xgridsize + 1):
                    xcoord1, ycoord1, ttime, prob1 = map(float, fh.readline().strip().split(","))
                    Pfind[x][y][t] = prob1

    with open("allowance_weekday_daytime_x_y.csv", "r") as fh:
        for y in range(1, ygridsize + 1):
            for x in range(1, xgridsize + 1):
                xcoord1, ycoord1, allowance = map(int, fh.readline().strip().split(","))
                Allowance[x][y] = allowance

    with open("Pdest_weekday_daytime_ij.csv", "r") as fh:
        for y2 in range(1, ygridsize + 1):
            for x2 in range(1, xgridsize + 1):
                for y1 in range(1, ygridsize + 1):
                    for x1 in range(1, xgridsize + 1):
                        xcoord1, ycoord1, xcoord2, ycoord2, prob2 = map(float, fh.readline().strip().split(","))
                        Pdest[x1][y1][x2][y2] = prob2

    with open("Tdrive_manhattan_weekday_daytime_1.csv", "r") as fh:
        for y2 in range(1, ygridsize + 1):
            for x2 in range(1, xgridsize + 1):
                for y1 in range(1, ygridsize + 1):
                    for x1 in range(1, xgridsize + 1):
                        xcoord1, ycoord1, xcoord2, ycoord2, drive = map(float, fh.readline().strip().split(","))
                        tdrive[x1][y1][x2][y2] = drive

    with open("Reward_manhattan_weekday_daytime_1.csv", "r") as fh:
        for y2 in range(1, ygridsize + 1):
            for x2 in range(1, xgridsize + 1):
                for y1 in range(1, ygridsize + 1):
                    for x1 in range(1, xgridsize + 1):
                        xcoord1, ycoord1, xcoord2, ycoord2, reward = map(float, fh.readline().strip().split(","))
                        Reward[x1][y1][x2][y2] = reward

# ================================================

def printmatrix(t, a):
    for y in range(ygridsize, 0, -1):
        for x in range(1, xgridsize + 1):
            print(Pv[x][y][t][a] * Allowance[x][y], end="\t")
        print()

# ================================================

def newx(x, y, a):
    if a in [1, 4, 7]:
        return max(1, x - 1)
    elif a in [3, 6, 9]:
        return min(xgridsize, x + 1)
    else:
        return x

# ================================================

def newy(x, y, a):
    if a in [1, 2, 3]:
        return max(1, y - 1)
    elif a in [7, 8, 9]:
        return min(ygridsize, y + 1)
    else:
        return y

# ================================================

def is_allowed(x, y, a):
    if a in [1, 2, 3, 4, 6, 7, 8, 9]:
        new_x = newx(x, y, a)
        new_y = newy(x, y, a)
        return bool(Allowance[new_x][new_y])
    return True

# ================================================

def printpolicy(t):
    for y in range(ygridsize, 0, -1):
        for x in range(1, xgridsize + 1):
            dummy = Pv[x][y][t][5]
            for a in range(1, D + 1):
                if is_allowed(x, y, a):
                    if Pv[x][y][t][a] > dummy:
                        dummy = Pv[x][y][t][a]
                        policy[x][y][t] = a
            print(int(policy[x][y][t]) * Allowance[x][y], end="\t")
        print()

# ================================================

def V(x, y, t, a):
    bestreward = 0
    nexta = 5

    dummy = Pv[newx(x, y, a)][newy(x, y, a)][min(t + tseek + tdrive[x][y][newx(x, y, a)][newy(x, y, a)], T)][5]
    for nexta in range(1, D + 1):
        if is_allowed(newx(x, y, a), newy(x, y, a), nexta):
            dummy = max(dummy, Pv[newx(x, y, a)][newy(x, y, a)][min(t + tseek + tdrive[x][y][newx(x, y, a)][newy(x, y, a)], T)][nexta])
    bestreward = (1 - Pfind[x][y][t]) * dummy

    for x2 in range(1, xgridsize + 1):
        for y2 in range(1, ygridsize + 1):
            dummy = Pv[x2][y2][min(t + tseek + tdrive[x][y][x2][y2], T)][5]
            for nexta in range(1, D + 1):
                if is_allowed(x2, y2, nexta):
                    dummy = max(dummy, Pv[x2][y2][min(t + tseek + tdrive[x][y][x2][y2], T)][nexta])
            bestreward += Pfind[x][y][t] * Pdest[x][y][x2][y2] * (Reward[x][y][x2][y2] + dummy)
    return bestreward

# ================================================

def main():
    initialize()

    for t in range(T, 0, -1):
        for x in range(1, xgridsize + 1):
            for y in range(1, ygridsize + 1):
                for a in range(1, D + 1):
                    Pv[x][y][t][a] = V(x, y, t, a)
                    print(Pv[x][y][t][a])

    for t in range(T, 0, -1):
        print(f"t = {t}, d = 5")
        printmatrix(t, 5)
        print()

        print(f"t = {t}")
        printpolicy(t)
        print()

    with open("result_PV_weekday_daytime.csv", "w") as f:
        for t in range(T, 0, -1):
            for x in range(1, xgridsize + 1):
                for y in range(1, ygridsize + 1):
                    for a in range(1, D + 1):
                        f.write(f"{x}, {y}, {t}, {a}, {Pv[x][y][t][a] * Allowance[x][y]}\n")

    with open("result_weekday_daytime.csv", "w") as f:
        for t in range(T, 0, -1):
            for x in range(1, xgridsize + 1):
                for y in range(1, ygridsize + 1):
                    f.write(f"{x}, {y}, {t}, {int(policy[x][y][t]) * Allowance[x][y]}\n")

if __name__ == "__main__":
    main()

