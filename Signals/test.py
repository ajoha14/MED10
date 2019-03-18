import heartpy as hp
path = 'C:/Users/Anders S. Johansen/Desktop/data.txt'
hrdata = hp.get_data(path)
seglength = 1000
for i in range(len(hrdata)):

working_data, measures = hp.process(hrdata, 100)
hp.plotter(working_data,measures)