import matplotlib.pyplot as plt
import numpy as np


def intersection(line1, line2):
    """Intersection of two lines, represented as (point, direction). Returns None if the lines are perpendicular but
    different - they don't intersect, coefficient of direction of second line, if first point lies on it (lines are the
    same) and both coefficients of directions if lines are not perpendicular."""

    # in this case line1 is the point of interest with direction (0, 1) and line2 is a segment of the polygon
    point1, direction1 = line1
    point2, direction2 = line2

    det_denom = direction1[0] * direction2[1] - direction2[0] * direction1[1]

    # if lines are parallel -> shouldn't happen, since we have noise added to points
    if det_denom == 0:
        return None

    # coefficients
    s = (direction1[0] * (point1 - point2)[1] - direction1[1] * (point1 - point2)[0]) / det_denom
    r = (point2[0] + s * direction2[0] - point1[0]) / direction1[0]

    return r, s


def generify(S):
    """Adds small amount of noise to points S."""
    return np.array(S) + np.random.normal(0, 0.01, size=np.shape(np.array(S)))


def triangulate(S, vertical=True):
    """Plots line sweep triangulation of points in S. S should consist of at least of 4 points."""
    S = generify(S)
    sort_by = 1 - int(vertical)
    points = sorted(S, key=lambda x: x[sort_by])
    edges = [points[:2], points[1:3], [points[0], points[2]]]
    triangles = [points[:3]]
    for i in range(3, len(points)):
        p = points[i]
        if i == len(points)-1:
            a = 0
        connect_to = []
        for p2 in points[:i]:
            # is edge possible?
            possible = True
            for edge in edges:
                # does it intersect any other edge
                t, s = intersection((p, p2 - p), (edge[0], edge[1] - edge[0]))
                if 1e-5 < t < 1-1e-5 and 1e-5 < s < 1-1e-5:
                    possible = False
                    break
            if possible:
                connect_to.append(p2)

        # append triangles
        for j in range(len(connect_to) - 1):
            p1 = connect_to[j]
            for k in range(j+1, len(connect_to)):
                p2 = connect_to[k]
                if np.any([np.any(p2 == e) and np.any(p1 == e) for e in edges]):
                    # check if any point in connect_to lies inside triangle
                    point_inside = False
                    for c in connect_to:
                        s, t = intersection((p, p1 - p), (c, p - p2))
                        if s + t < 1 and s > 0 and t > 0:
                            point_inside = True
                            break
                    if not point_inside:
                        triangles.append([p, p1, p2])

        # append edges
        edges = edges + [[p, c] for c in connect_to]

    return edges, triangles


if __name__ == '__main__':
    for seed in [0, 1]:
        np.random.seed(seed)

        S = [np.random.uniform(0, 100, size=2) for _ in range(100)] + \
            [np.array([0, 0]), np.array([100, 0]), np.array([0, 100]), np.array([100, 100])]
        edges, triangles = triangulate(S, True)

        # plot triangulation
        plt.figure(figsize=(10, 10))
        plt.plot(*list(zip(*S)), 'o')
        for edge in edges:
            plt.plot(*list(zip(*edge)), color='black')
        for tri in triangles:
            plt.fill(*list(zip(*tri)), color=np.random.uniform(0, 1, size=3), alpha=0.5)
        plt.show()

        edges, triangles = triangulate(S, False)

        # plot triangulation
        plt.figure(figsize=(10, 10))
        plt.plot(*list(zip(*S)), 'o')
        for edge in edges:
            plt.plot(*list(zip(*edge)), color='black')
        for tri in triangles:
            plt.fill(*list(zip(*tri)), color=np.random.uniform(0, 1, size=3), alpha=0.5)
        plt.show()

