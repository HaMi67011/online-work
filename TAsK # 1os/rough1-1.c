#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>

#define MAX_WAITING_AREA_CAPACITY 100
#define MAX_FERRY_CAPACITY 60
#define NUM_VEHICLES 20
#define NUM_BOOTH_CLERKS 4
#define NUM_WAITING_LINES 4
#define NUM_FERRIES 3

typedef enum {
    CAR,
    MOTORCYCLE,
    BUS,
    TRUCK
} VehicleType;

typedef enum {
    LINE_1,
    LINE_2,
    LINE_3,
    LINE_4
} WaitingLine;

typedef struct {
    int id;
    VehicleType type;
    WaitingLine line;
} Vehicle;

typedef struct {
    int id;
    VehicleType type;
} BoothClerk;

sem_t ferrySemaphore;
pthread_mutex_t waitingAreaMutex;
pthread_mutex_t boothMutex[NUM_BOOTH_CLERKS];
pthread_mutex_t ferryMutex[NUM_FERRIES];
int waitingArea[NUM_WAITING_LINES] = {0};

void* vehicleThread(void* arg) {
    Vehicle* vehicle = (Vehicle*)arg;
    sleep(rand() % 5); // Random delay before approaching toll booth

    // Choose a random toll booth
    int boothId = rand() % NUM_BOOTH_CLERKS;

    // Acquire the booth mutex
    if (pthread_mutex_lock(&boothMutex[boothId]) != 0) {
        fprintf(stderr, "Error: Failed to acquire booth mutex.\n");
        return NULL;
    }

    // Collect payment and enter the waiting area
    printf("Vehicle %d (Type: %d) approaches Booth%d\n", vehicle->id, vehicle->type, boothId + 1);

    // Release the booth mutex
    pthread_mutex_unlock(&boothMutex[boothId]);

    // Check if the waiting area is full
    if (pthread_mutex_lock(&waitingAreaMutex) != 0) {
        fprintf(stderr, "Error: Failed to acquire waiting area mutex.\n");
        return NULL;
    }

    if (waitingArea[vehicle->line] == MAX_WAITING_AREA_CAPACITY) {
        printf("Waiting area is full. Vehicle %d (Type: %d) is waiting at Booth%d\n", vehicle->id, vehicle->type, boothId + 1);
        pthread_mutex_unlock(&waitingAreaMutex);
        return NULL;
    }

    // Enter the waiting area
    waitingArea[vehicle->line]++;
    pthread_mutex_unlock(&waitingAreaMutex);

    printf("Vehicle %d (Type: %d) enters Line%d\n", vehicle->id, vehicle->type, vehicle->line + 1);

    // Wait until the vehicle gets loaded onto a ferry
    // ...

    printf("Vehicle %d (Type: %d) has been loaded onto a ferry\n", vehicle->id, vehicle->type);

    return NULL;
}

void* ferryThread(void* arg) {
    int ferryId = *((int*)arg);
    free(arg);

    // Wait until the ferry is full or the waiting area is full for the first trip
    // ...

    printf("Ferry %d is ready to load vehicles\n", ferryId);

    // Load vehicles from the waiting area onto the ferry
    // ...

    printf("Ferry %d has loaded all vehicles and is moving to the other port\n", ferryId);

    // Simulate travel time
    sleep(ferryId == 0 ? 6 : 4); // Adjust travel time based on the direction

    printf("Ferry %d has reached the other port and is unloading vehicles\n", ferryId);

    // Unload vehicles from the ferry
    // ...

    // Signal the completion, allowing the ferry to start moving again
    // ...

    return NULL;
}

void* boothClerkThread(void* arg) {
    BoothClerk* clerk = (BoothClerk*)arg;

    while (1) {
        // Process one customer at a time
        // ...

        // Wait for a random period of time before processing the next customer
        sleep(rand() % 3);
    }

    return NULL;
}

int main() {
    srand(time(NULL));

    if (sem_init(&ferrySemaphore, 0, 0) != 0) {
        fprintf(stderr, "Error: Failed to initialize semaphore.\n");
        return 1;
    }
    if (pthread_mutex_init(&waitingAreaMutex, NULL) != 0) {
        fprintf(stderr, "Error: Failed to initialize waiting area mutex.\n");
        return 1;
    }
    for (int i = 0; i < NUM_BOOTH_CLERKS; i++) {
        if (pthread_mutex_init(&boothMutex[i], NULL) != 0) {
            fprintf(stderr, "Error: Failed to initialize booth mutex %d.\n", i);
            return 1;
        }
    }
    for (int i = 0; i < NUM_FERRIES; i++) {
        if (pthread_mutex_init(&ferryMutex[i], NULL) != 0) {
            fprintf(stderr, "Error: Failed to initialize ferry mutex %d.\n", i);
            return 1;
        }
    }

    pthread_t vehicles[NUM_VEHICLES];
    pthread_t ferries[NUM_FERRIES];
    pthread_t boothClerks[NUM_BOOTH_CLERKS];

    // Create vehicle threads
    for (int i = 0; i < NUM_VEHICLES; i++) {
        Vehicle* vehicle = malloc(sizeof(Vehicle));
        vehicle->id = i + 1;
        vehicle->type = rand() % 4;
        vehicle->line = rand() % NUM_WAITING_LINES;
        if (pthread_create(&vehicles[i], NULL, vehicleThread, (void*)vehicle) != 0) {
            fprintf(stderr, "Error: Failed to create vehicle thread %d.\n", i);
            return 1;
        }
    }

    // Create ferry threads
    for (int i = 0; i < NUM_FERRIES; i++) {
        int* ferryId = malloc(sizeof(int));
        *ferryId = i + 1;
        if (pthread_create(&ferries[i], NULL, ferryThread, (void*)ferryId) != 0) {
            fprintf(stderr, "Error: Failed to create ferry thread %d.\n", i);
            return 1;
        }
    }

    // Create booth clerk threads
    for (int i = 0; i < NUM_BOOTH_CLERKS; i++) {
        BoothClerk* clerk = malloc(sizeof(BoothClerk));
        clerk->id = i + 1;
        clerk->type = rand() % 4;
        if (pthread_create(&boothClerks[i], NULL, boothClerkThread, (void*)clerk) != 0) {
            fprintf(stderr, "Error: Failed to create booth clerk thread %d.\n", i);
            return 1;
        }
    }

    // Join vehicle threads
    for (int i = 0; i < NUM_VEHICLES; i++) {
        if (pthread_join(vehicles[i], NULL) != 0) {
            fprintf(stderr, "Error: Failed to join vehicle thread %d.\n", i);
            return 1;
        }
    }

    // Join ferry threads
    for (int i = 0; i < NUM_FERRIES; i++) {
        if (pthread_join(ferries[i], NULL) != 0) {
            fprintf(stderr, "Error: Failed to join ferry thread %d.\n", i);
            return 1;
        }
    }

    // Join booth clerk threads
    for (int i = 0; i < NUM_BOOTH_CLERKS; i++) {
        if (pthread_join(boothClerks[i], NULL) != 0) {
            fprintf(stderr, "Error: Failed to join booth clerk thread %d.\n", i);
            return 1;
        }
    }

    sem_destroy(&ferrySemaphore);
    pthread_mutex_destroy(&waitingAreaMutex);
    for (int i = 0; i < NUM_BOOTH_CLERKS; i++) {
        pthread_mutex_destroy(&boothMutex[i]);
    }
    for (int i = 0; i < NUM_FERRIES; i++) {
        pthread_mutex_destroy(&ferryMutex[i]);
    }

    return 0;
}

