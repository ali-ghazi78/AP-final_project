import mysql.connector
from mysql.connector import Error
import matplotlib.image as mpimg
import matplotlib.pyplot as plt


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

def write_file(data, filename, show=1):
    # Convert binary data to proper format and write it on Hard Disk
    if(data != None):
        with open(filename, 'wb') as file:
            file.write(data)
        if(show):
            plt.imshow(mpimg.imread(filename))
            plt.axis('off')
            plt.show()
    elif(show):
        plt.imshow(mpimg.imread("teeth.jpg"))
        plt.show()
        return False

    return True

