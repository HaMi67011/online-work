#include <iostream>
#include <vector>
#include <cmath>

struct Device {
    double x;
    double y;
    double power;
};

double calculateDistance(double x1, double y1, double x2, double y2) {
    return std::sqrt(std::pow(x2 - x1, 2) + std::pow(y2 - y1, 2));
}

void AnalyzeSmartFarm(int numDevices, const std::vector<double>& x, const std::vector<double>& y, std::vector<double>& power) {
    int numDead = 0;
    int deadDevice = -1;
    int connectedNetworks = 0;
    double threshold = 0.3 * numDevices;

    std::vector<std::vector<bool>> adjacencyMatrix(numDevices, std::vector<bool>(numDevices, false));
    for (int i = 0; i < numDevices; ++i) {
        for (int j = i + 1; j < numDevices; ++j) {
            double distance = calculateDistance(x[i], y[i], x[j], y[j]);
            if (distance <= 20) {
                adjacencyMatrix[i][j] = true;
                adjacencyMatrix[j][i] = true;
            }
        }
    }

    while (numDead < threshold) {
        for (int i = 0; i < numDevices; ++i) {
            if (power[i] < 5e-3 && i != deadDevice) {
                numDead++;
                power[i] = 0;
                if (deadDevice == -1) {
                    deadDevice = i;
                }
            }
        }

        if (numDead >= threshold) {
            break;
        }

        for (int i = 0; i < numDevices; ++i) {
            if (power[i] >= 5e-3) {
                int numNeighbors = 0;
                for (int j = 0; j < numDevices; ++j) {
                    if (adjacencyMatrix[i][j]) {
                        numNeighbors++;
                    }
                }
                power[i] -= numNeighbors * 5e-9;
            }
        }

        connectedNetworks = numDevices - numDead;
    }

    std::cout << deadDevice << std::endl;
    std::cout << connectedNetworks << std::endl;
}
