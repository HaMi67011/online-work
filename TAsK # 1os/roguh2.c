#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>
#include <time.h>
#include <string.h> // Add the string.h header for strcpy function

#define NUM_VEHICLES 10
#define WAITING_AREA_CAPACITY 10
#define NUM_BOOTH_CLERKS 4
#define NUM_FERRIES 2

typedef enum {
    CAR,
    BUS,
    TRUCK
} VehicleType;

typedef enum {
    PORT_A,
    PORT_B
} Port;

typedef struct {
    int index;
    VehicleType type;
    Port startPort;
    int waitTime;
    int size;
} Vehicle;

typedef struct {
    Vehicle vehicles[WAITING_AREA_CAPACITY];
    int size;
    int numVehicles;
    pthread_cond_t cond;
} WaitingLine;

typedef struct {
    WaitingLine lines[3];
    pthread_mutex_t mutex;
} WaitingArea;

typedef struct {
    pthread_t thread;
    WaitingArea* waitingArea;
} BoothClerk;

typedef struct {
    pthread_t thread;
    WaitingArea* waitingArea;
    WaitingArea* otherWaitingArea;
} Ferry;

WaitingArea portAWaitingArea;
WaitingArea portBWaitingArea;
BoothClerk portABoothClerks[NUM_BOOTH_CLERKS];
BoothClerk portBBoothClerks[NUM_BOOTH_CLERKS];
Ferry ferries[NUM_FERRIES];

void initializeWaitingArea(WaitingArea* waitingArea) {
    for (int i = 0; i < 3; i++) {
        waitingArea->lines[i].size = 0;
        waitingArea->lines[i].numVehicles = 0;
        pthread_cond_init(&waitingArea->lines[i].cond, NULL);
    }
    pthread_mutex_init(&waitingArea->mutex, NULL);
}

void destroyWaitingArea(WaitingArea* waitingArea) {
    for (int i = 0; i < 3; i++) {
        pthread_cond_destroy(&waitingArea->lines[i].cond);
    }
    pthread_mutex_destroy(&waitingArea->mutex);
}

void initializeBoothClerks(BoothClerk* boothClerks, int numClerks) {
    for (int i = 0; i < numClerks; i++) {
        boothClerks[i].waitingArea = (i % 2 == 0) ? &portAWaitingArea : &portBWaitingArea;
    }
}

void initializeFerries(Ferry* ferries, int numFerries) {
    for (int i = 0; i < numFerries; i++) {
        ferries[i].waitingArea = (i % 2 == 0) ? &portAWaitingArea : &portBWaitingArea;
        ferries[i].otherWaitingArea = (i % 2 == 0) ? &portBWaitingArea : &portAWaitingArea;
    }
}

void* boothClerkThread(void* arg) {
    BoothClerk* clerk = (BoothClerk*)arg;
    WaitingArea* waitingArea = clerk->waitingArea;

    while (1) {
        pthread_mutex_lock(&waitingArea->mutex);

        for (int i = 0; i < 3; i++) {
            WaitingLine* line = &waitingArea->lines[i];

            if (line->numVehicles > 0) {
                Vehicle vehicle = line->vehicles[line->size - line->numVehicles];

                char vehicleType[10]; // Declare vehicleType variable

                switch (vehicle.type) {
                    case CAR:
                        strcpy(vehicleType, "Car"); // Use strcpy to assign the vehicle type
                        break;
                    case BUS:
                        strcpy(vehicleType, "Bus"); // Use strcpy to assign the vehicle type
                        break;
                    case TRUCK:
                        strcpy(vehicleType, "Truck"); // Use strcpy to assign the vehicle type
                        break;
                }

                printf("Booth clerk at Port %c processes Vehicle %d (Type: %s)\n",
                       (waitingArea == &portAWaitingArea) ? 'A' : 'B',
                       vehicle.index, vehicleType);

                line->numVehicles--;

                if (line->numVehicles == 0) {
                    line->size = 0;
                }

                pthread_mutex_unlock(&waitingArea->mutex);

                usleep(vehicle.waitTime * 1000);

                break;
            }
        }

        pthread_mutex_unlock(&waitingArea->mutex);
    }

    return NULL;
}

void* ferryThread(void* arg) {
    Ferry* ferry = (Ferry*)arg;
    WaitingArea* waitingArea = ferry->waitingArea;

    while (1) {
        pthread_mutex_lock(&waitingArea->mutex);

        for (int i = 0; i < 3; i++) {
            WaitingLine* line = &waitingArea->lines[i];

            if (line->numVehicles > 0) {
                Vehicle vehicle = line->vehicles[line->size - line->numVehicles];

                char vehicleType[10]; // Declare vehicleType variable

                switch (vehicle.type) {
                    case CAR:
                        strcpy(vehicleType, "Car"); // Use strcpy to assign the vehicle type
                        break;
                    case BUS:
                        strcpy(vehicleType, "Bus"); // Use strcpy to assign the vehicle type
                        break;
                    case TRUCK:
                        strcpy(vehicleType, "Truck"); // Use strcpy to assign the vehicle type
                        break;
                }

                printf("Ferry at Port %c carries Vehicle %d (Type: %s)\n",
                       (waitingArea == &portAWaitingArea) ? 'A' : 'B',
                       vehicle.index, vehicleType);

                line->numVehicles--;

                if (line->numVehicles == 0) {
                    line->size = 0;
                }

                pthread_mutex_unlock(&waitingArea->mutex);

                usleep(vehicle.waitTime * 1000);

                break;
            }
        }

        pthread_mutex_unlock(&waitingArea->mutex);

        pthread_mutex_lock(&ferry->otherWaitingArea->mutex);

        if (ferry->otherWaitingArea->lines[0].numVehicles > 0 ||
            ferry->otherWaitingArea->lines[1].numVehicles > 0 ||
            ferry->otherWaitingArea->lines[2].numVehicles > 0) {

            pthread_mutex_unlock(&ferry->otherWaitingArea->mutex);
        } else {
            pthread_mutex_unlock(&ferry->otherWaitingArea->mutex);
            usleep(1000);
        }
    }

    return NULL;
}

int main() {
    srand(time(NULL));

    initializeWaitingArea(&portAWaitingArea);
    initializeWaitingArea(&portBWaitingArea);
    initializeBoothClerks(portABoothClerks, NUM_BOOTH_CLERKS);
    initializeBoothClerks(portBBoothClerks, NUM_BOOTH_CLERKS);
    initializeFerries(ferries, NUM_FERRIES);

    pthread_attr_t attr;
    pthread_attr_init(&attr);
    pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_DETACHED);

    for (int i = 0; i < NUM_BOOTH_CLERKS; i++) {
        pthread_create(&portABoothClerks[i].thread, &attr, boothClerkThread, &portABoothClerks[i]);
        pthread_create(&portBBoothClerks[i].thread, &attr, boothClerkThread, &portBBoothClerks[i]);
    }

    for (int i = 0; i < NUM_FERRIES; i++) {
        pthread_create(&ferries[i].thread, &attr, ferryThread, &ferries[i]);
    }

    for (int i = 0; i < NUM_VEHICLES; i++) {
        Vehicle vehicle;
        vehicle.index = i;
        vehicle.type = rand() % 3;
        vehicle.startPort = rand() % 2;
        vehicle.waitTime = rand() % 2000 + 1000;
        vehicle.size = 1;

        WaitingArea* waitingArea = (vehicle.startPort == PORT_A) ? &portAWaitingArea : &portBWaitingArea;

        pthread_mutex_lock(&waitingArea->mutex);

        WaitingLine* line = &waitingArea->lines[vehicle.type];
        line->vehicles[line->size] = vehicle;
        line->size++;
        line->numVehicles++;

        printf("Vehicle %d (Type: %s) arrives at Port %c.\n",
               vehicle.index, (vehicle.type == CAR) ? "Car" : (vehicle.type == BUS) ? "Bus" : "Truck",
               (vehicle.startPort == PORT_A) ? 'A' : 'B');

        pthread_mutex_unlock(&waitingArea->mutex);

        usleep(vehicle.waitTime * 1000);
    }

    pthread_attr_destroy(&attr);

    destroyWaitingArea(&portAWaitingArea);
    destroyWaitingArea(&portBWaitingArea);

    return 0;
}

