import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from google.adk.tools.mcp_tool import MCPToolset, StreamableHTTPConnectionParams


tools = [MCPToolset(connection_params=StreamableHTTPConnectionParams(
                url="http://localhost:8005/mcp/"                
            )
        )
    ]
root_agent = Agent(
    name="agratas_policy_checking",
    model="gemini-2.0-flash",
    description=(
        "Agent to answer questions wth certain tools"
    ),
    instruction=(
        "You are a helpful agent who can answer user questions about the time and weather in a city."
    ),
    tools=tools,
)