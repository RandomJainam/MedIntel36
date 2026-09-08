from mining.timeseries import TimeSeriesAnalysis

ts = TimeSeriesAnalysis()

summary = ts.run()

print(summary)

ts.export_results()