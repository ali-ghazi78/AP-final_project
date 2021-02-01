import mysql.connector
from mysql.connector import Error
import matplotlib.image as mpimg
import matplotlib.pyplot as plt


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData


def insertImage(database_name, table_name, photo, pass_id, visit_date):
    try:
        print("Inserting BLOB into python_employee table")
        connection = mysql.connector.connect(host='127.0.0.1',
                                             database=database_name,
                                             user='ali',
                                             password='root')

        cursor = connection.cursor()
        sql_insert_blob_query = '''UPDATE  '''+table_name + \
            ''' SET radio_picture = (%s) WHERE pass_id = (%s) AND visit_date = (%s) '''

        empPicture = convertToBinaryData(photo)

        # Convert data into tuple format
        result = cursor.execute(sql_insert_blob_query,
                                (empPicture, pass_id, visit_date))
        connection.commit()
        print("Image and file inserted successfully as a BLOB into python_employee table", result)

    except mysql.connector.Error as error:
        print("Failed inserting BLOB data into MySQL table {}".format(error))

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


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


def loadImage(pass_id, visit_date, show=1):
    print("Reading BLOB data from python_employee table")
    done = False
    try:
        connection = mysql.connector.connect(host='127.0.0.1',
                                             database='patient',
                                             user='ali',
                                             password='root')

        cursor = connection.cursor()
        sql_fetch_blob_query = """SELECT * from patient  where pass_id = %s AND visit_date = %s  LIMIT 1"""

        cursor.execute(sql_fetch_blob_query, (pass_id, visit_date))
        record = cursor.fetchall()
        for i in range(len(record)):
            image = record[i][6]
            print("Storing employee image and bio-data on disk \n")
            done = write_file(image, "output"+str(i)+".jpg", show)

    except mysql.connector.Error as error:
        print("Failed to read BLOB data from MySQL table {}".format(error))

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

    return done


if __name__ == "__main__":
    insertImage("ax.jpg", "1272978699", "1999-06-20 23:59:59")
    loadImage("1272978699", "1999-06-20 23:59:59")
