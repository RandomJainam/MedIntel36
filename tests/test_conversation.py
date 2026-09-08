from ai_engine.conversation_manager import ConversationManager

conversation = ConversationManager()
print(conversation.get_context())
print(conversation.get_context().keys())


conversation.update_context(
    selected_dataset="finance",
    dataset_confidence=0.98
)

conversation.update_context(
    metrics=["total_amount"]
)

conversation.update_context(
    dimensions=["department_name"],
    group_by=["department_name"]
)

conversation.update_context(
    filters=[
        {
            "column": "department_name",
            "operator": "=",
            "value": "Cardiology"
        }
    ]
)

print(conversation.get_context())

conversation.reset()

print(conversation.get_context())   