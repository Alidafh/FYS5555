import numpy as np

def readfile(filename):
    # input: "filename.txt", first line in file must be titles
    data = np.loadtxt("{}".format(filename), skiprows = 3)
    return data

data = readfile("datafiles/diff_A.txt")
print (data)
