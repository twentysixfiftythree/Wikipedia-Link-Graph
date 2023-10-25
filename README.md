# Wikipedia-Link-Graph
## Description
This script is designed to create a directed graph based on Wikipedia links starting from a given URL. It fetches links from the introductory section and subsections of a Wikipedia page, adds them to a directed graph, and visualizes the network using PyVis.




## Functions
get_links_from_wikipedia(url, n=5)
Fetches the first n links from each subsection of the wikipedia page.

get_title_from_url(url)
Fetches the title of a Wikipedia page using its URL.

create_wikipedia_graph(root_url, depth=1)
Creates a 'directed' graph from a given Wikipedia URL, following links up to a specified depth. The graph is visualized using PyVis.

## Notes
The create_wikipedia_graph function uses a depth-first search algorithm to traverse the links.
The script may take a considerable amount of time to run, especially for higher depth values, as it needs to send HTTP requests and parse HTML for each linked Wikipedia page.
