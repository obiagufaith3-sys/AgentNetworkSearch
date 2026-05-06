"""
agent_logic.py
==============
Contains the MessageBoard (agent communication) and SearchAgent class.
"""

import random


# ─────────────────────────────────────────────
# SHARED MESSAGE BOARD (Agent Communication)
# ─────────────────────────────────────────────
class MessageBoard:
    """
    A shared communication board all agents can read and write to.
    This simulates agent-to-agent communication in a network.
    """
    def __init__(self):
        self.messages = []           # List of all messages posted
        self.target_found = False    # Flag: has any agent found the target?
        self.finder = None           # Which agent found the target?
        self.shared_visited = set()  # NEW: all nodes visited by ANY agent

    def post(self, agent_name, message):
        """An agent posts a message to the board."""
        full_message = f"[{agent_name}]: {message}"
        self.messages.append(full_message)
        print(full_message)

    def mark_visited(self, node):
        """Any agent that visits a node registers it here so others know."""
        self.shared_visited.add(node)

    def announce_found(self, agent_name, node):
        """An agent announces it found the target."""
        self.target_found = True
        self.finder = agent_name
        self.post(agent_name, f"TARGET FOUND at Node {node}! All agents stopping.")


# ─────────────────────────────────────────────
# AGENT CLASS
# ─────────────────────────────────────────────
class SearchAgent:
    """
    An agent that traverses the network searching for the target node.
    It communicates via the shared MessageBoard.
    """
    def __init__(self, name, start_node, target_node, graph, board):
        self.name = name                    # Agent identifier e.g "Agent A"
        self.current_node = start_node      # Where the agent starts
        self.target_node = target_node      # What the agent is looking for
        self.graph = graph                  # The network to search
        self.board = board                  # Shared communication board
        self.visited = set()                # Nodes this agent has already visited
        self.path = [start_node]            # Trail of nodes visited
        self.active = True                  # Is this agent still searching?

    def look_around(self):
        """Check if the current node is the target."""
        if self.current_node == self.target_node:
            self.board.announce_found(self.name, self.current_node)
            self.active = False
            return True
        return False

    def move(self):
        """
        Move to a neighboring node that hasn't been visited yet.
        If all neighbors are visited, pick any neighbor (backtrack).
        """
        # Check if another agent already found the target
        if self.board.target_found:
            if self.active:
                self.board.post(self.name, f"Received broadcast. Stopping at Node {self.current_node}.")
                self.active = False
            return

        # Register current node on both personal and shared visited lists
        self.visited.add(self.current_node)
        self.board.mark_visited(self.current_node)

        neighbors = list(self.graph.neighbors(self.current_node))

        # First priority: nodes no agent has visited yet (uses shared list)
        globally_unvisited = [n for n in neighbors if n not in self.board.shared_visited]

        # Second priority: nodes this agent hasn't visited (but another may have)
        personally_unvisited = [n for n in neighbors if n not in self.visited]

        if globally_unvisited:
            next_node = random.choice(globally_unvisited)
            self.board.post(self.name, f"Moving to Node {next_node} (fresh - no agent has been here)")
        elif personally_unvisited:
            next_node = random.choice(personally_unvisited)
            self.board.post(self.name, f"Moving to Node {next_node} (visited by another agent, not me)")
        elif neighbors:
            next_node = random.choice(neighbors)
            self.board.post(self.name, f"Backtracking to Node {next_node} (all neighbors covered)")
        else:
            self.board.post(self.name, f"Dead end at Node {self.current_node}. No moves available.")
            self.active = False
            return

        self.current_node = next_node
        self.path.append(next_node)