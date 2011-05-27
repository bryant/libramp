#define ZERO_REP 0xFFFFFFFF

typedef long long fixed_t;
typedef unsigned long long ufixed_t;

typedef struct {
    unsigned int val;
    int num;
    unsigned int rest;
} Accel;

typedef struct {
    ufixed_t freq;
    unsigned int c0;
    Accel acc_rung;
} Axis;

Accel speed_up(Accel a, unsigned int c0);
void init_axis(Axis *axis);
unsigned int next_step(Axis *axis, unsigned int target_period);
unsigned int go(Axis *axis, unsigned int target_period);
