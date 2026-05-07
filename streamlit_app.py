"""
streamlit_app.py
================
Streamlit web app for the Multi-Agent Network Search Simulation.
Run with:   streamlit run streamlit_app.py
"""

import time
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

from agent_logic import MessageBoard, SearchAgent
from network_logic import create_network, visualize

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Multi-Agent Network Search",
    page_icon="🔍",
    layout="wide"
)

# ── Title ─────────────────────────────────────────────────────────────────────
st.title("Multi-Agent Network Search Simulation")
st.caption("Artificial Intelligence Project — Agent Communication for Searching a Network")
st.divider()

# ── Build the network once and cache it ──────────────────────────────────────
@st.cache_resource
def get_network():
    G = create_network()
    positions = nx.spring_layout(G, seed=42)
    return G, positions

G, positions = get_network()

# ── Sidebar — Controls ───────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Simulation Controls")

    # Show the node list so the user knows valid options
    st.caption(f"Network has nodes: {sorted(G.nodes())}")

    # Target node input — user types any number from 1 to 12
    target_input = st.number_input(
        label="🎯 Target Node",
        min_value=1,
        max_value=12,
        value=10,
        step=1,
        help="Choose which node the agents should search for (1 to 12)"
    )
    target_node = int(target_input)

    # Speed slider — controls delay between steps
    speed = st.slider(
        label="⏱ Speed (seconds per step)",
        min_value=0.3,
        max_value=2.0,
        value=0.8,
        step=0.1,
        help="Lower = faster simulation"
    )

    st.divider()

    # Agent starting positions (fixed but shown clearly)
    st.subheader("🤖 Agent Start Positions")
    st.markdown("- **Agent A** — Node 1 (🟢 Green)")
    st.markdown("- **Agent B** — Node 6 (🟠 Orange)")
    st.markdown("- **Agent C** — Node 12 (🟣 Purple)")

    st.divider()

    # Validate: make sure target isn't the same as a start node
    start_nodes = [1, 6, 12]
    if target_node in start_nodes:
        st.warning(f"⚠️ Node {target_node} is a start node. Agent will find it immediately. Choose a different target for a better demo.")

    # Start button
    start = st.button("▶ Start Simulation", type="primary", use_container_width=True)
    reset = st.button("↺ Reset", use_container_width=True)

# ── Main area layout ──────────────────────────────────────────────────────────
col_graph, col_log = st.columns([2, 1])

with col_graph:
    st.subheader("📡 Network Graph")
    graph_placeholder = st.empty()   # This updates live during simulation

with col_log:
    st.subheader("📨 Agent Messages")
    log_placeholder = st.empty()     # This updates live during simulation

# Metrics row
m1, m2, m3, m4 = st.columns(4)
step_metric    = m1.empty()
covered_metric = m2.empty()
msg_metric     = m3.empty()
status_metric  = m4.empty()

# ── Helper: draw the initial (blank) network ──────────────────────────────────
def show_initial_graph():
    fig, ax = plt.subplots(figsize=(9, 6))
    node_colors = ["#FF4B4B" if n == target_node else "#AED6F1" for n in G.nodes()]
    nx.draw(G, pos=positions, ax=ax, with_labels=True,
            node_color=node_colors, node_size=900,
            font_size=10, font_weight='bold',
            edge_color='#AAAAAA', width=1.5)
    ax.set_title(f"Network — Target is Node {target_node} (red)", fontsize=13, fontweight='bold')
    plt.tight_layout()
    graph_placeholder.pyplot(fig)
    plt.close(fig)

# Show the initial graph when the app first loads
show_initial_graph()

# Show blank metrics on load
step_metric.metric("Step", "—")
covered_metric.metric("Nodes Covered", "—")
msg_metric.metric("Messages Sent", "—")
status_metric.metric("Status", "Waiting")

# ── Run simulation when Start is pressed ─────────────────────────────────────
if start:

    # Create fresh board and agents
    board   = MessageBoard()
    agent_A = SearchAgent("Agent A", start_node=1,  target_node=target_node, graph=G, board=board)
    agent_B = SearchAgent("Agent B", start_node=6,  target_node=target_node, graph=G, board=board)
    agent_C = SearchAgent("Agent C", start_node=12, target_node=target_node, graph=G, board=board)
    agents  = [agent_A, agent_B, agent_C]

    # Post deployment messages
    for agent in agents:
        board.post(agent.name, f"Deployed at Node {agent.current_node}. Searching for Node {target_node}.")

    # Agent dot colours for the message log
    agent_color_map = {
        "Agent A": "🟢",
        "Agent B": "🟠",
        "Agent C": "🟣"
    }

    step = 0
    max_steps = 30

    while step < max_steps:
        step += 1

        # ── Draw updated graph ──────────────────────────────────────────────
        fig = visualize(G, agents, target_node, step, positions)
        graph_placeholder.pyplot(fig)
        plt.close(fig)

        # ── Update message log ──────────────────────────────────────────────
        log_lines = []
        for msg in board.messages[-20:]:   # Show last 20 messages
            icon = "🔴" if "TARGET FOUND" in msg else "⚪"
            for name, emoji in agent_color_map.items():
                if name in msg:
                    icon = emoji
                    break
            log_lines.append(f"{icon} {msg}")

        log_placeholder.markdown("\n\n".join(log_lines))

        # ── Update metrics ──────────────────────────────────────────────────
        nodes_covered = len(board.shared_visited)
        step_metric.metric("Step", step)
        covered_metric.metric("Nodes Covered", f"{nodes_covered} / {G.number_of_nodes()}")
        msg_metric.metric("Messages Sent", len(board.messages))
        status_metric.metric("Status", "🔴 Found!" if board.target_found else "🔍 Searching...")

        # ── Check if done ───────────────────────────────────────────────────
        all_stopped = all(not agent.active for agent in agents)
        if all_stopped:
            break

        # ── Each active agent takes a turn ──────────────────────────────────
        for agent in agents:
            if agent.active:
                found = agent.look_around()
                if found:
                    break
                else:
                    agent.move()

        time.sleep(speed)

    # ── Final frame after loop ends ─────────────────────────────────────────
    fig = visualize(G, agents, target_node, step, positions)
    graph_placeholder.pyplot(fig)
    plt.close(fig)

    # ── Final summary ────────────────────────────────────────────────────────
    st.divider()
    if board.target_found:
        st.success(f"✅ {board.finder} found the target at Node {target_node} in {step} steps!")
    else:
        st.error("❌ Target was not found within the step limit.")

    st.subheader("📋 Agent Paths")
    for agent in agents:
        path_str = " → ".join(str(n) for n in agent.path)
        st.markdown(f"**{agent.name}:** {path_str}")

# ── Reset ─────────────────────────────────────────────────────────────────────
if reset:
    show_initial_graph()
    log_placeholder.empty()
    step_metric.metric("Step", "—")
    covered_metric.metric("Nodes Covered", "—")
    msg_metric.metric("Messages Sent", "—")
    status_metric.metric("Status", "Waiting")
    st.info("Reset complete. Adjust settings and press Start.")
