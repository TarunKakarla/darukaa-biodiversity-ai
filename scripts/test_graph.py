from app.graph.reasoning_graph import standalone_test
for c in standalone_test():
    print(c["name"], ":", " -> ".join(c["nodes"]))
