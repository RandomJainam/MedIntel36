from mining.clustering import PatientClustering

cluster = PatientClustering()

summary = cluster.run()

print(summary)

cluster.export_results()