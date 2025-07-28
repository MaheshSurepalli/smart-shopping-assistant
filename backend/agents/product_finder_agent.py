# agents/product_finder_agent.py
from azure.ai.agents.models import ConnectedAgentTool
from azure.ai.agents import AgentsClient
from azure.identity import DefaultAzureCredential
import os

def create_product_finder_tool(client: AgentsClient) -> ConnectedAgentTool:
    instructions = """
You are a product finder assistant.

When a user describes what they are looking for (e.g., "running shoes under ₹1500"), return a list of 3 relevant products.

Each product should include:
- Product name
- Category or type
- Approximate price
- 1-line reason why it fits the user's need

Be concise and avoid long descriptions.
"""

    agent = client.create_agent(
        model=os.getenv("MODEL_DEPLOYMENT_NAME"),
        name="product_finder_agent",
        instructions=instructions,
    )

    return ConnectedAgentTool(
        id=agent.id,
        name=agent.name,
        description="Finds products based on user input"
    )
