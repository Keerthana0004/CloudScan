# import networkx as nx

# def build_resource_graph(terraform_data):
#     G = nx.DiGraph()

#     resources = terraform_data.get("resource", [])
#     for block in resources:
#         for res_type, res_dict in block.items():
#             for name, props in res_dict.items():
#                 node_id = f"{res_type}.{name}"
#                 G.add_node(node_id, **props)

#                 # Add dummy "depends_on" edges if any
#                 if "depends_on" in props:
#                     for dep in props["depends_on"]:
#                         G.add_edge(dep, node_id)

#     return G

# def visualize_graph(G):
#     print("Resources and their connections:")
#     for node in G.nodes:
#         print(f"- {node}")
#     for edge in G.edges:
#         print(f"  {edge[0]} --> {edge[1]}")
