import requests
from bs4 import BeautifulSoup
import networkx as nx
from pyvis.network import Network
import numpy
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import SpectralClustering
from scipy.sparse import csr_matrix


def get_links_from_wikipedia(url, n=2):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # find 'n' links from the introductory section
    parser_output = soup.find('div', class_='mw-parser-output')
    intro_links = []
    if parser_output:
        intro_section = parser_output.find('p')
        if intro_section:
            intro_links = ['https://en.wikipedia.org' + a['href'] for a in intro_section.find_all('a', limit=n) if a.has_attr('href') and a['href'].startswith('/wiki/')]
    
    # find subsections
    subsections = soup.find_all('span', class_='mw-headline')
    
    all_links = intro_links  # start with the links from the introduction
    for subsection in subsections:
        
        parent_section = subsection.find_parent('h2' if subsection.name == 'span' else 'h3')
        
        #grab n links from subsection
        if parent_section:
            links = ['https://en.wikipedia.org' + a['href'] for a in parent_section.find_all_next('a', limit=n) if a.has_attr('href') and a['href'].startswith('/wiki/')]
            all_links.extend(links)

    return all_links

def get_title_from_url(url):
    """Fetch the title of a Wikipedia page using its URL."""
    content = requests.get(url).text
    start_tag = '<title>'
    end_tag = '</title>'
    start_index = content.find(start_tag) + len(start_tag)
    end_index = content.find(end_tag)
    # before all titles, it has '- Wikipedia'  
    title = content[start_index:end_index].replace(' - Wikipedia', '')
    return title

def create_wikipedia_graph(root_url, depth=1):
    G = nx.DiGraph()
    visited = set()
    
    def add_links_to_graph(url, current_depth):
        if url in visited or current_depth > depth:
            return
        visited.add(url)
        links = get_links_from_wikipedia(url)
        
        current_title = get_title_from_url(url)
    
        for link in links:
            linked_title = get_title_from_url(link)
            if not link in visited:  # avoid adding edges to already visited links at depth=0
                G.add_edge(current_title, linked_title)
                add_links_to_graph(link, current_depth + 1)
    
    add_links_to_graph(root_url, 0)
    
    net = Network(notebook=True)
    net.from_nx(G)
    
    # locate and highlight the root_url node in the pyvis network
    root_title = get_title_from_url(root_url)
    for node in net.nodes:
        if node['id'] == root_title:
            node['color'] = 'red'
            node['size'] = 30
            node['title'] = root_title
            break
    
    # display graph
    net.show('graph.html')
    
    return G



root_url = "https://en.wikipedia.org/wiki/Spelunky_2"
G = create_wikipedia_graph(root_url, depth=1)

adj_matrix = nx.adjacency_matrix(G)