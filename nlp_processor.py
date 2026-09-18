import pandas as pd
import spacy
import networkx as nx
import json

print("Loading NLP Model...")
nlp = spacy.load("en_core_web_sm")
G = nx.Graph()

# 1. Ingest & Extract Unstructured FIRs
df_firs = pd.read_csv("mock_firs.csv")
for text in df_firs['text']:
    doc = nlp(text)
    entities = [ent.text for ent in doc.ents if ent.label_ in ["PERSON", "GPE", "LOC", "FAC"]]
    for i in range(len(entities)):
        G.add_node(entities[i])
        for j in range(i+1, len(entities)):
            G.add_edge(entities[i], entities[j], relation="Co-occurrence")

# 2. Ingest Structured Call Data
df_cdrs = pd.read_csv("mock_cdrs.csv")
for _, row in df_cdrs.iterrows():
    G.add_edge(row['caller'], row['receiver'], relation="Phone Call")

# 3. Ingest Structured Financial Data
df_txns = pd.read_csv("mock_financials.csv")
for _, row in df_txns.iterrows():
    G.add_edge(row['sender'], row['receiver'], relation="Money Transfer")

# 4. Math: Betweenness Centrality (Finds bridge nodes / intermediaries)
bet_centrality = nx.betweenness_centrality(G)

# 5. Math: Anomaly Detection (Finds closed loops indicating laundering or burner rings)
cycles = nx.cycle_basis(G)
suspicious_nodes = set()
for cycle in cycles:
    if len(cycle) <= 4:  # Short loops are highly suspicious
        suspicious_nodes.update(cycle)

nodes = []
for node in G.nodes():
    score = bet_centrality[node]
    is_anomaly = node in suspicious_nodes
    
    # Calculate a 1-100 threat score
    threat_level = int(score * 200) + (30 if is_anomaly else 0)
    
    # Red for high threat or anomalies, Blue for standard nodes. Stars indicate anomalies.
    node_color = "#ef4444" if threat_level > 40 else "#3b82f6"
    node_shape = "star" if is_anomaly else "dot"
    
    nodes.append({
        "id": node, 
        "label": f"{node}\n(Threat: {threat_level})", 
        "color": node_color, 
        "shape": node_shape,
        "size": 15 + (score * 100),
        "font": {"color": "white"}
    })

edges = [{"from": u, "to": v, "label": d['relation'], "color": {"color": "#64748b"}} for u, v, d in G.edges(data=True)]

with open("network_data.json", "w") as f:
    json.dump({"nodes": nodes, "edges": edges}, f)

print("Success: Influencers and anomalies mathematically detected.")