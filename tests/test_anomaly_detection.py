from mining.anomaly_detection import AnomalyDetection

detector = AnomalyDetection()

summary = detector.run()

print(summary)

detector.export_results()