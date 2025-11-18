import streamlit as st
from pyvis.network import Network
import networkx as nx

st.title("Grafo interactivo con PyVis")

# Crear grafo
G = nx.Graph()
G.add_nodes_from(["A", "B", "C"])
G.add_edges_from([("A","B"), ("B","C")])

# Convertir grafo a PyVis
net = Network(height="500px", width="100%", bgcolor="#ffffff", font_color="black")
net.from_nx(G)

# Guardar en HTML
net.save_graph("grafo.html")

# Mostrar en Streamlit
with open("grafo.html", "r", encoding="utf-8") as f:
    html = f.read()
st.components.v1.html(html, height=550)
