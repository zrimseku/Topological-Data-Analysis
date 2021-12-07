import matplotlib.pyplot as plt
import numpy as np
from itertools import compress
from line_sweep import triangulate


def optimize(triangles):
    """Uses edge-flipping to return Delauney triangulation from any initial triangulation."""
    triangles = [[np.array(p1), np.array(p2), np.array(p3)] for p1, p2, p3 in triangles]
    edges = []
    for t in triangles:
        for p1, p2 in [t[:2], t[1:], (t[0], t[2])]:
            if not np.any([np.any(p2 == e) and np.any(p1 == e) for e in edges]):
                edges.append([p1, p2])

    no_possible_flips = False
    while not no_possible_flips:
        no_possible_flips = True
        for e in edges:
            in_triangles = [np.any(e[0] == t) and np.any(e[1] == t) for t in triangles]
            if sum(in_triangles) == 2:
                t1, t2 = list(compress(triangles, in_triangles))
                # points of the common edge
                x, y = e
                # other two points
                w = list(compress(t1, [np.all(x != p) and np.all(y != p) for p in t1]))[0]
                z = list(compress(t2, [np.all(x != p) and np.all(y != p) for p in t2]))[0]

                # first let's check that the edge flip is possible -> angles at x and y are smaller than 180
                anglex = np.rad2deg(np.arctan2(np.cross(w - x, z - x), np.dot(w - x, z - x)))
                angley = np.rad2deg(np.arctan2(np.cross(z - y, w - y), np.dot(z - y, w - y)))
                if angley * anglex < 0:
                    # if both angles are over 180 we were checking their outside angles, so it's ok
                    continue

                # if the flip is possible, we check if we should do it
                anglew = abs(np.rad2deg(np.arctan2(np.cross(x - w, y - w), np.dot(x - w, y - w))))
                anglez = abs(np.rad2deg(np.arctan2(np.cross(x - z, y - z), np.dot(x - z, y - z))))
                if abs(anglew) + abs(anglez) > 180:
                    no_possible_flips = False
                    # do the flip
                    other_triangles = [not i for i in in_triangles]
                    new_triangles = [[x, z, w], [w, y, z]]
                    triangles = list(compress(triangles, other_triangles)) + new_triangles
                    edges = list(compress(edges, [np.all(x != e) or np.all(y != e) for e in edges])) + [[w, z]]

    return triangles


if __name__ == '__main__':
    for vertical in [True, False]:
        np.random.seed(2)

        S = [np.random.uniform(0, 100, size=2) for _ in range(100)]
        edges, triangles = triangulate(S, vertical)

        # plot original triangulation
        plt.figure(figsize=(10, 10))
        plt.plot(*list(zip(*S)), 'o')
        for edge in edges:
            plt.plot(*list(zip(*edge)), color='black')
        for tri in triangles:
            plt.fill(*list(zip(*tri)), color=np.random.uniform(0, 1, size=3), alpha=0.5)
        plt.show()

        delauney_triangles = optimize(triangles)
        print(delauney_triangles)

        delauney_edges = []
        for t in delauney_triangles:
            for p1, p2 in [t[:2], t[1:], (t[0], t[2])]:
                if not np.any([np.any(p2 == e) and np.any(p1 == e) for e in delauney_edges]):
                    delauney_edges.append([p1, p2])

        # plot delauney triangulation
        plt.figure(figsize=(10, 10))
        plt.plot(*list(zip(*S)), 'o')
        for edge in delauney_edges:
            plt.plot(*list(zip(*edge)), color='black')
        for tri in delauney_triangles:
            plt.fill(*list(zip(*tri)), color=np.random.uniform(0, 1, size=3), alpha=0.5)
        plt.show()

