import networkx as nx
import matplotlib.pyplot as plt


def findComponents(V, E):
    """Returns components of graph given by vertices V and edges E."""
    all_points = {}
    connections = {}
    for point in V:
        all_points[point] = 0
        connections[point] = []

    for v1, v2 in E:
        connections[v1].append(v2)
        connections[v2].append(v1)

    if len(V) == 0:
        return []

    comp_list = [V[0]]
    while len(comp_list) != 0:
        current_point = comp_list.pop()
        if all_points[current_point] == 0:
            component = max(all_points.values()) + 1
            all_points[current_point] = component
        else:
            component = all_points[current_point]
        for p in connections[current_point]:
            if all_points[p] == 0:
                comp_list.append(p)
                all_points[p] = component
            else:
                if component != all_points[p]:
                    print('different components')

        if len(comp_list) == 0:
            for p in all_points.keys():
                if all_points[p] == 0:
                    comp_list.append(p)
                    break

    components = [[] for _ in range(max(all_points.values()))]
    for p in all_points.keys():
        components[all_points[p] - 1].append(p)

    return components


if __name__ == '__main__':

    V1 = [1, 2, 3, 4, 5, 6, 7, 8]
    E1 = [(1, 2), (2, 3), (1, 3), (4, 5), (5, 6), (5, 7), (6, 7), (7, 8)]

    V2 = [1, 2, 3, 4, 5]
    E2 = [(1, 2), (1, 3), (1, 4), (1, 5)]

    V3 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    E3 = [(1, 2), (1, 3), (1, 8), (3, 7), (4, 5), (4, 6), (4, 9), (5, 6), (5, 9), (7, 8)]

    V4 = [1, 2, 3, 4, 5, 6, 7]
    E4 = [(1, 2), (2, 3), (1, 3), (4, 5), (6, 7)]

    V5 = [1, 2, 3, 4, 5]
    E5 = []

    V6 = [1, 2, 3, 4, 5, 6]
    E6 = [(1, 2), (3, 4), (5, 6), (1, 6)]

    g = 1

    for V, E in zip([V1, V2, V3, V4, V5, V6], [E1, E2, E3, E4, E5, E6]):
        comp = findComponents(V, E)

        # setting colors of edges
        colors = ['dodgerblue', 'tomato', 'palegreen', 'peru', 'plum']
        points_colors = [None for _ in range(len(V))]
        for i in range(len(comp)):
            for c in comp[i]:
                points_colors[c-1] = colors[i]

        G = nx.Graph()
        for v in V:
            G.add_node(v)
        for e in E:
            G.add_edge(*e)

        plt.figure(figsize=(max(6, len(E) - 2), 5))
        ax = plt.gca()
        ax.set_title(f'Input: V = {V}, \n   E = {E} \n Output: {comp}', loc='left')

        nx.draw(G, with_labels=True, pos=nx.planar_layout(G), node_color=points_colors, node_size=500)

        plt.savefig(f'Graph{g}')

        g += 1
