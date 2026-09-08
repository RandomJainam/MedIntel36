import pandas as pd

from ai_engine.finance_agent import FinanceAgent

finance = pd.read_csv("data/gold/gold_finance_analytics.csv")

finance_agent = FinanceAgent(finance)

print(finance_agent.get_summary())

print(finance_agent.answer("total revenue"))

print(finance_agent.answer("average billing"))

print(finance_agent.answer("highest revenue department"))

print(finance_agent.answer("insurance"))