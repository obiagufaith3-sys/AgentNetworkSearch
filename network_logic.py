"""
network_logic.py
================
Contains the network (graph) creation and visualization functions.
"""

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


# ─────────────────────────────────────────────
# NETWORK SETUP
# ─────────────────────────────────────────────
def create_network():
    """
    Create a fixed network (graph) representing connected nodes.
    Nodes  = locations in the network (e.g., computers, routers)
    Edges  = connections between nodes
    """
    G = nx.Graph()

    # Add nodes (numbered 1 to 12)
    G.add_nodes_from(range(1, 13))

    # Add edges (connections between nodes)
    edges = [
        (1, 2), (1, 3), (2, 4), (2, 5),
        (3, 5), (3, 6), (4, 7), (5, 7),
        (5, 8), (6, 8), (6, 9), (7, 10),
        (8, 10), (8, 11), (9, 11), (10, 12),
        (11, 12)
    ]
    G.add_edges_from(edges)

    return G


# ─────────────────────────────────────────────
# VISUALIZATION
# ─────────────────────────────────────────────
def visualize(graph, agents, target_node, step_number, positions):
    """
    Builds and returns a matplotlib figure showing the network state.
    - RED node          = target
    - BLUE node         = not yet visited by anyone
    - Light GREEN node  = visited by Agent A (footprint trail)
    - Light ORANGE node = visited by Agent B (footprint trail)
    - Light PURPLE node = visited by Agent C (footprint trail)
    - If multiple agents visited a node, the FIRST visitor's color wins
    - Bright dot on a node = agent currently standing there
    """

    # Each agent's bright current-position color and their lighter trail shade
    agent_colors       = ["#2ECC71", "#E67E22", "#9B59B6"]   # bright: green, orange, purple
    agent_trail_colors = ["#A9F5D0", "#FAD7A0", "#D7BDE2"]   # light:  green, orange, purple

    fig, ax = plt.subplots(figsize=(9, 6))

    # Build a map: node -> index of the agent who visited it first
    first_visitor = {}
    for i, agent in enumerate(agents):
        for node in agent.visited:
            if node not in first_visitor:
                first_visitor[node] = i   # first agent to visit wins the color

    # Pick a colour for every node in the graph
    node_colors = []
    for node in graph.nodes():
        if node == target_node:
            node_colors.append("#FF4B4B")                       # red — target
        elif node in first_visitor:
            node_colors.append(agent_trail_colors[first_visitor[node]])  # light trail color
        else:
            node_colors.append("#AED6F1")                       # blue — unvisited

    # Draw the base network
    nx.draw(graph, pos=positions, ax=ax, with_labels=True,
            node_color=node_colors, node_size=900,
            font_size=10, font_weight='bold',
            edge_color='#AAAAAA', width=1.5)

    # Draw a bright dot on each agent's current position
    legend_handles = []
    for i, agent in enumerate(agents):
        color = agent_colors[i]
        trail = agent_trail_colors[i]
        x, y  = positions[agent.current_node]
        ax.add_patch(plt.Circle((x, y), 0.07, color=color, zorder=5))
        status = "STOPPED" if not agent.active else "Searching"
        legend_handles.append(mpatches.Patch(
            color=trail,
            label=f"{agent.name} trail ({status})",
            edgecolor=color,
            linewidth=2
        ))

    # Node color key
    legend_handles.append(mpatches.Patch(color="#FF4B4B", label=f"Target — Node {target_node}"))
    legend_handles.append(mpatches.Patch(color="#AED6F1", label="Unvisited node"))

    ax.legend(handles=legend_handles, loc='upper left', fontsize=8, framealpha=0.9)
    ax.set_title(f"Multi-Agent Network Search  |  Step {step_number}", fontsize=13, fontweight='bold')
    plt.tight_layout()
    return fig
