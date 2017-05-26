import psycopg2

class Database:
    def __init__(self, dbname, user, host, password):
        try:
            print "Connecting to database"

            self.connection = psycopg2.connect("dbname = '" + dbname + "' user = '" + user + "' host = '" + host + "' password = '" + password + "'")
            self.cursor = self.connection.cursor()
        except:
            print "Cannot connect to the database"

    def select_query(self, attributes, table, condition):
        query = "SELECT " + attributes + " FROM " + table
        if condition != "":
            query += " WHERE " + condition
        self.cursor.execute(query)

        rows = self.cursor.fetchall()
        return rows

    def insert_query(self, attributes, values, table):
        query = "INSERT INTO " + table + " (" + attributes + ") VALUES (" + values + ")"
        self.cursor.execute(query)

        self.connection.commit()

    def update_query(self, values_and_atrributes_set, table, condition):
        query = "UPDATE " + table + " SET " + values_and_atrributes_set + " WHERE " + condition
        self.cursor.execute(query)

        self.connection.commit()

    def delete_query(self, table, condition):
        query = "DELETE FROM " + table + " WHERE " + condition
        self.cursor.execute(query)
        self.restart_sequence(table)

        self.connection.commit()

    def restart_sequence(self, table):
        rows = self.select_query("MAX(id)", table, "")
        if rows != []:
            maximum = rows[0][0] + 1

            query = "ALTER SEQUENCE " + table + "_id_seq RESTART WITH " + str(maximum)
            self.cursor.execute(query)

    def disconnect(self):
        print 'Closing database'

        self.connection.close()
