from ai_engine.openrouter_client import OpenRouterClient

client = OpenRouterClient()

response = client.chat(

    system_prompt="You are a helpful assistant.",

    user_prompt="Say Hello in one sentence."

)

print(response)