from neo4j import GraphDatabase

# Conexión a Neo4j
URI = "neo4j+s://b29b29cb.databases.neo4j.io"
AUTH= ("neo4j", "D7MvqURA0Ov-q71KDA9ZqkvU2FeEjn2DsIK5RlodsSg")

driver = GraphDatabase.driver(URI, auth=AUTH)

def get_graph(tx):
    query = """
    MATCH (a)-[r]->(b)
    RETURN a, r, b
    LIMIT 100
    """
    return list(tx.run(query))

def load_graph():
    with driver.session() as session:
        return session.execute_read(get_graph)
import networkx as nx

def neo4j_to_networkx(records):
    G = nx.DiGraph()

    for row in records:
        a = row["a"]
        b = row["b"]
        r = row["r"]

        # Nodos con labels
        G.add_node(a.id, label=list(a.labels)[0], **a._properties)
        G.add_node(b.id, label=list(b.labels)[0], **b._properties)

        # Relación con tipo
        G.add_edge(a.id, b.id, type=r.type, **r._properties)

    return G
from pyvis.network import Network

def draw_graph(G):
    net = Network(height="600px", width="100%", directed=True)
    net.from_nx(G)

    # Opcional: configurar físicas
    net.barnes_hut()

    net.save_graph("grafo.html")
    
    with open("grafo.html", "r", encoding="utf-8") as f:
        html = f.read()
    st.components.v1.html(html, height=650)
import streamlit as st
from neo4j import GraphDatabase
from pyvis.network import Network
import networkx as nx

st.title("Grafo interactivo conectado a Neo4j")

# Conexión a Neo4j (usar secrets en Streamlit Cloud)
# uri = st.secrets["neo4j"]["uri"]
# user = st.secrets["neo4j"]["user"]
# password = st.secrets["neo4j"]["password"]

driver = GraphDatabase.driver(URI, auth=AUTH)

def get_graph(tx):
    query = """
    MATCH (a)-[r]->(b)
    RETURN a, r, b
    LIMIT 100
    """
    return tx.run(query).data()

def neo4j_to_nx(records):
    G = nx.DiGraph()
    for row in records:
        a, r, b = row["a"], row["r"], row["b"]
        
        G.add_node(a.id, label=list(a.labels)[0], **a._properties)
        G.add_node(b.id, label=list(b.labels)[0], **b._properties)

        G.add_edge(a.id, b.id, type=r.type, **r._properties)
    return G

# Cargar datos
with driver.session() as session:
    records = session.execute_read(get_graph)

G = neo4j_to_nx(records)

# Visualizar
net = Network(height="600px", width="100%", directed=True)
net.from_nx(G)
net.barnes_hut()
net.save_graph("grafo.html")

with open("grafo.html", "r", encoding="utf-8") as f:
    st.components.v1.html(f.read(), height=650)
