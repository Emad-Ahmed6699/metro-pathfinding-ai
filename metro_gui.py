import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import time
import math

# Import the logic from metro_optimizer
from metro_optimizer import setup_sample_metro, bfs, dfs, dijkstra

class MetroGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Metro Route Optimizer | AI Search")
        self.geometry("1200x800")
        
        # --- Data Setup ---
        self.metro = setup_sample_metro()
        self.selected_algo = tk.StringVar(value="BFS")
        
        # Coordinates for drawing (scaled for canvas)
        self.coords = {
            "Helwan": (500, 750), "Maadi": (500, 600), "Sadat": (500, 400),
            "Shohadaa": (500, 250), "Ghamra": (600, 150), "Marg": (750, 50),
            "Mounib": (200, 750), "Giza": (300, 550), "Shubra": (500, 50),
            "Kit Kat": (200, 250), "Attaba": (350, 250), "Abbassia": (700, 250),
            "Heliopolis": (850, 250)
        }
        
        self.line_colors = {
            "Blue Line": "#00aaff",
            "Red Line": "#ff4444",
            "Green Line": "#00ff88",
            "Yellow Line": "#ffcc00"
        }

        # --- UI Layout ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=300, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.setup_sidebar()

        # Map Area
        self.map_frame = ctk.CTkFrame(self)
        self.map_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        self.canvas = tk.Canvas(
            self.map_frame, 
            bg="#1a1c1e", 
            highlightthickness=0,
            cursor="cross"
        )
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.render_map()

    def setup_sidebar(self):
        ctk.CTkLabel(self.sidebar, text="METRO OPTIMIZER", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)

        # Algorithm Selection
        ctk.CTkLabel(self.sidebar, text="1. Select Algorithm", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(20, 10))
        for algo in ["BFS", "DFS", "Dijkstra"]:
            ctk.CTkRadioButton(self.sidebar, text=algo, variable=self.selected_algo, value=algo).pack(pady=5, padx=20, anchor="w")

        # Station Selection
        stations = sorted(list(self.coords.keys()))
        
        ctk.CTkLabel(self.sidebar, text="2. Choose Path", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(30, 10))
        
        ctk.CTkLabel(self.sidebar, text="Start Station:").pack(padx=20, anchor="w")
        self.start_select = ctk.CTkOptionMenu(self.sidebar, values=stations)
        self.start_select.pack(pady=5, padx=20, fill="x")
        self.start_select.set("Helwan")

        ctk.CTkLabel(self.sidebar, text="Destination:").pack(padx=20, anchor="w")
        self.goal_select = ctk.CTkOptionMenu(self.sidebar, values=stations)
        self.goal_select.pack(pady=5, padx=20, fill="x")
        self.goal_select.set("Shubra")

        # Run Button
        self.run_btn = ctk.CTkButton(self.sidebar, text="RUN OPTIMIZER", command=self.run_search, fg_color="#7000ff", hover_color="#5a00cc")
        self.run_btn.pack(pady=40, padx=20, fill="x")

        # Stats Area
        self.stats_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.stats_frame.pack(pady=10, padx=20, fill="x")
        
        self.stat_labels = {}
        for stat in ["Path Length", "Nodes Expanded", "Total Time"]:
            f = ctk.CTkFrame(self.stats_frame, fg_color="transparent")
            f.pack(fill="x", pady=2)
            ctk.CTkLabel(f, text=f"{stat}:", font=ctk.CTkFont(size=12)).pack(side="left")
            self.stat_labels[stat] = ctk.CTkLabel(f, text="-", font=ctk.CTkFont(size=12, weight="bold"), text_color="#7000ff")
            self.stat_labels[stat].pack(side="right")

    def render_map(self):
        self.canvas.delete("all")
        
        # Draw Connections
        self.edge_ids = {}
        for station, conns in self.metro.graph.items():
            for neighbor, weight, line in conns:
                # To avoid double drawing, sort keys
                pair = tuple(sorted((station, neighbor)))
                if pair not in self.edge_ids:
                    x1, y1 = self.coords[station]
                    x2, y2 = self.coords[neighbor]
                    color = self.line_colors.get(line, "white")
                    eid = self.canvas.create_line(x1, y1, x2, y2, fill=color, width=6, capstyle="round")
                    self.edge_ids[pair] = eid
                    # Add glow effect (background line)
                    self.canvas.tag_lower(self.canvas.create_line(x1, y1, x2, y2, fill=color, width=10, stipple="gray50"))

        # Draw Stations
        self.node_ids = {}
        for name, (x, y) in self.coords.items():
            # Shadow
            self.canvas.create_oval(x-12, y-12, x+12, y+12, fill="#000000", outline="")
            
            # Node
            nid = self.canvas.create_oval(x-10, y-10, x+10, y+10, fill="#2a2d31", outline="white", width=2)
            self.node_ids[name] = nid
            
            # Label
            self.canvas.create_text(x+15, y+5, text=name, fill="white", font=("Arial", 10, "bold"), anchor="w")

    def run_search(self):
        start = self.start_select.get()
        goal = self.goal_select.get()
        algo = self.selected_algo.get()

        if start == goal:
            messagebox.showwarning("Warning", "Start and Goal stations must be different!")
            return

        self.reset_viz()
        
        path = []
        nodes = 0
        total_time = 0

        if algo == "BFS":
            path, nodes = bfs(self.metro, start, goal)
            total_time = self.calculate_path_time(path)
        elif algo == "DFS":
            path, nodes = dfs(self.metro, start, goal)
            total_time = self.calculate_path_time(path)
        elif algo == "Dijkstra":
            path, total_time, nodes = dijkstra(self.metro, start, goal)

        if path:
            self.animate_path(path)
            self.update_stats(len(path), nodes, total_time)
        else:
            messagebox.showerror("Error", "No path found!")

    def calculate_path_time(self, path):
        # Helper for BFS/DFS to get travel time
        if not path: return 0
        total = 0
        last_line = None
        for i in range(len(path) - 1):
            s1, s2 = path[i], path[i+1]
            # Find edge
            for neighbor, weight, line in self.metro.graph[s1]:
                if neighbor == s2:
                    total += weight
                    if last_line and last_line != line:
                        total += self.metro.transfer_cost
                    last_line = line
                    break
        return total

    def reset_viz(self):
        self.render_map()
        for stat in self.stat_labels:
            self.stat_labels[stat].configure(text="-")

    def animate_path(self, path):
        # Highlight path step by step
        for i in range(len(path)):
            station = path[i]
            
            # Pulse Node
            nid = self.node_ids[station]
            self.canvas.itemconfig(nid, fill="#7000ff", outline="#7000ff", width=4)
            self.update()
            time.sleep(0.1)

            if i < len(path) - 1:
                # Highlight Edge
                pair = tuple(sorted((station, path[i+1])))
                if pair in self.edge_ids:
                    eid = self.edge_ids[pair]
                    self.canvas.itemconfig(eid, width=10)
                    self.update()
                    time.sleep(0.2)

    def update_stats(self, length, nodes, time):
        self.stat_labels["Path Length"].configure(text=f"{length} stations")
        self.stat_labels["Nodes Expanded"].configure(text=str(nodes))
        self.stat_labels["Total Time"].configure(text=f"{time} mins")

if __name__ == "__main__":
    # Ensure customtkinter is installed
    try:
        app = MetroGUI()
        app.mainloop()
    except Exception as e:
        print(f"Error starting GUI: {e}")
        print("\nMake sure you have customtkinter installed:")
        print("pip install customtkinter")
