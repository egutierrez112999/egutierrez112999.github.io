import sqlite3
import os 
import psycopg2
import psycopg2.extras
import urllib.parse

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class AdoptionCentersDB:

    def __init__(self):
        urllib.parse.uses_netloc.append("postgres")
        url = urllib.parse.urlparse(os.environ["DATABASE_URL"])

        self.connection = psycopg2.connect(
                cursor_factory=psycopg2.extras.RealDictCursor,
                database=url.path[1:],
                user=url.username,
                password=url.password,
                host=url.hostname,
                port=url.port
        )

        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def createAdoptionCentersTable(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS adoptionscenters (id SERIAL PRIMARY KEY, name TEXT, location TEXT, rating INTEGER, url TEXT, selection TEXT)")
        self.connection.commit()

    def createUsersTable(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, email TEXT, epasswd TEXT, firstname TEXT, lastname TEXT)")
        self.connection.commit()

    #Inputs: None
    #Outputs: List of all the centerss
    def getAllCenters(self):
        self.cursor.execute("SELECT * FROM adoptionscenters")
        return self.cursor.fetchall()

    #INPUTS: which center ID
    #Output: single center
    def getOneCenter(self, centerID):
        data = [centerID]
        self.cursor.execute("SELECT * FROM adoptionscenters WHERE id = %s", data)
        return self.cursor.fetchone()

        #center fields needed, name, location, rating
    #Output: None, Sideeffect only 
    def createCenter(self, name, location, rating, url, selection):
        #order of data array is critical. must match order of question marks
        data = [name, location, rating, url, selection]
        self.cursor.execute("INSERT INTO adoptionscenters (name, location, rating, url, selection) VALUES (%s,%s, %s, %s, %s)",data)
        self.connection.commit()
        return None

    #Output: None, side effect only
    def updateCenter(self, centerID, name, location, rating, url, selection):
        #all fields to update: id, name, everything else
        data = [name, location, rating, url, selection, centerID]
        #Its like taking getonecenter and create center and shove them together.Hybrid.
        self.cursor.execute("UPDATE adoptionscenters SET name = %s, location = %s, rating = %s, url = %s, selection = %s WHERE id = %s",data)
        self.connection.commit()
        return None
        #sql "UPDATE adoptionscenters SET name=?, location=?, rating=? WHERE id = ?"

    #Output: None, Side effect only
    def deleteCenter(self, centerID):
        #need center id to delete it. slmost exactly the same as getOne structurally
        data = [centerID]
        self.cursor.execute("DELETE FROM adoptionscenters WHERE id = %s", data)
        self.connection.commit()
        return None
        #sql: DELETE FROM adoptionscenters WHERE id = ?
    

#---------USER STUFF------------------------------------------------------------


    def findUserByEmail(self, email):
        data = [email]
        self.cursor.execute("SELECT * FROM users WHERE email = %s", data)
        return self.cursor.fetchone()

    def createUser(self, email, epasswd, firstname, lastname):
        #order of data array is critical. must match order of question marks
        data = [email, epasswd, firstname, lastname]
        self.cursor.execute("INSERT INTO users (email, epasswd, firstname, lastname) VALUES (%s, %s, %s, %s)",data)
        self.connection.commit()
        return None

    def deleteUser(self, userID):
        data = [userID]
        self.cursor.execute("DELETE FROM users WHERE id = %s", data)
        self.connection.commit()
        return None
