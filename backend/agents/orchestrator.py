import os
from azure.ai.agents import AgentsClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

from agents.product_finder_agent import create_product_finder_tool
from agents.price_negotiator_agent import create_price_negotiator_tool
from agents.order_helper_agent import create_order_helper_tool

load_dotenv()

def build_agents_client() -> AgentsClient:
    return AgentsClient(
        endpoint=os.getenv("PROJECT_ENDPOINT"),
        credential=DefaultAzureCredential(exclude_environment_credential=True)
    )

def create_orchestrator(client: AgentsClient):
    pf_tool = create_product_finder_tool(client)
    pn_tool = create_price_negotiator_tool(client)
    oh_tool = create_order_helper_tool(client)

    orchestrator = client.create_agent(
        model=os.getenv("MODEL_DEPLOYMENT_NAME"),
        name="shopping_orchestrator_agent",
        instructions="""
You are a Smart Shopping Assistant.

You can:
- Find products
- Suggest price alternatives
- Help the user place an order

Important Rules:
- DO NOT place an order unless the user explicitly confirms their choice.
- Wait for phrases like "I want this", "I'll buy this", or "place the order".
- Always give the user a chance to choose before invoking the order helper tool.
""",
        tools=[
            pf_tool.definitions[0],
            pn_tool.definitions[0],
            oh_tool.definitions[0]
        ]
    )
    return orchestrator
