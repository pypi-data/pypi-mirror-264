from typing import Dict, Set
import urllib
import goshawk.builder.file_reader as fr
import urllib.request 
import urllib.parse
import webbrowser



def dag_to_dot(schema_dag:Dict[str, Set[str]])->str:
    dot_graph = 'digraph G {\n'
    for child_schema in schema_dag:
        dot_graph = dot_graph + f'"{child_schema}";\n'
    for child_schema in schema_dag:
        for parent_schema in schema_dag[child_schema]:
            dot_graph = dot_graph + f'"{parent_schema}" -> "{child_schema}";\n'
    dot_graph = dot_graph + '}'
    return dot_graph

def view_model_tree()->None:
    result = fr.read_files()
    #print("building dag")
    ts = fr.build_schema_dag(result)
    #print(ts)
    dot = dag_to_dot(ts)

    #url = f'https://graphviz.shn.hk/?src={urllib.parse.quote(dot)}&format=svg'
    #urllib.request.urlretrieve(url, "dag.svg") 
    url = 'https://edotor.net/?engine=dot#'+urllib.parse.quote(dot)

    #url='https://quickchart.io/graphviz?graph='+urllib.parse.quote(dot)

    #print(dot)
    body = {
  "graph": dot,
  "layout": "dot",
  "format": "svg"
}

    #r = requests.post('https://quickchart.io/graphviz', json=body)

# r.text is sufficient for SVG. Use `r.raw` for png images
    #svg = r.text
    #with open("dag.svg", "w") as file1:
    #    file1.write(svg)
    
    #webbrowser.open_new('/Users/ericb/Code/goshawk/dag.html')

    webbrowser.open_new(url)


