#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>
#include <time.h>
#include <string.h>

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
    pthread_cond_t capacityCond;
    int maxCapacity;
    int size;
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

void initializeWaitingArea(WaitingArea* waitingArea, int maxCapacity) {
    for (int i = 0; i < 3; i++) {
        waitingArea->lines[i].size = 0;
        waitingArea->lines[i].numVehicles = 0;
        pthread_cond_init(&waitingArea->lines[i].cond, NULL);
    }
    pthread_mutex_init(&waitingArea->mutex, NULL);
    pthread_cond_init(&waitingArea->capacityCond, NULL);
    waitingArea->maxCapacity = maxCapacity;
    waitingArea->size = 0;
}

void destroyWaitingArea(WaitingArea* waitingArea) {
    for (int i = 0; i < 3; i++) {
        pthread_cond_destroy(&waitingArea->lines[i].cond);
    }
    pthread_mutex_destroy(&waitingArea->mutex);
    pthread_cond_destroy(&waitingArea->capacityCond);
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

            while (line->numVehicles == 0) {
                pthread_cond_wait(&line->cond, &waitingArea->mutex);
            }

            Vehicle vehicle = line->vehicles[line->size - line->numVehicles];

            char vehicleType[10];
            switch (vehicle.type) {
                case CAR:
                    strcpy(vehicleType, "Car");
                    break;
                case BUS:
                    strcpy(vehicleType, "Bus");
                    break;
                case TRUCK:
                    strcpy(vehicleType, "Truck");
                    break;
            }

            time_t rawtime;
            struct tm* timeinfo;
            time(&rawtime);
            timeinfo = localtime(&rawtime);

            printf("[%02d:%02d:%02d] Booth clerk at Port %c processes Vehicle %d (Type: %s)\n",
                   timeinfo->tm_hour, timeinfo->tm_min, timeinfo->tm_sec,
                   (waitingArea == &portAWaitingArea) ? 'A' : 'B',
                   vehicle.index, vehicleType);

            line->numVehicles--;

            if (line->numVehicles == 0) {
                line->size = 0;
            }

            pthread_mutex_unlock(&waitingArea->mutex);

            usleep(vehicle.waitTime * 1000);
        }
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

            while (line->numVehicles == 0) {
                pthread_cond_wait(&line->cond, &waitingArea->mutex);
            }

            Vehicle vehicle = line->vehicles[line->size - line->numVehicles];

            char vehicleType[10];
            switch (vehicle.type) {
                case CAR:
                    strcpy(vehicleType, "Car");
                    break;
                case BUS:
                    strcpy(vehicleType, "Bus");
                    break;
                case TRUCK:
                    strcpy(vehicleType, "Truck");
                    break;
            }

            time_t rawtime;
            struct tm* timeinfo;
            time(&rawtime);
            timeinfo = localtime(&rawtime);

            printf("[%02d:%02d:%02d] Ferry at Port %c carries Vehicle %d (Type: %s)\n",
                   timeinfo->tm_hour, timeinfo->tm_min, timeinfo->tm_sec,
                   (waitingArea == &portAWaitingArea) ? 'A' : 'B',
                   vehicle.index, vehicleType);

            line->numVehicles--;

            if (line->numVehicles == 0) {
                line->size = 0;
            }

            pthread_mutex_unlock(&waitingArea->mutex);

            usleep(vehicle.waitTime * 1000);
        }

        pthread_mutex_lock(&ferry->otherWaitingArea->mutex);

        int otherSize = ferry->otherWaitingArea->size;
        int otherMaxCapacity = ferry->otherWaitingArea->maxCapacity;

        while (otherSize == otherMaxCapacity) {
            pthread_cond_wait(&ferry->otherWaitingArea->capacityCond, &ferry->otherWaitingArea->mutex);
            otherSize = ferry->otherWaitingArea->size;
        }

        pthread_mutex_unlock(&ferry->otherWaitingArea->mutex);
    }

    return NULL;
}

int main() {
    srand(time(NULL));

    initializeWaitingArea(&portAWaitingArea, WAITING_AREA_CAPACITY);
    initializeWaitingArea(&portBWaitingArea, WAITING_AREA_CAPACITY);
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

        time_t rawtime;
        struct tm* timeinfo;
        time(&rawtime);
        timeinfo = localtime(&rawtime);

        printf("[%02d:%02d:%02d] Vehicle %d (Type: %s) arrives at Port %c.\n",
               timeinfo->tm_hour, timeinfo->tm_min, timeinfo->tm_sec,
               vehicle.index, (vehicle.type == CAR) ? "Car" : (vehicle.type == BUS) ? "Bus" : "Truck",
               (vehicle.startPort == PORT_A) ? 'A' : 'B');

        pthread_cond_broadcast(&line->cond);
        pthread_mutex_unlock(&waitingArea->mutex);

        usleep(vehicle.waitTime * 1000);
    }

    pthread_attr_destroy(&attr);

    destroyWaitingArea(&portAWaitingArea);
    destroyWaitingArea(&portBWaitingArea);

    return 0;
}

