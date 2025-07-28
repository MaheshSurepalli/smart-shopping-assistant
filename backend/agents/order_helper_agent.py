# agents/order_helper_agent.py
from azure.ai.agents.models import ConnectedAgentTool
from azure.ai.agents import AgentsClient
import os

def create_order_helper_tool(client: AgentsClient) -> ConnectedAgentTool:
    instructions = """
You are an order helper agent.

When a user indicates they want to buy a product, do the following:
1. Confirm the product name and price.
2. Ask for the user's name and delivery location.
3. Summarize the order and confirm before submitting.

Respond as a helpful assistant, and simulate the flow — no actual order is placed.
"""

    agent = client.create_agent(
        model=os.getenv("MODEL_DEPLOYMENT_NAME"),
        name="order_helper_agent",
        instructions=instructions,
    )

    return ConnectedAgentTool(
        id=agent.id,
        name=agent.name,
        description="Helps users place an order by collecting required info and confirming."
    )
