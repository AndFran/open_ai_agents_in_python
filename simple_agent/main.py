import os
import dotenv
import asyncio
from openai import OpenAI
from agents import Agent, Runner, trace
from openai.types.responses import ResponseTextDeltaEvent

dotenv.load_dotenv()


if not os.environ.get('OPENAI_API_KEY'):
    print("""
        No OPENAI_API_KEY environment variable found.
        Set in the OS or create a .env file
    """)

r = OpenAI().responses.create(
    model=os.environ["OPENAI_DEFAULT_MODEL"],
    input="Say: We are good to launch!!"
).output_text

print(r)

print("-"*100)

# an agent needs a name and instructions (a prompt)
nutrition_agent = Agent(
    name="Nutrition agent",
    instructions="""
    You are a helpful assistant giving out nutrition advice.
    You give concise answers.
    """
)

# an agent needs a runner, which is ASYNC

async def run_agent():
    with trace("Simple nutrition agent"):
        result = await Runner.run(nutrition_agent, "How healthy are bananas?")
    print(result)

asyncio.run(run_agent())











