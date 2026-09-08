from mining.association_rules import AssociationRules

miner = AssociationRules()
rules = miner.run()
print(rules.head(20))