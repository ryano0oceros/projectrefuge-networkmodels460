import networkx as nx
import matplotlib.pyplot as plt

# Define tasks and dependencies as per the project plan
tasks = {
    'A': 'Describe product',
    'B': 'Develop marketing strategy',
    'C': 'Design brochure',
    'D1': 'Requirements analysis',
    'D2': 'Software design',
    'D3': 'System design',
    'D4': 'Coding',
    'D5': 'Write documentation',
    'D6': 'Unit testing',
    'D7': 'System testing',
    'D8': 'Package deliverables',
    'E': 'Survey potential market',
    'F': 'Develop pricing plan',
    'G': 'Develop implementation plan',
    'H': 'Write client proposal'
}

# Dependencies based on task predecessor information
dependencies = [
    ('A', 'C'), ('A', 'D1'), ('B', 'E'), ('C', 'E'), ('D1', 'D2'), ('D1', 'D3'),
    ('D2', 'D4'), ('D3', 'D4'), ('D4', 'D5'), ('D4', 'D6'), ('D5', 'D8'),
    ('D6', 'D7'), ('D7', 'D8'), ('E', 'F'), ('D8', 'F'), ('D8', 'G'), ('F', 'H'), ('G', 'H')
]

# Initialize directed graph
G = nx.DiGraph()

# Add nodes and edges based on tasks and dependencies
G.add_nodes_from(tasks.keys())
G.add_edges_from(dependencies)

# Draw the graph and save to a file
plt.figure(figsize=(10, 8))
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_size=3000, node_color="skyblue", font_size=10, font_weight="bold", arrows=True)
nx.draw_networkx_labels(G, pos, labels=tasks, font_size=8)
plt.title("Project Task Dependencies")
plt.savefig("project_task_dependencies.png")
plt.close()
