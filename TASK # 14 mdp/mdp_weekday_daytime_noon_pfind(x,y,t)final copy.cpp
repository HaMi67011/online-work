#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <iostream> 
#include <fstream>
using namespace std;
#define min(a,b) (((a) < (b)) ? (a) : (b))
#define max(a,b) (((a) > (b)) ? (a) : (b))

const int xgridsize = 50;
const int ygridsize = 50;
const int T = 60;
const int D = 9;
const int tseek = 1;

double Pv[xgridsize + 1][ygridsize + 1][T + 1][D + 1];
double Pfind[xgridsize + 1][ygridsize + 1][T + 1];
double Pdest[xgridsize + 1][ygridsize + 1][xgridsize + 1][ygridsize + 1];
double Reward[xgridsize + 1][ygridsize + 1][xgridsize + 1][ygridsize + 1];
int Allowance[xgridsize + 1][ygridsize + 1];
int tdrive[xgridsize + 1][ygridsize + 1][xgridsize + 1][ygridsize + 1];
int policy[xgridsize + 1][ygridsize + 1][T + 1];

// ================================================
FILE* fh;
void initialize(void) {



    int xcoord1, ycoord1, xcoord2, ycoord2, allowance, ttime;
    double prob1 = 0;
    double prob2 = 0.0;
    double reward = 0.0;
    double drive = 0.0;
    double value = 0.0;

    for (int x = 1; x <= xgridsize; x++) {
        for (int y = 1; y <= ygridsize; y++) {
            for (int t = 1; t <= T; t++) {
                for (int a = 1; a <= D; a++) {
                    Pv[x][y][t][a] = 0.0;
                    policy[x][y][t] = 5;
                }
            }
        }
    }


    fh = fopen( "p_find_01_15_2013_1200_1300_x_y_t copy.csv", "r");
    if (fh == NULL) {
        perror("Error opening file");
    }

    for (int t = 1; t <= T; t++) {
        for (int y = 1; y <= ygridsize; y++) {
            for (int x = 1; x <= xgridsize; x++) {
                fscanf(fh, "%d, %d, %d, %lf", &xcoord1, &ycoord1, &ttime, &prob1);
                Pfind[x][y][t] = prob1;
            }
        }
    }

    fh = fopen("allowance_weekday_daytime_x_y.csv", "r");
    if (fh == NULL) {
        perror("Error opening file");
    }
    for (int y = 1; y <= ygridsize; y++) {
        for (int x = 1; x <= xgridsize; x++) {
            fscanf(fh, "%d, %d, %d", &xcoord1, &ycoord1, &allowance);
            Allowance[x][y] = allowance;

        }
    }
    fclose(fh);

    fh = fopen("Pdest_weekday_daytime_ij.csv", "r");
    if (fh == NULL) {
        perror("Error opening file");
    }
    for (int y2 = 1; y2 <= ygridsize; y2++) {
        for (int x2 = 1; x2 <= xgridsize; x2++) {
            for (int y1 = 1; y1 <= ygridsize; y1++) {
                for (int x1 = 1; x1 <= xgridsize; x1++) {
                    fscanf(fh, "%d, %d, %d, %d, %lf", &xcoord1, &ycoord1, &xcoord2, &ycoord2, &prob2);
                    Pdest[x1][y1][x2][y2] = prob2;
    
                }
            }
        }
    }
    fclose(fh);

    fh = fopen("Tdrive_manhattan_weekday_daytime_1.csv", "r");
    if (fh == NULL) {
        perror("Error opening file");
    }
    for (int y2 = 1; y2 <= ygridsize; y2++) {
        for (int x2 = 1; x2 <= xgridsize; x2++) {
            for (int y1 = 1; y1 <= ygridsize; y1++) {
                for (int x1 = 1; x1 <= xgridsize; x1++) {
                    fscanf(fh, "%d, %d, %d, %d, %lf", &xcoord1, &ycoord1, &xcoord2, &ycoord2, &drive);
                    tdrive[x1][y1][x2][y2] = drive;
          
                }
            }
        }
    }
    fclose(fh);

    fh = fopen("Reward_manhattan_weekday_daytime_1.csv", "r");
    if (fh == NULL) {
        perror("Error opening file");
    }
    for (int y2 = 1; y2 <= ygridsize; y2++) {
        for (int x2 = 1; x2 <= xgridsize; x2++) {
            for (int y1 = 1; y1 <= ygridsize; y1++) {
                for (int x1 = 1; x1 <= xgridsize; x1++) {
                    fscanf(fh, "%d, %d, %d, %d, %lf", &xcoord1, &ycoord1, &xcoord2, &ycoord2, &reward);
                    Reward[x1][y1][x2][y2] = reward;
           
                }
            }
        }
    }
    fclose(fh);
}

// ================================================

void printmatrix(int t, int a) {
    for (int y = ygridsize; y >= 1; y--) {
        for (int x = 1; x <= xgridsize; x++) {
            printf("%f\t", Pv[x][y][t][a] * Allowance[x][y]);
        }
        printf("\n");
    }
}

// ================================================

int newx(int x, int y, int a) {
    int newx;

    switch (a) {
    case 1: newx = (x == 1 || y == 1 ? x : x - 1); break; // Bottom left corner
    case 3: newx = (x == xgridsize || y == 1 ? x : x + 1); break; // Bottom right corner
    case 4: newx = (x == 1 ? x : x - 1); break; // Left
    case 6: newx = (x == xgridsize ? x : x + 1); break; //Right
    case 7: newx = (x == 1 || y == ygridsize ? x : x - 1); break; // Top left corner
    case 9: newx = (x == xgridsize || y == ygridsize ? x : x + 1); break; // Top right corner
    default: newx = x;
    }
    return newx;
}

// ================================================

int newy(int x, int y, int a) {
    int newy;

    switch (a) {
    case 1: newy = (x == 1 || y == 1 ? y : y - 1); break; // Bottom left corner
    case 2: newy = (y == 1 ? y : y - 1); break; // Downward
    case 3: newy = (x == xgridsize || y == 1 ? y : y - 1); break; // Bottom right corner
    case 7: newy = (x == 1 || y == ygridsize ? y : y + 1); break; // Top left corner
    case 8: newy = (y == ygridsize ? y : y + 1); break; // Top
    case 9: newy = (x == xgridsize || y == ygridsize ? y : y + 1); break; // Top right corner
    default: newy = y;
    }
    return newy;
}

// ================================================

bool is_allowed(int x, int y, int a) {
    bool valid;

    switch (a) {
    case 1: valid = (x == 1 || y == 1 ? false : true); break; // Bottom left corner
    case 2: valid = (y == 1 ? false : true); break; // Downward
    case 3: valid = (x == xgridsize || y == 1 ? false : true); break; // Bottom right corner
    case 4: valid = (x == 1 ? false : true); break; // Left
    case 6: valid = (x == xgridsize ? false : true); break; // Right
    case 7: valid = (x == 1 || y == ygridsize ? false : true); break; // Top left corner
    case 8: valid = (y == ygridsize ? false : true); break; // Top
    case 9: valid = (x == xgridsize || y == ygridsize ? false : true); break; // Top right corner
    default: valid = true;
    }

    if (valid == true) {
        int new_x = newx(x, y, a);
        int new_y = newy(x, y, a);
        valid = Allowance[new_x][new_y];
    }
    return valid;
}

// ================================================

void printpolicy(int t)
{
    double dummy = 0.0;

    for (int y = ygridsize; y >= 1; y--) {
        for (int x = 1; x <= xgridsize; x++) {
            dummy = Pv[x][y][t][5];
            for (int a = 1; a <= D; a++) {
                if (is_allowed(x, y, a)) {
                    if (Pv[x][y][t][a] > dummy) {
                        dummy = Pv[x][y][t][a];
                        policy[x][y][t] = a;
                    }
                }
            }
            printf("%d\t", policy[x][y][t] * Allowance[x][y]);
        }
        printf("\n");
    }
}

// ================================================

double V(int x, int y, int t, int a) {
    double bestreward = 0;
    double dummy = 0.0;
    int nexta = 5;

    dummy = Pv[newx(x, y, a)][newy(x, y, a)][min(t + tseek + tdrive[x][y][newx(x, y, a)][newy(x, y, a)], T)][5];
    for (nexta = 1; nexta <= D; nexta++) {
        if (is_allowed(newx(x, y, a), newy(x, y, a), nexta)) {
            dummy = max(dummy, Pv[newx(x, y, a)][newy(x, y, a)][min(t + tseek + tdrive[x][y][newx(x, y, a)][newy(x, y, a)], T)][nexta]);
        }
    }
    bestreward = (1 - Pfind[x][y][t]) * dummy;

    for (int x2 = 1; x2 <= xgridsize; x2++) {
        for (int y2 = 1; y2 <= ygridsize; y2++) {
            dummy = Pv[x2][y2][min(t + tseek + tdrive[x][y][x2][y2], T)][5];
            for (nexta = 1; nexta <= D; nexta++) {
                if (is_allowed(x2, y2, nexta)) {
                    dummy = max(dummy, Pv[x2][y2][min(t + tseek + tdrive[x][y][x2][y2], T)][nexta]);
                }
            }
            bestreward += Pfind[x][y][t] * Pdest[x][y][x2][y2] * (Reward[x][y][x2][y2] + dummy);
        }
    }
    return bestreward;
}

// ================================================

int main(void) {
    int x, y, t, a;

    initialize();
   
    for (t = T; t >= 1; t--) {
        for (x = 1; x <= xgridsize; x++) {
            for (y = 1; y <= ygridsize; y++) {
                for (a = 1; a <= D; a++) {
                    Pv[x][y][t][a] = V(x, y, t, a);
                    cout << Pv[x][y][t][a] << endl;
                }
            }
        }
    }

    for (t = T; t >= 1; t--) {
        printf("t = %d, d = 5\n", t);
        printmatrix(t, 5);
        printf("\n");

        printf("t = %d\n", t);
        printpolicy(t);
        printf("\n");
    }

    freopen("result_PV_weekday_daytime.csv", "w", stdout);
    for (t = T; t >= 1; t--) {
        for (x = 1; x <= xgridsize; x++) {
            for (y = 1; y <= ygridsize; y++) {
                for (a = 1; a <= D; a++) {
                    std::cout << x << ", " << y << ", " << t << ", " << a << ", " << Pv[x][y][t][a] * Allowance[x][y] << "\n";
                }
            }
        }
    }
  
    freopen("result_weekday_daytime.csv", "w", stdout);
    for (t = T; t >= 1; t--) {
        for (x = 1; x <= xgridsize; x++) {
            for (y = 1; y <= ygridsize; y++) {
                std::cout << x << ", " << y << ", " << t << ", " << policy[x][y][t] * Allowance[x][y] << "\n";
            }
        }
    }

    return 0;
}