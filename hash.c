// Filename: hash.c
#include <stdint.h>

// A simple "hash" function to demonstrate
uint32_t simple_hash(uint32_t input) {
    uint32_t hash = input;
    for (int i = 0; i < 100000; i++) {
        hash = (hash * 31) + i;  // Simulate heavy computation
    }
    return hash;
}
