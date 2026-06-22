import os
import dotenv
import asyncio
from openai import OpenAI
from agents import Agent, Runner, trace, function_tool
from openai.types.responses import ResponseTextDeltaEvent

def setup():
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


@function_tool
def get_food_calories_tool(food_item: str) -> str:
    """
    Get calories for a common food to help with nutrition tracking.

    :param food_item: the food we want to know the calories for i.e. apple
    :return: the calorie information for the given food or an error message
    """
    calorie_data = {
        "apple": "80 calories per medium apple (182g)",
        "banana": "105 calories per medium banana (118g)",
        "broccoli": "25 calories per 1 cup chopped (91g)",
        "almonds": "164 calories per 1oz (28g) or about 23 nuts",
    }

    food_key = food_item.lower()
    if food_key in calorie_data:
        return f"{food_item.title()}: {calorie_data[food_key]}"
    else:
        return f"I dont have the calories for {food_item}"


# an agent needs a runner, which is ASYNC and takes the prompt

async def run_agent():
    # an agent needs a name and instructions (a prompt)
    nutrition_agent = Agent(
        name="Nutrition agent",
        instructions="""
        You are a helpful assistant giving out nutrition advice.
        You give concise answers.
        """,
        tools=[get_food_calories_tool],
    )

    with trace("Simple nutrition agent"):
        result = await Runner.run(nutrition_agent, "How many calories in an apple?")
        print(result)

       




def main():
    setup()
    asyncio.run(run_agent())

main()
