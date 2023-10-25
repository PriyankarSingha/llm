import os
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms.openai import OpenAI
import chainlit as cl


openapi_key = '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'

os.environ["OPENAI_API_KEY"] = openapi_key

llm = OpenAI(temperature=0)

template = """Question: {question}

Answer: Let's think step by step."""

@cl.on_chat_start
def main():
    prompt = PromptTemplate(template=template, input_variables=["question"])
    llm_chain = LLMChain(prompt=prompt, llm=llm, verbose=True)

    cl.user_session.set("llm_chain", llm_chain)


@cl.on_message
async def main(message: str):
    llm_chain = cl.user_session.get("llm_chain")

    res = await llm_chain.acall(message, callbacks=[cl.AsyncLangchainCallbackHandler()])

    await cl.Message(content=res["text"]).send()