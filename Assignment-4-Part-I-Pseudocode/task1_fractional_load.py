# Task 1 - Repaired design: FractionalVehicleLoad (greedy by value/weight ratio)

def fractional_vehicle_load(packages, capacity):
    fraction = {pid: 0 for pid, w, v in packages}
    order = sorted(packages, key=lambda p: p[2] / p[1], reverse=True)   # greedy order
    remaining, total = capacity, 0
    print("Order by value/weight:", [(pid, round(v / w, 2)) for pid, w, v in order])
    for pid, w, v in order:
        if remaining <= 0:
            break
        if w <= remaining:                       # whole package fits
            fraction[pid] = 1
            remaining -= w
            total += v
            print("  %s: whole package, remaining = %g, value = %g" % (pid, remaining, total))
        else:                                    # only a part fits
            f = remaining / w
            fraction[pid] = f
            total += f * v
            remaining = 0
            print("  %s: fraction %.3f, remaining = 0, value = %g" % (pid, f, total))
    return fraction, total


packages = [("P1", 10, 60), ("P2", 20, 100), ("P3", 30, 120)]   # (id, weight, value)
fr, value = fractional_vehicle_load(packages, 50)
print("Fractions loaded:", fr)
print("Total value:", value)
print("Empty vehicle :", fractional_vehicle_load(packages, 0)[1])
print("All fit       :", fractional_vehicle_load(packages, 100)[1])
