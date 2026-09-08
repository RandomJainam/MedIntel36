from mining.sequential_patterns import SequentialPatternMining

miner = SequentialPatternMining()

summary = miner.run()

print(summary)

miner.export_results()