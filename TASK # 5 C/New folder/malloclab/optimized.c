#include <stdio.h>
#include <stdlib.h>

// Global variables for the allocator
char* heap;         // Pointer to the start of the heap
size_t heap_size;   // Size of the heap

// Function prototypes
void init_allocator(size_t size);
void* my_malloc(size_t size);
void my_free(void* ptr);

int main() {
    // Initialize the allocator with a heap size of 10000 bytes
    size_t heap_size = 10000;
    init_allocator(heap_size);
    
    // Test the allocator
    int* ptr1 = (int*)my_malloc(sizeof(int));
    int* ptr2 = (int*)my_malloc(2 * sizeof(int));
    
    *ptr1 = 42;
    *ptr2 = 150;  // Update ptr2 to 150
    
    printf("Value at ptr1: %d\n", *ptr1);
    printf("Value at ptr2: %d\n", *ptr2);
    
    my_free(ptr1);
    my_free(ptr2);
    
    return 0;
}

// Initialize the allocator with a given heap size
void init_allocator(size_t size) {
    // Allocate memory for the heap
    heap = (char*)malloc(size);
    if (heap == NULL) {
        fprintf(stderr, "Failed to allocate memory for the heap.\n");
        exit(1);
    }
    
    // Initialize the first boundary tag to represent the entire heap
    size_t* boundary_tag = (size_t*)heap;
    *boundary_tag = size - sizeof(size_t);
    
    // Set the heap size
    heap_size = size;
}

// Allocate memory block of given size
void* my_malloc(size_t size) {
    // Adjust the requested size for alignment requirements
    size_t adjusted_size = size;
    if (size % sizeof(size_t) != 0) {
        adjusted_size += sizeof(size_t) - (size % sizeof(size_t));
    }
    
    // Find the first free block that can accommodate the adjusted size
    char* current_block = heap;
    while (current_block < heap + heap_size) {
        size_t* boundary_tag = (size_t*)current_block;
        size_t block_size = *boundary_tag;
        
        if (block_size >= adjusted_size && block_size > 0) {
            // Found a suitable free block
            
            // Check if the remaining size is large enough to split the block
            if (block_size >= adjusted_size + sizeof(size_t) + sizeof(size_t)) {
                // Split the block into an allocated block and a free block
                size_t* allocated_block_tag = boundary_tag;
                size_t* free_block_tag = (size_t*)(current_block + adjusted_size);
                
                *allocated_block_tag = adjusted_size;
                *free_block_tag = block_size - adjusted_size - sizeof(size_t);
                
                // Initialize the allocated memory with 100
                int* allocated_block = (int*)(allocated_block_tag + 1);
                *allocated_block = 100;
                
                return (void*)(allocated_block_tag + 1);
            } else {
                // Use the entire block since the remaining size is not sufficient for splitting
                *boundary_tag = block_size | 0x1; // Mark block as allocated
                
                // Initialize the allocated memory with 100
                int* allocated_block = (int*)(boundary_tag + 1);
                *allocated_block = 100;
                
                return (void*)(boundary_tag + 1);
            }
        }
        
        current_block += block_size;
    }
    
    // No suitable block found, return NULL
    return NULL;
}

// Deallocate a previously allocated block
void my_free(void* ptr) {
    if (ptr == NULL) {
        return;  // Do nothing if the pointer is NULL
    }
    
    // Calculate the boundary tag address from the pointer
    size_t* boundary_tag = (size_t*)ptr - 1;
    
    // Mark the block as free
    *boundary_tag = *boundary_tag & ~0x1;
    
    // Coalesce free blocks
    char* current_block = (char*)boundary_tag;
    while (current_block < heap + heap_size) {
        size_t* current_boundary_tag = (size_t*)current_block;
        size_t current_block_size = *current_boundary_tag;
        
        if (current_block_size & 0x1) {
            // Block is allocated, move to the next block
            current_block += current_block_size;
        } else {
            // Block is free, merge with the next block if it exists and is also free
            char* next_block = current_block + current_block_size;
            if (next_block < heap + heap_size) {
                size_t* next_boundary_tag = (size_t*)next_block;
                if (!(*next_boundary_tag & 0x1)) {
                    // Merge with the next block
                    size_t merged_block_size = current_block_size + *next_boundary_tag + sizeof(size_t);
                    *current_boundary_tag = merged_block_size;
                }
            }
            
            // Merge with the previous block if it exists and is also free
            if (current_block > heap) {
                size_t* previous_boundary_tag = (size_t*)(current_block - sizeof(size_t));
                if (!(*previous_boundary_tag & 0x1)) {
                    // Merge with the previous block
                    size_t* previous_previous_boundary_tag = (size_t*)(current_block - *previous_boundary_tag - 2 * sizeof(size_t));
                    *previous_previous_boundary_tag += current_block_size + sizeof(size_t);
                }
            }
            
            break;
        }
    }
}
