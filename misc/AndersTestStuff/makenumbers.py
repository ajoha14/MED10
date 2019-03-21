from datetime import datetime
from datetime import timedelta

dateformat = '%m_%d-%H_%M_%S.%f'

now = datetime.now()

with open("C:/Users/Anders S. Johansen/Desktop/data.txt") as f:
    data = f.read().splitlines()
    with open("C:/Users/Anders S. Johansen/Desktop/data2.txt",'w+') as o:
        for i in range(len(data)):
            t = now + timedelta(seconds=0.6)
            o.write("{},{}\n".format(data[i], (t.strftime(dateformat))))


