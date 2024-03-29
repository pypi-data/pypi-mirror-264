from natural import insert_into_graph  # type: ignore

insert_into_graph("Tell me about quantum mechanics?")

# from graphviz import Digraph  # type: ignore
# from models import KnowledgeGraph  # type: ignore
#
# kg = {
#     "nodes": [
#         {
#             "id": 1,
#             "body": "How to ace DSA interview",
#             "label": "User Query",
#             "color": "blue",
#         },
#         {
#             "id": 2,
#             "body": "Data Structures and Algorithms (DSA)",
#             "label": "Subject",
#             "color": "orange",
#         },
#         {
#             "id": 3,
#             "body": "Interview Preparation",
#             "label": "Category",
#             "color": "orange",
#         },
#         {
#             "id": 4,
#             "body": "Practice Coding Questions",
#             "label": None,
#             "color": "yellow",
#         },
#         {"id": 5, "body": "Understand Concepts", "label": None, "color": "yellow"},
#         {
#             "id": 6,
#             "body": "Review Time Complexity and Space Complexity",
#             "label": None,
#             "color": "yellow",
#         },
#         {
#             "id": 7,
#             "body": "Utilize Online Platforms like LeetCode and HackerRank",
#             "label": None,
#             "color": "yellow",
#         },
#     ],
#     "edges": [
#         {"id": 1, "source": 1, "target": 2, "label": "Focuses on", "color": "black"},
#         {"id": 2, "source": 1, "target": 3, "label": "Belongs to", "color": "black"},
#         {"id": 3, "source": 3, "target": 4, "label": "Includes", "color": "black"},
#         {"id": 4, "source": 3, "target": 5, "label": "Includes", "color": "black"},
#         {"id": 5, "source": 3, "target": 6, "label": "Includes", "color": "black"},
#         {"id": 6, "source": 3, "target": 7, "label": "Includes", "color": "black"},
#     ],
# }
#
#
# def visualize_knowledge_graph(kg: KnowledgeGraph):
#     dot = Digraph(comment="Knowledge Graph")
#
#     print(kg["nodes"], type(kg))
#
#     # Add nodes
#     for node in kg["nodes"]:
#         dot.node(str(node["id"]), node["label"], color=node["color"])
#
#     # Add edges
#     for edge in kg["edges"]:
#         dot.edge(
#             str(edge["source"]),
#             str(edge["target"]),
#             label=edge["label"],
#             color=edge["color"],
#         )
#
#     # Render the graph
#     dot.render("knowledge_graph.gv", view=True)
#
#
# # graph = generate_graph("Teach me how to make tea")
# visualize_knowledge_graph(kg)
