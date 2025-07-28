# agents/price_negotiator_agent.py
from azure.ai.agents.models import ConnectedAgentTool
from azure.ai.agents import AgentsClient
from azure.identity import DefaultAzureCredential
import os

def create_price_negotiator_tool(client: AgentsClient) -> ConnectedAgentTool:
    instructions = """
You are a price negotiator.

Given a product the user likes, suggest 2 or 3 alternate deals around the same budget.
- Be friendly and persuasive.
- Mention price ranges and make it sound like a human deal.
- Example: "This one's ₹1800, but I found a similar one at ₹1499!"
"""

    agent = client.create_agent(
        model=os.getenv("MODEL_DEPLOYMENT_NAME"),
        name="price_negotiator_agent",
        instructions=instructions,
    )

    return ConnectedAgentTool(
        id=agent.id,
        name=agent.name,
        description="Suggests similar but more affordable product options"
    )
