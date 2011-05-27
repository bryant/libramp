from math import sqrt

def ramp(freq, accel, vel):
    c_n = int(freq * sqrt(float(2) / accel))
    n = 0
    rest = 0
    target_c = freq / vel
    yield c_n, rest

    while True:
        n += 1
        f, rest = divmod(2*c_n + rest, 4*n + 1)
        c_n = c_n - f
        #c_n, rest = divmod(c_n*(4*n - 1) + rest, 4*n + 1)

        if c_n > freq:
            c_n = freq
        elif c_n <= 0:
            c_n = 1

        if c_n >= target_c:
            yield c_n, rest
        else:
            yield target_c, rest
            break

    while True:
        f, rest = divmod(2*c_n + rest, 4*n - 1)
        c_n = c_n + f
        #c_n, rest = divmod(c_n*(4*n + 1) + rest, 4*n - 1)

        if n == 1:
            yield c_n, rest
            break

        n -= 1
        yield c_n, rest

class Accel(object):
    ZERO_REP = 0xFFFFFFFF

    def __init__(self, num, val, rest=0):
        self.val = val
        self.num = num
        self.rest = rest

class Axis(object):
    ZERO_REP = 0xFFFFFFFF

    def __init__(self, freq, accel):
        self.freq = float(freq)
        self.c0 = int(freq * sqrt(float(2)/accel))

        self.acc_rung = self.ZERO_REP, -1, 0

        self.period = self.ZERO_REP

    @property
    def vel(self):
        if self.period == self.ZERO_REP:
            return 0

        return self.freq / self.period

    @property
    def d(self):
        return self.__dict__

    def speed_up(self, accel):
        val, n, rest = accel
        n = n + 1

        if n < 0:
            val = self.ZERO_REP
        elif n == 0:
            val = self.c0
            rest = 0
        else:
            f, rest = divmod(2*val + rest, 4*n + 1)
            val -= f
            #val, rest = divmod(val * (4*n-1) + rest, 4*n + 1)

        return val, n, rest

    def slow_down(self, accel):
        val, n, rest = accel

        if n < 0:
            val = self.ZERO_REP
            n = n + 1
        elif n == 0:
            val = self.ZERO_REP
            rest = 0
        else:
            f, rest = divmod(2*val + rest, 4*n - 1)
            val += f
            #val, rest = divmod(val * (4*n+1) + rest, 4*n - 1)

        return val, n-1, rest

    def next_step(self, vel, debug=False):
        target_period = int(self.freq / vel) if vel > 0 else self.ZERO_REP

        accel = self.speed_up(self.acc_rung)
        decel = self.slow_down(self.acc_rung)

        #print decel, target_period, accel,

        if target_period < accel[0]:
            target_period = accel[0]
            self.acc_rung = accel
        elif target_period > self.acc_rung[0]:
            target_period = self.acc_rung[0]
            self.acc_rung = decel

        #print "=>", target_period
        if debug:
            print target_period
        self.period = target_period
        return self.period

    def go(self, vel, debug=False):
        target_period = int(self.freq / vel) if vel > 0 else self.ZERO_REP
        p = self.period
        num_steps = 0

        while p != target_period:
            num_steps += 1
            p = self.next_step(vel, debug=debug)

        return num_steps

    s = next_step

def test_ramp():
    accel = lambda c1, c2, freq: 2*freq**2*(c1-c2)/(float(c1)*c2*(c1+c2))
    lastc = None
    for i, (c, shit) in enumerate(ramp(8*10**6, 40, 200)):
        if lastc is not None:
            print i, c, accel(lastc, c, 8*10**6)
        else:
            print i, c

        lastc = c

p = Axis(80*10**6, 100)
#z = list(enumerate(ramp(8*10**6, 40, 200)))
#for i in xrange(len(z)/2+1):
#   print z[i], z[-(i+1)]
#test_ramp()

if __name__ == "__main__":
    from sys import argv

    #print "Ramping to 200:\n", p.go(200, debug=False), "steps"
    #print "Ramping to 494:\n", p.go(p.freq/162000, debug=False), "steps"

    '''p.go(400, debug=False)

    if len(argv) > 1:
        print "Wearing and tearing"
        for i in xrange(24):
            p.go(2, debug=False)
            p.go(563, debug=False)
            p.go(400, debug=False)

    print "Back to 0:\n", p.go(0), "steps"'''

    print p.go(200), "steps"
    print p.go(p.freq/162000), "steps"
    print p.go(0), "steps"
