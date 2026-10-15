from collections import deque
import heapq

def dijkstra(graph, start, target):
    """Return (shortest_path, distance) using Dijkstra and a min-priority queue."""
    distances = {node: float("inf") for node in graph}
    previous = {node: None for node in graph}
    distances[start] = 0
    queue = [(0, start)]

    while queue:
        current_distance, current = heapq.heappop(queue)
        if current_distance != distances[current]:
            continue
        if current == target:
            break
        for neighbor, weight in graph[current].items():
            new_distance = current_distance + weight
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = current
                heapq.heappush(queue, (new_distance, neighbor))

    if distances[target] == float("inf"):
        return [], None

    path = []
    current = target
    while current is not None:
        path.append(current)
        current = previous[current]
    path.reverse()
    return path, distances[target]


def bfs_order(graph, start):
    """Return BFS visitation order. Queue is implemented with collections.deque."""
    visited = {start}
    queue = deque([start])
    order = []
    while queue:
        current = queue.popleft()
        order.append(current)
        for neighbor in sorted(graph[current]):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return order


def dfs_order(graph, start):
    """Return DFS visitation order using an explicit stack."""
    visited = set()
    stack = [start]
    order = []
    while stack:
        current = stack.pop()
        if current in visited:
            continue
        visited.add(current)
        order.append(current)
        # Reverse sorted order so traversal output is predictable.
        for neighbor in sorted(graph[current], reverse=True):
            if neighbor not in visited:
                stack.append(neighbor)
    return order


def bfs_path(graph, start, target):
    """Find a path with fewest edges (not necessarily shortest distance)."""
    queue = deque([start])
    previous = {start: None}
    while queue:
        current = queue.popleft()
        if current == target:
            break
        for neighbor in graph[current]:
            if neighbor not in previous:
                previous[neighbor] = current
                queue.append(neighbor)
    if target not in previous:
        return []
    path = []
    current = target
    while current is not None:
        path.append(current)
        current = previous[current]
    return list(reversed(path))


def dfs_path(graph, start, target):
    """Find the first path discovered by DFS; it is not guaranteed shortest."""
    stack = [start]
    previous = {start: None}
    while stack:
        current = stack.pop()
        if current == target:
            break
        for neighbor in sorted(graph[current], reverse=True):
            if neighbor not in previous:
                previous[neighbor] = current
                stack.append(neighbor)
    if target not in previous:
        return []
    path = []
    current = target
    while current is not None:
        path.append(current)
        current = previous[current]
    return list(reversed(path))


def connected_components(graph):
    """Return groups of locations that are connected to each other."""
    visited = set()
    components = []
    for node in graph:
        if node not in visited:
            component = []
            queue = deque([node])
            visited.add(node)
            while queue:
                current = queue.popleft()
                component.append(current)
                for neighbor in graph[current]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
            components.append(component)
    return components
