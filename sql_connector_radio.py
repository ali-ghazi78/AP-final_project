import mysql.connector


def insert_into_table(first_name, last_name, father_name, pass_id, visit_date, radio_or_dentist_visit, radio_picture=None, dentist_prescription=None):
    mydb = mysql.connector.connect(user='ali', password='root',
                                   host='127.0.0.1', database="patient")
    mycursor = mydb.cursor()
    insert_command = "INSERT INTO patient(first_name, last_name, father_name, pass_id, visit_date, radio_or_dentist_visit, radio_picture, dentist_prescription) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"

    mycursor.execute(insert_command, (first_name, last_name, father_name, pass_id,
                                      visit_date, radio_or_dentist_visit, radio_picture, dentist_prescription))
    mydb.commit()


def get_all_records():
    mydb = mysql.connector.connect(user='ali', password='root',
                                   host='127.0.0.1', database="patient")
    mycursor = mydb.cursor()
    columns = "first_name, last_name, father_name, pass_id, visit_date"
    insert_command = "SELECT "+columns + " FROM patient "

    mycursor.execute(insert_command)
    records = mycursor.fetchall()

    return records


def check_if_exist(pass_id, visit_date):
    mydb = mysql.connector.connect(user='ali', password='root',
                                   host='127.0.0.1', database="patient")
    mycursor = mydb.cursor()
    columns = "pass_id, visit_date"
    insert_command = "SELECT "+columns + \
        " FROM patient  where pass_id = %s AND visit_date = %s"
    mycursor.execute(insert_command, (pass_id, visit_date))
    records = mycursor.fetchall()
    if(records):
        return True
    return False


def search_for_record(kargs):
    mydb = mysql.connector.connect(user='ali', password='root',
                                   host='127.0.0.1', database="patient")
    mycursor = mydb.cursor()

    columns = "first_name, last_name, father_name, pass_id, visit_date"
    insert_value = []
    insert_command = "SELECT "+columns + " FROM patient  where "
    for key, value in kargs.items():
        if(key == "visit_date"):
            insert_command += key + " >= %s"
        else:
            insert_command += key + " REGEXP %s"
        insert_value.append(value)
        insert_command += "AND "

    insert_command = insert_command[0:-4]

    mycursor.execute(insert_command, insert_value)

    return mycursor.fetchall()


def search_for_booking(date):
    mydb = mysql.connector.connect(user='ali', password='root',
                                   host='127.0.0.1', database="patient")
    mycursor = mydb.cursor()
    columns = "first_name, last_name, father_name, pass_id, visit_date"
    insert_value = (date+"%",)
    insert_command = "SELECT " + columns+"  FROM patient  where visit_date like %s "
    mycursor.execute(insert_command, insert_value)

    return mycursor.fetchall()

def remove_from_table(kargs):
    mydb = mysql.connector.connect(user='ali', password='root',
                                   host='127.0.0.1', database="patient")
    mycursor = mydb.cursor()

    insert_value = []
    insert_command = "DELETE FROM patient where "
    for key, value in kargs.items():
        insert_command += key + " = %s"
        insert_value.append(value)
        insert_command += "AND "
    insert_command = insert_command[0:-4]
    mycursor.execute(insert_command, insert_value)


if __name__ == "__main__":
    pass
    # insert_into_table("ali", "ghazi", "m", "12", "1999-06-20 23:59:59", 0,)

    # re = get_all_records()
    # for i in re:
    #     print(i)

    # reg = {"visit_date" : "1999-06-20 23:59:59"}
    # re  = search_for_record(reg)
    # for i in re:
    #         print(i)
