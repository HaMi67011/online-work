#include <assert.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdint.h>
#include <stdbool.h>

#include "mm.h"
#include "memlib.h"

/* Constants and macros */
#define ALIGNMENT 16
#define SIZE_T_SIZE (sizeof(size_t))

/* Basic constants for the segregated free list */
#define NUM_FREE_LISTS 10

/* Macros for manipulating the header and footer of a block */
#define PACK(size, alloc) ((size) | (alloc))
#define GET(p) (*(size_t *)(p))
#define PUT(p, val) (*(size_t *)(p) = (val))
#define GET_SIZE(p) (GET(p) & ~0xF)
#define GET_ALLOC(p) (GET(p) & 0x1)

/* Given a block pointer, compute the address of its header and footer */
#define HDRP(bp) ((char *)(bp) - SIZE_T_SIZE)
#define FTRP(bp) ((char *)(bp) + GET_SIZE(HDRP(bp)) - 2 * SIZE_T_SIZE)

/* Given a block pointer, compute the address of the next and previous blocks */
#define NEXT_BLKP(bp) ((char *)(bp) + GET_SIZE((char *)(bp) - SIZE_T_SIZE))
#define PREV_BLKP(bp) ((char *)(bp) - GET_SIZE((char *)(bp) - 2 * SIZE_T_SIZE))

/* Global variables */
static char heap_start = NULL;
static char free_lists[NUM_FREE_LISTS];

/*
 * mm_init: initializes the heap
 * Returns true on success, false on failure
 */
bool mm_init(void) {
    /* Create the initial empty heap */
    if ((heap_start = mem_sbrk(4 * SIZE_T_SIZE)) == (void *)-1) {
        return false;
    }

    /* Initialize the prologue and epilogue headers */
    PUT(heap_start, 0);                             /* Alignment padding */
    PUT(heap_start + (1 * SIZE_T_SIZE), PACK(2 * SIZE_T_SIZE, 1));  /* Prologue header */
    PUT(heap_start + (2 * SIZE_T_SIZE), PACK(2 * SIZE_T_SIZE, 1));  /* Prologue footer */
    PUT(heap_start + (3 * SIZE_T_SIZE), PACK(0, 1));               /* Epilogue header */

    /* Initialize the segregated free lists */
    for (int i = 0; i < NUM_FREE_LISTS; i++) {
        free_lists[i] = NULL;
    }

    /* Extend the empty heap with a free block of CHUNKSIZE bytes */
    while (extend_heap(4) == NULL) {
        if (heap_start == NULL) {
            return false;
        }
    }

    return true;
}

/*
 * malloc: allocates a block of memory and returns a pointer to it
 * Returns a pointer to the allocated block on success, NULL on failure
 */
void *malloc(size_t size) {
    size_t asize;         /* Adjusted block size */
    size_t extendsize;    /* Amount to extend heap if no fit */
    char *bp;

    /* Ignore spurious requests */
    if (size == 0) {
        return NULL;
    }

    /* Adjust block size to include overhead and alignment requirements */
    if (size <= ALIGNMENT) {
        asize = 2 * SIZE_T_SIZE;
    } else {
        asize = ALIGNMENT * ((size + SIZE_T_SIZE + (ALIGNMENT - 1)) / ALIGNMENT);
    }

    /* Search the free list for a fit */
    if ((bp = find_fit(asize)) != NULL) {
        place(bp, asize);
        return bp;
    }

    /* No fit found. Get more memory and place the block */
    extendsize = (asize > 4)} else if (extendsize <= 4 * SIZE_T_SIZE) {
        extendsize = 4 * SIZE_T_SIZE;
    }

    /* Extend the heap */
    if ((bp = mem_sbrk(extendsize)) == (void *)-1) {
        return NULL;
    }

    /* Initialize the new block */
    PUT(bp, PACK(extendsize, 0));
    PUT(bp + (extendsize - 1), PACK(extendsize, 0));

    /* Find the first fit in the new block */
    if ((bp = find_fit(asize, bp)) != NULL) {
        place(bp, asize);
        return bp;
    } else {
        return NULL;
    }
}

/*
 * free: frees a previously allocated block
 */
void free(void *ptr) {
    if (ptr == NULL) {
        return;
    }

    /* Get the block size and address */
    size_t size = GET_SIZE(HDRP(ptr));
    char *bp = ptr;

    /* Mark the block as free */
    PUT(HDRP(bp), PACK(size, 0));
    PUT(FTRP(bp), PACK(size, 0));

    /* Coalesce with adjacent free blocks */
    coalesce(bp);
}

/*
 * realloc: changes the size of the block pointed to by 'ptr' to 'size' bytes
 */
void *realloc(void *ptr, size_t size) {
    void *newptr;
    size_t copySize;

    /* If ptr is NULL, equivalent to malloc(size) */
    if (ptr == NULL) {
        return malloc(size);
    }

    /* If size is 0, equivalent to free(ptr) and return NULL */
    if (size == 0) {
        free(ptr);
        return NULL;
    }

    /* Get the old block size */
    size_t oldsize = GET_SIZE(HDRP(ptr));

    /* If the new size is smaller than or equal to the old size, shrink the block */
    if (size <= oldsize) {
        newptr = malloc(size);
        if (newptr == NULL) {
            return NULL;
        }
        memcpy(newptr, ptr, size);
        free(ptr);
    } else {
        /* If the new size is larger than the old size, extend the block */
        newptr = ptr;
        if (extend_heap(size - oldsize) == NULL) {
            return NULL;
        }
    }

    /* Return the new pointer */
    return newptr;
}

/*
 * calloc: allocates memory for an array of nmemb elements of size bytes each
 */
void *calloc(size_t nmemb, size_t size) {
    void *ptr;
    size *= nmemb;
    ptr = malloc(size);
    if (ptr) {
        memset(ptr, 0, size);
    }
    return ptr;
}

/* is this  code completely correct
 * Returns whether the pointer is in the heap.
 * May be useful for debugging.
 */
static bool in_heap(const void *p) {
    return p <= mem_heap_hi() && p >= mem_heap_lo();
}

/*
 * Returns whether the pointer is aligned.
 * May be useful for debugging.
 */
static bool aligned(const void *p) {
    size_t ip = (size_t)p;
    return align(ip) == ip;
}

/*
 * mm_checkheap: checks the heap for consistency
 * You can call the function via mm_checkheap(LINE) to print the line number
 * of the calling function where there was an invalid heap.
 */
bool mm_checkheap(int line_number) {
    check_heap(line_number);
    return true;
}