import pickle

motors = [0]*len(range(8))

for i in range(8):
    motors[i] = i%2

print(motors)

file_Name = "testfile"
# open the file for writing
with open(file_Name,'wb') as fileObject:
    # this writes the object a to the
    # file named 'testfile'
    pickle.dump(motors,fileObject)   

with open(file_Name,'r') as fileObject:
    # load the object from the file into var b
    b = pickle.load(fileObject)  

print(b)