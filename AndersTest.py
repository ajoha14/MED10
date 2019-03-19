from Signals.hrProc import hrProcesser

c = hrProcesser(1,10)
l = c.heartRate(['03_19-11_00_39.100000','03_19-11_00_40.100000','03_19-11_00_41.100000','03_19-11_00_42.100000','03_19-11_00_43.100000','03_19-11_00_44.100000'])

for i in range(100):
    print('' + str(c.hrbuffer.data) + '\r')
    c.hrbuffer.add(i)
