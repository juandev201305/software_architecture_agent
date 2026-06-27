from langchain_core.prompts import PromptTemplate
def build_chain(llm, prompt, schema):
    final_llm = llm.with_structured_output(schema)
    final_prompt = PromptTemplate.from_template(
        prompt
    )
    chain = (
        final_prompt
        | final_llm
    )
    return chain