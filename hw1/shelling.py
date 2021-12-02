
def shelling(T):
    """Returnes shelling of triangles from triangulation T."""
    if len(T) <= 1:
        return T
    ordered_T = [T[0]]
    edges = [T[0][:2], T[0][1:], (T[0][0], T[0][2])]
    vertices = [v for v in T[0]]
    unused = T[1:]
    while len(unused) != 0:
        t = unused.pop(0)
        t_edges = [t[:2], t[1:], (t[0], t[2])]
        new_edges = [e for e in t_edges if e not in edges and e[::-1] not in edges]
        if len(new_edges) == 3:
            unused.append(t)
            continue
        new_vertices = [v for v in t if v not in vertices]
        euler = len(ordered_T) + 1 - len(edges) - len(new_edges) + len(vertices) + len(new_vertices)
        if euler == 1:
            ordered_T.append(t)
            edges += new_edges
            vertices += new_vertices
        else:
            print(euler)
            unused.append(t)
    return ordered_T


if __name__ == '__main__':
    T = [(1, 2, 6), (1, 5, 6), (2, 3, 7), (2, 6, 7), (3, 4, 8), (3, 7, 8), (5, 6, 9), (6, 7, 11),
         (6, 9, 10), (6, 10, 11), (7, 8, 12), (7, 11, 12), (9, 10, 13), (10, 13, 14),
         (10, 11, 15), (10, 14, 15), (11, 12, 15), (12, 15, 16)]
    print(shelling(T))

    T2 = [(1, 2, 6), (7, 11, 12), (3, 4, 8), (2, 3, 7), (6, 10, 11), (2, 6, 7), (3, 7, 8), (5, 6, 9), (6, 7, 11),
          (6, 9, 10)]
    print(shelling(T2))
