import numpy as np
import matplotlib.pyplot as plt


def intersection(line1, line2):
    """Intersection of two lines, represented as (point, direction). Returns None if the lines are perpendicular but
    different - they don't intersect, coefficient of direction of second line, if first point lies on it (lines are the
    same) and both coefficients of directions if lines are not perpendicular."""

    # in this case line1 is the point of interest with direction (0, 1) and line2 is a segment of the polygon
    point1, direction1 = line1
    point2, direction2 = line2

    det_denom = direction1[0] * direction2[1] - direction2[0] * direction1[1]

    # if lines are parallel
    if det_denom == 0:
        # avoid division by 0
        if direction2[0] == 0:
            if point1[0] != point2[0]:
                # parallel lines, no intersection
                return None
            else:
                return [(point1[1] - point2[1]) / direction2[1]]

        if direction2[1] == 0:
            if point1[1] != point2[1]:
                # parallel lines, no intersection
                return None
            else:
                return [(point1[0] - point2[0]) / direction2[0]]

        s1 = (point1[0] - point2[0]) / direction2[0]
        s2 = (point1[1] - point2[1]) / direction2[1]

        if s1 == s2:        # lines are the same
            return [s1]

        else:
            # parallel lines, no intersection
            return None

    # coefficients
    s = (direction1[0] * (point1 - point2)[1] - direction1[1] * (point1 - point2)[0]) / det_denom
    r = (point2[0] + s * direction2[0] - point1[0]) / direction1[0]

    return r, s


def insideQ(P, T):
    """Returns whether point T lies inside curve given by points P."""
    points = [np.array(p) for p in P]
    directions = [np.array(P[i + 1]) - np.array(P[i]) for i in range(len(P) - 1)] + [np.array(P[0]) - np.array(P[-1])]
    polygon_lines = list(zip(points, directions))
    t_line = (np.array(T), np.array((1, 0)))
    nr_intersections = 0

    for i, line in enumerate(polygon_lines):
        intrsc = intersection(t_line, line)

        if intrsc is None:
            continue        # there is no intersection

        elif len(intrsc) == 1:
            # intersection of parallel lines
            if 0 <= intrsc[0] <= 1:
                # point on the edge means it's inside
                return True
            else:
                continue
        else:
            t, p = intrsc

        if t < 0:
            continue        # we will only check the rays in positive direction

        if t == 0:          # point on the edge is inside
            return True

        if p <= 0 or p > 1:
            continue        # the intersection is not on the edge (t == 0 means previous t was 1 -> already included)

        if p == 1:
            # the intersection is on polygon vertex, we need to check angles to see if the point is inside
            angle1 = np.angle(complex(*line[1]), deg=True)
            next_line = polygon_lines[(i+1) % len(polygon_lines)]
            angle2 = np.angle(complex(*next_line[1]), deg=True)

            # if second line is parallel to (1, 0) we don't know if we're inside or outside
            counter = 2
            while angle2 == 0 or angle2 == 180:
                next_line = polygon_lines[(i + counter) % len(polygon_lines)]
                angle2 = np.angle(complex(*next_line[1]), deg=True)
                counter += 1

            if angle1 * angle2 > 0:
                # point is inside
                nr_intersections += 1

        else:
            nr_intersections += 1

    if nr_intersections % 2 == 0:
        # even number of intersections => point is outside the polygon
        return False
    else:
        # odd number of intersections => point is inside the polygon
        return True


if __name__ == '__main__':
    T1 = (2.33, 0.66)
    P1 = [(0.02, 0.10), (0.98, 0.05), (2.10, 1.03), (3.11, -1.23), (4.34, -0.35),
         (4.56, 2.21), (2.95, 3.12), (2.90, 0.03), (1.89, 2.22)]

    print(insideQ(P1, T1))

    plt.plot([p[0] for p in P1] + [P1[0][0]], [p[1] for p in P1] + [P1[0][1]], 'o-')
    plt.scatter(*T1, color='r')
    plt.savefig('figures/jordan1')
    plt.show()

    P2 = [(0, 0), (10, 0), (10, 8), (12, 9), (13, 3), (15, 0), (16, 5), (15, 10), (10, 10), (0, 10)]

    T2 = (5, 5)
    print(insideQ(P2, T2))

    T3 = (12, 0)
    print(insideQ(P2, T3))

    plt.plot([p[0] for p in P2] + [P2[0][0]], [p[1] for p in P2] + [P2[0][1]], 'o-')
    plt.scatter(*T2, color='r')
    plt.scatter(*T3, color='r')
    plt.savefig('figures/jordan2')

