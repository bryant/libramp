#include <stdio.h>
#include "ramp.h"

/*unsigned int isqrt(unsigned int input)
{
    unsigned int base;
    unsigned int nextapprox, result = 0;

    for (base=1<<31; base>0; base>>=1)
    {
        nextapprox = result | base;
        if ((ufix_t)(nextapprox * nextapprox) <= (ufix_t)input)
        {
            result = nextapprox;
        }
    }

    return result;
}*/

Accel speed_up(Accel a, unsigned int c0) {
    a.num++;

    if (a.num < 0) {
        a.val = ZERO_REP;
    }
    else if (a.num == 0) {
        a.val = c0;
        a.rest = 0;
    }
    else {
#if defined(EXACT_RAMPING)
        ufixed_t numer = (ufixed_t)a.val * (4*(ufixed_t)a.num-1) + a.rest,
                 denom = 4*(ufixed_t)a.num + 1;
        a.val = numer / denom;
        a.rest = numer % denom;
#else
        unsigned int numer = 2*a.val + a.rest,
                     denom = 4*a.num + 1;
        a.val -= numer / denom;
        a.rest = numer % denom;
#endif
    }

    return a;
}

Accel slow_down(Accel a) {
    if (a.num <= 0) {
        a.val = ZERO_REP;
        a.rest = 0;
        if (a.val < 0) {
            a.num = a.num + 1;
        }
    }
    else {
#if defined(EXACT_RAMPING)
        ufixed_t numer = a.val * (4*a.num+1) + a.rest,
                 denom = 4*a.num - 1;
        a.val = numer / denom;
        a.rest = numer % denom;
#else
        unsigned int numer = 2*a.val + a.rest,
                     denom = 4*a.num - 1;
        a.val += numer / denom;
        a.rest = numer % denom;
#endif
    }

    a.num--;
    return a;
}

void init_axis(Axis *axis) {
    axis->acc_rung.val = ZERO_REP;
    axis->acc_rung.num = -1;
    axis->acc_rung.rest = 0;
}

unsigned int next_step(Axis *axis, unsigned int target_period) {
    Accel *cur = &(axis->acc_rung),
          faster = speed_up(*cur, axis->c0),
          slower = slow_down(*cur);

    if (target_period < faster.val) {
        target_period = cur->val = faster.val;
        cur->num = faster.num;
        cur->rest = faster.rest;
    }
    /* take note of the fact that the below comparison is made
       against the current accel val, instead of "slower."
       contemplate on this. */
    else if (target_period > cur->val) {
        target_period = cur->val;
        cur->val = slower.val;
        cur->num = slower.num;
        cur->rest = slower.rest;
    }

    return target_period;
}

#if defined(TESTING)
unsigned int go(Axis *axis, unsigned int target_period) {
    static unsigned int p = ZERO_REP;
    unsigned int num_steps = 0;

    while (p != target_period) {
        num_steps++;
        p = next_step(axis, target_period);
        printf("%d\n", p);
    }

    return num_steps;
}
#endif
