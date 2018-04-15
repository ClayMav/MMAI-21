"""
Provides pathing utilities.
"""
import heapq


def get_tile_neighbors(tile):
    """
    Collects all of neighbors surrounding a tile with no restrictions.
    """
    return [x for x in tile.get_neighbors() if x.type == "water" and x.port == None]

    # return tile.get_neighbors()

def move_cost(start, end):
    """
    Determines the move cost between two nodes.
    """
    return 1

def find_path(start_tiles, goal_tiles, get_neighbors=get_tile_neighbors,
              g_func=lambda x, y: 1, f_func=lambda x, y: 0):
    """
    Given a list of starting locations and a list of ending locations,
    find the shortest path between them. Uses a priority queue to
    do Uniform Cost Search (think Breadth First Search, but with movement
    cost included).
    """
    path = []
    frontier = [(0, x) for x in start_tiles]
    path_from = dict()
    closed = set()

    g_score = {x: 0 for x in start_tiles}
    f_score = {x: g_score[x] + f_func(x, goal_tiles) for x in start_tiles}
    heapq.heapify(frontier)

    while frontier:
        _weight, working_tile = heapq.heappop(frontier)

        if working_tile in goal_tiles:
            current = working_tile
            path = [current]

            while path_from.get(current):
                current = path_from.get(current)
                if current not in start_tiles:
                    path.append(current)
            path.reverse()

            return current, path

        closed.add(working_tile)

        for neighbor in get_neighbors(working_tile):
            if neighbor in closed:
                continue

            new_g = g_score[working_tile] + g_func(working_tile, neighbor)

            if new_g < g_score.get(neighbor, 1000000):
                g_score[neighbor] = new_g
                f_score[neighbor] = new_g + f_func(working_tile, goal_tiles)
                path_from[neighbor] = working_tile
                heapq.heappush(frontier, (f_score[neighbor], neighbor))
    return None, []
