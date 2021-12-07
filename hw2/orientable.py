
def add_oriented_edges(oriented_triangle):
    """Returns induced oriented edges from oriented triangle"""
    return [list(oriented_triangle[:2][::-1]), list(oriented_triangle[1:][::-1]),
            [oriented_triangle[0], oriented_triangle[2]]]


def orientableQ(T):
    """Returns if the triangulation is orientable"""
    oriented = orientable(T)
    if oriented is None:
        return False
    else:
        return True


def orientable(T):
    """Returns orientated triangulation if possible, else returns None."""
    is_oriented = {t: False for t in T}
    oriented = [T[0]]
    is_oriented[T[0]] = True
    edges_oriented = add_oriented_edges(T[0])

    while sum(is_oriented.values()) != len(T):
        if len(edges_oriented) == 0:
            print('no more induced edges')
            for t in T[1:]:
                if not is_oriented[t]:
                    is_oriented[t] = True
                    oriented.append(t)
                    edges_oriented += add_oriented_edges(t)
                    break

        for t in T[1:]:
            # check if the triangle is already oriented, then skip it
            if is_oriented[t]:
                continue

            # if it is not, we will see if another triangle already induced its orientation
            already_oriented_edges = []
            for edge in edges_oriented:
                if edge[0] in t and edge[1] in t:
                    already_oriented_edges.append(edge)

            if len(already_oriented_edges) == 0:    # no induced orientation
                continue

            if len(already_oriented_edges) == 1:    # one edge induced orientation
                edge = already_oriented_edges[0]
                triangle = edge + [p for p in t if p not in edge]

            else:       # we have multiple edges that are already oriented, have to check whether they are consistent
                for i in range(len(already_oriented_edges) - 1):
                    first = already_oriented_edges[i]
                    if first[::-1] in already_oriented_edges:
                        return None
                    else:
                        for next in already_oriented_edges[i+1:]:
                            if first == next:
                                continue
                            elif first[0] == next[0] or first[1] == next[1]:
                                return None
                triangle = already_oriented_edges[0]
                if already_oriented_edges[1][0] in triangle:
                    triangle = triangle + [already_oriented_edges[1][1]]
                elif already_oriented_edges[1][1] in triangle:
                    triangle = [already_oriented_edges[1][0]] + triangle

            oriented.append(triangle)
            is_oriented[t] = True
            edges_oriented += add_oriented_edges(triangle)

    return [tuple(o) for o in oriented]


if __name__ == '__main__':
    M = [(1, 2, 3), (2, 3, 4), (3, 4, 5), (4, 5, 6), (2, 5, 6), (1, 2, 6)]
    S2 = [(1, 2, 3), (1, 2, 4), (1, 3, 4), (2, 3, 4)]
    torus = [(0, 3, 7), (0, 2, 7), (3, 4, 8), (3, 7, 8), (0, 4, 2), (2, 4, 8),
             (2, 7, 5), (1, 2, 5), (7, 6, 8), (5, 6, 7), (1, 2, 8), (1, 6, 8),
             (0, 1, 3), (1, 3, 5), (3, 4, 5), (4, 5, 6), (6, 4, 0), (1, 0, 6)]

    klein = [(0, 3, 7), (0, 2, 7), (3, 4, 8), (3, 7, 8), (0, 4, 1), (1, 4, 8),
             (2, 7, 5), (1, 2, 5), (7, 6, 8), (5, 6, 7), (1, 2, 8), (2, 6, 8),
             (0, 1, 3), (1, 3, 5), (3, 4, 5), (4, 5, 6), (6, 4, 0), (2, 0, 6)]

    sphere = [(1, 2, 3), (1, 3, 4), (1, 2, 4), (2, 3, 5), (3, 4, 5), (2, 4, 5)]

    cylinder = [(1, 2, 4), (2, 4, 5), (2, 3, 5), (3, 5, 6), (1, 3, 6), (1, 4, 6), (1, 2, 3), (4, 5, 6)]

    moebius = [(1, 2, 4), (2, 4, 5), (2, 3, 5), (3, 5, 6), (4, 3, 6), (1, 4, 6)]

    for name, T in [('M', M), ('S2', S2), ('torus', torus), ('Klein bottle', klein), ('sphere', sphere),
                    ('cylinder', cylinder), ('Moebius band', moebius)]:
        print(f"Surface ({name}): {T}")
        print(f'This surface is {["not ", ""][int(orientableQ(T))]}orientable.')
        print(f"Oriented triangles: \n {orientable(T)}")
        print("_________________________________________________________________")


