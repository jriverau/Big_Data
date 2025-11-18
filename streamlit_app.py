# Conexión a Neo4j

import streamlit as st
from neo4j import GraphDatabase
from pyvis.network import Network
import networkx as nx

st.title("Grafo interactivo conectado a Neo4j")

# ----------------------------
#  CONEXIÓN A NEO4J (USAR SECRETS)
# ----------------------------
# uri = st.secrets["neo4j"]["uri"]
# user = st.secrets["neo4j"]["user"]
# password = st.secrets["neo4j"]["password"]


# driver = GraphDatabase.driver(uri, auth=(user, password))
driver = GraphDatabase.driver(URI, auth=AUTH)


# ----------------------------
#  CONSULTA DEL GRAFO EN NEO4J
# ----------------------------
def get_graph(tx):
    query = """
    MATCH (a)-[r]->(b)
    RETURN a, r, b
    LIMIT 100
    """
    result = tx.run(query)
    return list(result)


# ----------------------------
#  CONVERTIR A NETWORKX
# ----------------------------
def neo4j_to_nx(records):
    G = nx.DiGraph()

    for row in records:
        a = row["a"]
        r = row["r"]
        b = row["b"]

        # Añadir nodos con labels y propiedades
        G.add_node(
            a.id,
            label=list(a.labels)[0] if a.labels else "Node",
            **a._properties
        )
        G.add_node(
            b.id,
            label=list(b.labels)[0] if b.labels else "Node",
            **b._properties
        )

        # Añadir relación con tipo y propiedades
        G.add_edge(
            a.id,
            b.id,
            type=r.type,
            **r._properties
        )

    return G


# ----------------------------
#  EJECUTAR CONSULTA
# ----------------------------
with driver.session() as session:
    records = session.execute_read(get_graph)

G = neo4j_to_nx(records)


# ----------------------------
#  VISUALIZACIÓN CON PYVIS
# ----------------------------
net = Network(
    height="600px",
    width="100%",
    directed=True,
    bgcolor="#ffffff",
    font_color="black"
)

net.from_nx(G)
net.barnes_hut()  # Físicas para mejor layout

net.save_graph("grafo.html")

# Mostrar en Streamlit
with open("grafo.html", "r", encoding="utf-8") as f:
    st.components.v1.html(f.read(), height=650)
