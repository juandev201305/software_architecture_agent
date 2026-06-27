from application.services.documentation_service import generator_documentation

# Generar la documentación final del sistema
async def run_documentation(state: dict, llm):
    documentation = await generator_documentation(state["requirements"], state["pre-architecture"], state["architecture"], llm)
    return documentation