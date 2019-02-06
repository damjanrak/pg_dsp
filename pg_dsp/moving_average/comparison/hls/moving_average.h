#ifndef __MOVING_AVERAGE_H__
#define __MOVING_AVERAGE_H__

#include "ap_int.h"
#include <cmath>
#include <hls_stream.h>
using namespace std;

// Compare TB vs HW C-model and/or RTL
#define HW_COSIM

#define W_DATA 16
#define MAX_SIZE 1024

// #define FLOAT

#ifdef FLOAT
typedef float data_t;
#else
typedef ap_fixed<W_DATA, 1> data_t;
#endif

typedef struct {
  data_t average_coef;
  ap_uint<16> average_window;
} cfg_t;

typedef struct {
  data_t data;
  ap_uint<1> eot;
} din_t;

#endif
