from alpha_vantage.sectorperformance import SectorPerformances
import matplotlib.pyplot as plt

sp = SectorPerformances(key='7WPQAG2NRC8PLFIZ', output_format='pandas')
data, meta_data = sp.get_sector()
print(data['Rank D: Month Performance']["Consumer Discretionary"]) # 1 month
print(data['Rank E: Month Performance']["Consumer Discretionary"]) # 3 month
print(data['Rank F: Year-to-Date (YTD) Performance']["Consumer Discretionary"]) # ytd
print(data['Rank G: Year Performance']["Consumer Discretionary"]) # 1 year
