#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define HEAP_SIZE 10000

// Global variables for the allocator
void* heap;
size_t heap_size;
size_t peak_memory_used;

// Initialize the allocator
void init_allocator() {
    // Allocate memory for the heap
    heap = malloc(HEAP_SIZE);
    if (heap == NULL) {
        fprintf(stderr, "Failed to allocate memory for the heap.\n");
        exit(1);
    }
    
    // Initialize heap size
    heap_size = HEAP_SIZE;
    peak_memory_used = 0;
}

// Allocate memory block of given size
void* my_malloc(size_t size) {
    // TODO: Implement memory allocation logic
    // This function should return a pointer to a memory block of at least the requested size
    // Return NULL if allocation fails
    
    void* block = malloc(size);
    if (block != NULL) {
        size_t memory_used = size + sizeof(size_t); // Include space to store block size
        peak_memory_used = (memory_used > peak_memory_used) ? memory_used : peak_memory_used;
        return block;
    }
    return NULL;
}

// Deallocate a previously allocated block
void my_free(void* ptr) {
    // TODO: Implement memory deallocation logic
    free(ptr);
}

int main() {
    // Initialize the allocator
    init_allocator();

    // Test the allocator's space utilization
    size_t allocated_memory = 0;
    size_t num_allocations = 0;
    
    // Allocate memory blocks until reaching the maximum heap size
    while (allocated_memory + sizeof(size_t) <= heap_size) {
        size_t size = rand() % 100 + 1; // Allocate random-sized blocks between 1 and 100 bytes
        void* block = my_malloc(size);
        if (block != NULL) {
            allocated_memory += size + sizeof(size_t);
            num_allocations++;
        } else {
            break; // Allocation failed, exit loop
        }
    }
    
    // Calculate space utilization ratio
    float space_utilization = (float)allocated_memory / (float)heap_size;
    
    // Print results
    printf("Space Utilization: %.2f\n", space_utilization);
    printf("Peak Memory Used: %zu\n", peak_memory_used);
    
    // Test the allocator's throughput
    clock_t start_time = clock();
    
    // Perform a large number of allocations and deallocations
    const int num_operations = 1000000;
    for (int i = 0; i < num_operations; i++) {
        size_t size = rand() % 100 + 1; // Allocate random-sized blocks between 1 and 100 bytes
        void* block = my_malloc(size);
        if (block != NULL) {
            my_free(block);
        }
    }
    
    // Calculate throughput
    clock_t end_time = clock();
    double elapsed_time = (double)(end_time - start_time) / CLOCKS_PER_SEC;
    double throughput = (double)num_operations / elapsed_time;
    
    // Print results
    printf("Throughput: %.2f operations per second\n", throughput);

    // Free the allocated memory and clean up
    free(heap);

    return 0;
}
