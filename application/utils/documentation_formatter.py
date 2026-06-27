from typing import List
from domain.schemas.documentation import Documentation

# Convierte una lista en viñetas Markdown, filtrando elementos vacíos.
def _to_bullets(items: List[str]) -> str:
    clean = [item.strip() for item in items if item.strip()]
    if not clean:
        return "_No se especificaron elementos para esta sección._"
    return "\n".join(f"- {item}" for item in clean)

# Genera el documento final en formato Markdown limpio.
def formatter_document(document: Documentation) -> str:
    sections = [
        f"# {document.project_overview}",
        f"## Problema\n\n{document.problem_statement}",
        f"## Resumen de Requerimientos\n\n{document.requirements_summary}",
        f"## Dominio\n\n{document.domain_summary}",
        "## Arquitectura",
        f"### Visión General\n\n{document.architecture_overview}",
        f"### Patrón Arquitectónico\n\n**{document.architecture_pattern}**",
        f"### Componentes Principales\n\n{_to_bullets(document.key_components)}",
        f"### Stack Tecnológico\n\n{_to_bullets(document.technology_stack)}",
        f"### Decisiones de Diseño\n\n{_to_bullets(document.design_decisions)}",
        f"### Restricciones y Trade-offs\n\n{_to_bullets(document.constraints_and_tradeoffs)}",
        f"### Riesgos y Consideraciones\n\n{_to_bullets(document.risks_and_considerations)}",
        f"## Conclusión\n\n{document.final_summary}",
    ]
    return "\n\n".join(sections)