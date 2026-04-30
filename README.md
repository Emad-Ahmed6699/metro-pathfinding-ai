# Metro Pathfinding AI 🚇

A smart navigation agent that helps passengers find the best way to travel between metro stations using AI search algorithms. This project visualizes how different algorithms (BFS, DFS, and Dijkstra) explore a complex graph of metro stations with multiple lines and closed cycles (loops).

![Project Preview](preview.png)

## ✨ Features

- **Multiple Algorithms**: Compare **BFS**, **DFS**, and **Dijkstra** in real-time.
- **Premium GUI**: Built with `CustomTkinter` for a modern, high-fidelity dark interface.
- **Interactive Map**: Dynamic visualization of metro lines (Blue, Red, Green, and a Yellow loop).
- **Realistic Logic**: 
    - Weights represent travel time between stations.
    - **Transfer Costs**: Switching between lines adds a time penalty, making the optimization realistic.
- **Closed Cycles**: Complex graph structure with multiple loops to test algorithm efficiency.
- **Live Metrics**: Displays nodes expanded, path length, and total travel time.

## 🚀 How to Run

### 1. Prerequisites
Ensure you have Python 3.x installed.

### 2. Install Dependencies
```bash
pip install customtkinter
```

### 3. Run the Application
```bash
python metro_gui.py
```

## 🧠 Algorithms Explained

- **Breadth-First Search (BFS)**: Finds the path with the minimum number of stops (optimality by node count).
- **Depth-First Search (DFS)**: Explores branches deeply; useful for understanding exploration behavior but not optimal.
- **Dijkstra's Algorithm**: Finds the absolute fastest path by considering travel times and transfer penalties (optimality by weight).

## 📄 Project Structure

- `metro_gui.py`: The main GUI application.
- `metro_optimizer.py`: Core logic and algorithm implementations.
- `documentation.md`: Detailed PEAS description and performance analysis.

## 🤝 Contributing
Contributions are welcome! Feel free to open an issue or submit a pull request.

## 📜 License
This project is licensed under the MIT License.
