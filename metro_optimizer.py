import collections
import heapq
import time

class MetroGraph:
    def __init__(self, transfer_cost=5):
        # graph[station] = [(neighbor, weight, line_name)]
        self.graph = collections.defaultdict(list)
        self.transfer_cost = transfer_cost
        self.stations_info = {} # station -> {lines: set()}

    def add_connection(self, s1, s2, weight, line):
        self.graph[s1].append((s2, weight, line))
        self.graph[s2].append((s1, weight, line))
        
        if s1 not in self.stations_info: self.stations_info[s1] = {'lines': set()}
        if s2 not in self.stations_info: self.stations_info[s2] = {'lines': set()}
        self.stations_info[s1]['lines'].add(line)
        self.stations_info[s2]['lines'].add(line)

# --- Algorithm Implementations ---

def bfs(metro, start, goal):
    """Find path with fewest stations."""
    queue = collections.deque([(start, [start])])
    visited = {start}
    nodes_expanded = 0

    while queue:
        current, path = queue.popleft()
        nodes_expanded += 1
        
        if current == goal:
            return path, nodes_expanded

        for neighbor, weight, line in metro.graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    return None, nodes_expanded

def dfs(metro, start, goal):
    """Find any path (not necessarily shortest)."""
    stack = [(start, [start])]
    visited = set()
    nodes_expanded = 0

    while stack:
        current, path = stack.pop()
        nodes_expanded += 1
        
        if current == goal:
            return path, nodes_expanded

        if current not in visited:
            visited.add(current)
            for neighbor, weight, line in metro.graph[current]:
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))
    return None, nodes_expanded

def dijkstra(metro, start, goal):
    """Find path with minimum time (including transfer costs)."""
    # pq: (total_time, current_station, path, current_line)
    pq = [(0, start, [start], None)]
    distances = {} # (station, line) -> time
    nodes_expanded = 0

    while pq:
        current_time, current_station, path, current_line = heapq.heappop(pq)
        nodes_expanded += 1

        if current_station == goal:
            return path, current_time, nodes_expanded

        # State is defined by (station, line) because transfer costs depend on the line
        state = (current_station, current_line)
        if state in distances and distances[state] <= current_time:
            continue
        distances[state] = current_time

        for neighbor, weight, line in metro.graph[current_station]:
            new_time = current_time + weight
            
            # Add transfer cost if switching lines
            if current_line is not None and current_line != line:
                new_time += metro.transfer_cost
            
            new_path = path + [neighbor]
            heapq.heappush(pq, (new_time, neighbor, new_path, line))
            
    return None, float('inf'), nodes_expanded

# --- Sample Data (Cairo Metro Inspired) ---

def setup_sample_metro():
    metro = MetroGraph(transfer_cost=5)
    
    # Line 1 (Blue) - Vertical Main Line
    l1 = "Blue Line"
    metro.add_connection("Helwan", "Maadi", 10, l1)
    metro.add_connection("Maadi", "Sadat", 15, l1)
    metro.add_connection("Sadat", "Shohadaa", 5, l1)
    metro.add_connection("Shohadaa", "Ghamra", 5, l1)
    metro.add_connection("Ghamra", "Marg", 20, l1)

    # Line 2 (Red) - Diagonal Line
    l2 = "Red Line"
    metro.add_connection("Mounib", "Giza", 8, l2)
    metro.add_connection("Giza", "Sadat", 12, l2)
    metro.add_connection("Sadat", "Shohadaa", 5, l2)
    metro.add_connection("Shohadaa", "Shubra", 15, l2)

    # Line 3 (Green) - Horizontal Line
    l3 = "Green Line"
    metro.add_connection("Kit Kat", "Attaba", 10, l3)
    metro.add_connection("Attaba", "Abbassia", 8, l3)
    metro.add_connection("Abbassia", "Heliopolis", 12, l3)
    
    # --- CYCLES & INTERCONNECTIONS ---
    # Connection between Attaba (L3) and Shohadaa (L1/L2)
    metro.add_connection("Attaba", "Shohadaa", 4, l2)
    
    # New connection: Giza (L2) to Kit Kat (L3) - West Loop
    metro.add_connection("Giza", "Kit Kat", 20, "Yellow Line")
    
    # New connection: Heliopolis (L3) to Marg (L1) - East Loop
    metro.add_connection("Heliopolis", "Marg", 25, "Yellow Line")
    
    # New connection: Mounib (L2) to Helwan (L1) - South Loop
    metro.add_connection("Mounib", "Helwan", 30, "Yellow Line")
    
    return metro

def main():
    metro = setup_sample_metro()
    start = "Helwan"
    goal = "Shubra"

    print(f"--- Metro Route Optimizer ---")
    print(f"From: {start} | To: {goal}\n")

    # BFS
    t0 = time.time()
    path_bfs, nodes_bfs = bfs(metro, start, goal)
    dt_bfs = (time.time() - t0) * 1000
    print(f"[BFS] Path: {' -> '.join(path_bfs)}")
    print(f"      Nodes Expanded: {nodes_bfs} | Time: {dt_bfs:.2f}ms\n")

    # DFS
    t0 = time.time()
    path_dfs, nodes_dfs = dfs(metro, start, goal)
    dt_dfs = (time.time() - t0) * 1000
    print(f"[DFS] Path: {' -> '.join(path_dfs)}")
    print(f"      Nodes Expanded: {nodes_dfs} | Time: {dt_dfs:.2f}ms\n")

    # Dijkstra
    t0 = time.time()
    path_dij, time_dij, nodes_dij = dijkstra(metro, start, goal)
    dt_dij = (time.time() - t0) * 1000
    print(f"[Dijkstra] Path: {' -> '.join(path_dij)}")
    print(f"           Total Time: {time_dij} mins (includes transfers)")
    print(f"           Nodes Expanded: {nodes_dij} | Time: {dt_dij:.2f}ms\n")

if __name__ == "__main__":
    main()
