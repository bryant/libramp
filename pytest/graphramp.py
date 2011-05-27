from rampsim import Axis

p = Axis(80 * 10**6, 833)
seq = []
v = 833
cum = c_n = 0

while p.vel < v:
    cum += c_n / 2.0
    c_n = p.next_step(v)
    cum += c_n / 2.0
    x, y, m = cum / p.freq, p.freq / c_n, 5

    if len(seq) > 0:
        m = (seq[-1][1]-y) / (seq[-1][0]-x)

    seq.append((x, y, m))

with open("fuck", "w") as f:
    for i in seq:
        f.write(", ".join([str(z) for z in i]) + "\n")
