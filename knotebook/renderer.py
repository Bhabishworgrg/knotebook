from typing import Any
from pathlib import Path
from math import ceil, sqrt
from markdown import markdown
from itertools import product
from importlib.resources import files
from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import TemplateNotFound


class Renderer:
    def __init__(self):
        self.__environment: Environment = Environment(
            loader=FileSystemLoader(str(files('knotebook').joinpath('templates')))
        )
        self.__pages_path: Path = Path('pages').resolve()


    def __render_with_context(self, file: str, **context: Any) -> str:
        try:
            template = self.__environment.get_template(file)
        except TemplateNotFound:
            raise TemplateNotFound(f'Template file {file} not found.') from None
        return template.render(context)


    def render_home(self):
        pages: list[dict[str, Any]] = [
            {
                'name': path.stem,
                'parent': path.parent.stem if path.parent != self.__pages_path else None,
                'depth': len(path.relative_to(self.__pages_path).parts)
            }
            for path in self.__pages_path.rglob('*')
        ]

        grid_size: int = ceil(sqrt(len(pages)))
        coordinates: list[tuple[int, int]] = list(product(range(grid_size), range(grid_size)))

        nodes: list[dict[str, Any]] = []
        edges: list[dict[str, str]] = []

        for (x, y), page in zip(coordinates, pages):
            page_name: str = page['name']
            page_parent: str = page['parent']

            nodes.append({
                'label': page_name,
                'x': x,
                'y': y,
                'size': 40 / page['depth']
            })

            if page_parent:
                edges.append({
                    'source': page_name,
                    'target': page_parent
                })

        return self.__render_with_context(
            file='index.html',
            title='Knotebook',
            nodes=nodes,
            edges=edges
        )


    def render_page(self, page: str) -> str:
        with open(self.__pages_path.joinpath(f'{page}.md'), 'r', encoding='utf-8') as file:
            text = file.read()
        html_content = markdown(text)

        return self.__render_with_context(
            file='page.html',
            title=page,
            content=html_content
        )


    def render_exact(self, file: str) -> str:
        return self.__render_with_context(file)
