# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['blar_graph', 'blar_graph.graph_construction', 'blar_graph.utils']

package_data = \
{'': ['*']}

install_requires = \
['langchain-openai>=0.1.1,<0.2.0',
 'langchain>=0.1.13,<0.2.0',
 'llama-index-packs-code-hierarchy>=0.1.1,<0.2.0',
 'llama-index>=0.10.20,<0.11.0',
 'neo4j>=5.18.0,<6.0.0',
 'python-dotenv>=1.0.1,<2.0.0',
 'tree-sitter-languages>=1.10.2,<2.0.0']

setup_kwargs = {
    'name': 'blar-graph',
    'version': '0.0.4',
    'description': 'Llm agent to search within a graph',
    'long_description': '# code-base-agent',
    'author': 'Benjamín Errazuriz',
    'author_email': 'benjamin@blar.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://blar.io',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
