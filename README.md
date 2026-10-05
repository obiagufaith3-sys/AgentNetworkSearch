# Multi-Agent Network Search

An interactive Streamlit web application that simulates collaborative multi-agent pathfinding and network exploration. Autonomous search agents coordinate using a shared message board and global memory map to prevent redundant searches and efficiently locate a target node within a network graph.

## Features

- **Collaborative Multi-Agent Architecture:** Independent search agents traverse the network graph simultaneously, making decisions based on both local and shared intelligence.
- **Shared Memory & Communication:** Agents log visited nodes onto a centralized message board, allowing other agents to skip previously searched areas and avoid redundant traversal.
- **Dynamic Real-Time UI:** Built with Streamlit, providing live visualization updates, step-by-step metrics tracking (nodes covered, messages sent, active status), and customized agent paths.

## Tech Stack

- **Language:** Python
- **Framework:** Streamlit
- **Libraries:** NetworkX, Matplotlib, Random

## Getting Started Locally

To run this project on your machine:

1. **Clone the repository:**
   ```
   git clone https://github.com/obiagufaith3-sys/AgentNetworkSearch.git
   ```
2. **Open the project folder** in your code editor (e.g., VS Code).
3. **Install dependencies:**
   ```
   pip install streamlit networkx matplotlib
   ```
4. **Run the application:
 ```
streamlit run streamlit_app.py
```
