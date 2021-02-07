import mysql.connector


class SqlConnector():
    def __init__(self,user_name,password,host_name,db_name):
        self.user_name = user_name
        self.password = password
        self.my_host = host_name
        self.db_name = db_name

    def insert_into_table(self,database_name, table_name, kargs):
        mydb = mysql.connector.connect(user=self.user_name, password=self.password,
                                    host=self.my_host, database=self.db_name)
        mycursor = mydb.cursor()
        insert_value = []
        place = "( "
        insert_command = "INSERT INTO "+table_name + " ( "

        for key, value in kargs.items():
            insert_command += key + " ,"
            insert_value.append(value)
            place += " %s, "

        insert_command = insert_command[0:-1]
        place = place[0:-2] + ")"

        insert_command = insert_command + " ) VALUES " + place
        mycursor.execute(insert_command, insert_value)
        mydb.commit()


    def check_if_exist(self,database_name, table_name, kargs):
        mydb = mysql.connector.connect(user=self.user_name, password=self.password,
                                    host=self.my_host, database=self.db_name)
        mycursor = mydb.cursor()

        insert_value = []
        insert_command = "SELECT * FROM "+table_name + " WHERE  "

        for key, value in kargs.items():
            insert_command += key + " = %s"
            insert_value.append(value)
            insert_command += " AND "

        insert_command = insert_command[0:-4]

        mycursor.execute(insert_command, insert_value)

        records = mycursor.fetchall()

        if(records):
            return True
        return False


    def edit_record(self,database_name, table_name, kargs_property, kargs_set):
        mydb = mysql.connector.connect(user=self.user_name, password=self.password,
                                    host=self.my_host, database=self.db_name)
        mycursor = mydb.cursor()
        insert_value = []
        insert_command = "UPDATE "+table_name + " set "

        for key, value in kargs_set.items():
            insert_command += key + " = (%s) ,"
            insert_value.append(value)

        insert_command = insert_command[0:-1]
        insert_command += " where "
        for key, value in kargs_property.items():
            insert_command += key + " = (%s) AND "
            insert_value.append(value)

        insert_command = insert_command[0:-4]

        mycursor.execute(insert_command, insert_value)
        mydb.commit()


    def search_with_join(self,database_name, from_tables, conditions, colummns,sort_col=None):
        mydb = mysql.connector.connect(user=self.user_name, password=self.password,
                                    host=self.my_host, database=self.db_name)
        mycursor = mydb.cursor()

        col = " "
        for i in colummns:
            col += i+", "
        col = col[:-2]

        join = "SELECT " + col + " FROM " + from_tables[0] + " "
        for i in range(1, len(from_tables)):
            join += "JOIN " + from_tables[i] + " on ( " + conditions[i-1] + " ) "
        
        
        if sort_col == None:
            sort_col = colummns[0]

        join += "ORDER BY " + sort_col + " asc "


        mycursor.execute(join)
        return mycursor.fetchall()


    def search_with_join_where(self,database_name, from_tables, conditions, colummns, where_kargs,sort_col=None):
        mydb = mysql.connector.connect(user=self.user_name, password=self.password,
                                    host=self.my_host, database=self.db_name)
        mycursor = mydb.cursor()

        insert_value = []
        col = " "

        for i in colummns:
            col += i+", "
        col = col[:-2]

        join = "SELECT " + col + " FROM " + from_tables[0] + " "
        for i in range(1, len(from_tables)):
            join += "JOIN " + from_tables[i] + " on ( " + conditions[i-1] + " ) "

        if(len(where_kargs)>=1):
            join += " where "
            for key, value in where_kargs.items():
                join += key + " REGEXP %s "
                insert_value.append(value)
                join += "AND "
            join = join[0:-4]

        if sort_col == None:
            sort_col = colummns[0]

        join += "ORDER BY " + sort_col + " asc "

        mycursor.execute(join, insert_value)
        return mycursor.fetchall()


    def search_for_record(self,database_name, table_name, kargs, colummns=None):
        mydb = mysql.connector.connect(user=self.user_name, password=self.password,
                                    host=self.my_host, database=self.db_name)
        mycursor = mydb.cursor()

        insert_value = []
        col = " "
        if colummns == None:
            col = " * "
        else:
            for i in colummns:
                col += i + ", "
            col = col[0:-2]

        insert_command = "SELECT " + col + " FROM " + table_name + " where "
        for key, value in kargs.items():
            if(key == "visit_date"):
                insert_command += key + " >= %s"
            else:
                insert_command += key + " REGEXP %s"
            insert_value.append(value)
            insert_command += " AND "

        insert_command = insert_command[0:-4]

        mycursor.execute(insert_command, insert_value)

        return mycursor.fetchall()



    def search_for_record_exact(self,database_name, table_name, kargs, colummns=None):
        mydb = mysql.connector.connect(user=self.user_name, password=self.password,
                                    host=self.my_host, database=self.db_name)
        mycursor = mydb.cursor()

        insert_value = []
        col = " "
        if colummns == None:
            col = " * "
        else:
            for i in colummns:
                col += i + ", "
            col = col[0:-2]

        insert_command = "SELECT " + col + " FROM " + table_name + " where "
        for key, value in kargs.items():
            insert_command += key + " = %s"
            insert_value.append(value)
            insert_command += " AND "

        insert_command = insert_command[0:-4]


        mycursor.execute(insert_command, insert_value)

        return mycursor.fetchall()

    # def get_all_records(self):
    #     mydb = mysql.connector.connect(user=self.user_name, password=self.password,
    #                                 host=self.my_host, database=self.db_name)
    #     mycursor = mydb.cursor()
    #     columns = "first_name, last_name, father_name, pass_id, visit_date"
    #     insert_command = "SELECT "+columns + " FROM patient_info "

    #     mycursor.execute(insert_command)
    #     records = mycursor.fetchall()

    #     return records


    # def search_for_booking(self,date):
    #     mydb = mysql.connector.connect(user=self.user_name, password=self.password,
    #                                 host=self.my_host, database="patient")
    #     mycursor = mydb.cursor()
    #     columns = "first_name, last_name, father_name, pass_id, visit_date"
    #     insert_value = (date+"%",)
    #     insert_command = "SELECT " + columns+"  FROM patient  where visit_date like %s "
    #     mycursor.execute(insert_command, insert_value)

    #     return mycursor.fetchall()


    def remove_from_table(self,database_name, table_name, kargs):
        mydb = mysql.connector.connect(user=self.user_name, password=self.password,
                                    host=self.my_host, database=self.db_name)
        mycursor = mydb.cursor()

        insert_value = []
        insert_command = "DELETE FROM " + table_name + " where "
        for key, value in kargs.items():
            insert_command += key + " = (%s) "
            insert_value.append(value)
            insert_command += "AND "
        insert_command = insert_command[0:-4]
        mycursor.execute(insert_command, insert_value)
        mydb.commit()


if __name__ == "__main__":
    pass
    