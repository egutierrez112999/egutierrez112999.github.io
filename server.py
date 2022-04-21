from http.server import BaseHTTPRequestHandler, HTTPServer
from http import cookies
import sys
#for threading
from socketserver import ThreadingMixIn
#db import
import sqlite3
from passlib.hash import bcrypt
import json
from centers import AdoptionCentersDB
from urllib.parse import urlparse, parse_qs
from sessions import SessionStore 

SESSION_STORE = SessionStore()

class MyRequestHandler(BaseHTTPRequestHandler):


    def end_headers(self):
        self.sendCookie()
        self.send_header("Access-Control-Allow-Origin", self.headers["Origin"])
        self.send_header("Access-Control-Allow-Credentials","true")
        super().end_headers()

    def loadCookie(self):
        if "Cookie" in self.headers:
            self.cookie = cookies.SimpleCookie(self.headers["Cookie"])
        else:
            #create an empty cookie object in case there is no cookie data to load
            self.cookie = cookies.SimpleCookie()

    def sendCookie(self):
        for morsel in self.cookie.values():
            #uncomment these below when testing with chrome
            morsel["samesite"] = "None"
            morsel["secure"] = True
            self.send_header("Set-Cookie", morsel.OutputString())        

    def loadSessionData(self):
        self.loadCookie()
        #check for existing session ID cookie
        if "sessionID" in self.cookie:
            sessionID = self.cookie["sessionID"].value
            self.sessionData = SESSION_STORE.loadSessionData(sessionID)
            #check if session was loaded
            if self.sessionData == None:
                #create new session
                sessionID = SESSION_STORE.createSession()
                self.sessionData = SESSION_STORE.loadSessionData(sessionID)
                #set a new session ID cookie
                self.cookie["sessionID"] = sessionID
        else:
            print("Creating new session")
            #create new session
            sessionID = SESSION_STORE.createSession()
            self.sessionData = SESSION_STORE.loadSessionData(sessionID)
            #set a new session ID cookie
            self.cookie["sessionID"] = sessionID
        print("MY SESSION DATA", self.sessionData)
        print(self.cookie["sessionID"])



    #handle any get request
    def do_GET(self):
        self.loadSessionData() 
        print("the request path is: ", self.path)
        pathlist = self.path.split("/")
        if len(pathlist) > 2:
            collection_name = pathlist[1]
            member_id = pathlist[2]
        else:
            collection_name = pathlist[1]
            member_id = None

        if collection_name == "adoptioncenters":
            if member_id == None:
                self.handleListDogs()
            else:
                self.handleRetrieveDogs(member_id)
        else:
            self.handleNotFound()
         
        
    def do_POST(self):
        self.loadSessionData() 
        if self.path == "/adoptioncenters":
            self.handleCreateDogs()
        elif self.path == "/users":
            self.handleCreateUser()
        elif self.path == "/sessions":
            self.handleCreateSession()
            pass
        else:
            self.handleNotFound()


    def do_PUT(self):
        self.loadSessionData() 
        pathlist = self.path.split("/")
        actualID = pathlist[2]
        if pathlist[1] == "adoptioncenters":
            if actualID:
                self.handleUpdateDogs()
            else:
                self.handleNotFound()
        else:
            self.handleNotFound()
        


    def do_DELETE(self):
        self.loadSessionData() 
        pathlist = self.path.split("/")
        actualID = pathlist[2]
        if pathlist[1] == "adoptioncenters":
            if actualID:
                self.handleDeleteDogs(actualID)
            else:
                self.handleNotFound()
        else:
            self.handleNotFound()
        
    def do_OPTIONS(self):
        self.loadSessionData() 
        self.send_response(200)
        self.send_header("Access-Control-Allow-Methods","POST, GET, DELETE, PUT, OPTIONS")
        self.send_header("Access-Control-Allow-Headers","Content-Type")
        self.end_headers()
         
    def handleCreateSession(self):
        db = AdoptionCentersDB()
        length = int(self.headers["Content-Length"])
        request_body = self.rfile.read(length).decode("utf-8")
        print("The raw request body:", request_body)
        parsed_body = parse_qs(request_body)
        print("The parsed Body: ",parsed_body)

        #GIVEN: an attempted email and password from the client
        email = parsed_body["email"][0]
        password = parsed_body["password"][0]
        #step 1: find a user in db with that email
        user = db.findUserByEmail(email)
        #if valid:
        if user != None:
            #step 2: compare passwords
            verified = bcrypt.verify(password, user["epasswd"])
            print(verified)
            if verified:
                self.send_response(201)
                #ToDo: remember the users authenticated state
                self.sessionData["userID"] = user["id"]
                self.end_headers()
            else:
                self.handle401()
        else:
            self.handle401()

 
    def handleNotFound(self):
        self.send_response(404)
        self.send_header("Content-Type","text/plain")
        self.end_headers()
        self.wfile.write(bytes("Path not found","utf-8"))

    def handle401(self):
        self.send_response(401)
        self.send_header("Content-Type","text/plain")
        self.end_headers()
        self.wfile.write(bytes("Request lacks proper authentication credentials","utf-8"))

    def handleListDogs(self):
        if 'userID' not in self.sessionData:
            self.handle401()
            return
        db = AdoptionCentersDB()
        allrecords = db.getAllCenters()
        #send status code
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        #write to "wfile" response body
        self.wfile.write(bytes(json.dumps(allrecords), "utf-8"))


    def handleRetrieveDogs(self, member_id):
        if 'userID' not in self.sessionData:
            self.handle401()
            return
        db = AdoptionCentersDB()
        dogrecord = db.getOneCenter(member_id)
        #send status code
        if dogrecord != None:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(dogrecord), "utf-8"))
        else:
            self.handleNotFound()


    def handleCreateDogs(self):
        if 'userID' not in self.sessionData:
            self.handle401()
            return
        db = AdoptionCentersDB()
        #capture input (restaurant name) from client request 
        #Step 1) read content length from request header
        length = int(self.headers["Content-Length"])
        #Step 2) read from "rfile" request body
        request_body = self.rfile.read(length).decode("utf-8")
        print("The raw request body:", request_body)
        #Step 3) parse the urlencoded request body
        parsed_body = parse_qs(request_body)
        print("The parsed Body: ",parsed_body)
        # Step 4) append new restaurant to list above
        center_name = parsed_body["name"][0] #the key "name" is specified by client
        center_location = parsed_body["location"][0]
        center_rating = parsed_body["rating"][0]
        center_url = parsed_body["url"][0]
        center_selection = parsed_body["selection"][0]
        #RESTAURANTS.append(restaurant_name)
        db.createCenter(center_name, center_location, center_rating, center_url, center_selection)
        #respond with success(201)
        self.send_response(201)
        self.end_headers()


    def handleDeleteDogs(self, center_id):        
        if 'userID' not in self.sessionData:
            self.handle401()
            return
        db = AdoptionCentersDB()
        record = db.getOneCenter(center_id)
        if record != None:
            db.deleteCenter(center_id)
            self.send_response(200)
            self.end_headers()
        else:
            self.handleNotFound()



    def handleUpdateDogs(self):        
        if 'userID' not in self.sessionData:
            self.handle401()
            return
        db = AdoptionCentersDB()
        length = int(self.headers["Content-Length"])
        request_body = self.rfile.read(length).decode("utf-8")
        print("The raw request body:", request_body)
        parsed_body = parse_qs(request_body)
        print("The parsed Body: ",parsed_body)
        center_id = parsed_body["id"][0]
        center_name = parsed_body["name"][0] 
        center_location = parsed_body["location"][0]
        center_rating = parsed_body["rating"][0]
        center_url = parsed_body["url"][0]
        center_selection = parsed_body["selection"][0]
        record = db.getOneCenter(center_id)
        if record != None:
            db.updateCenter(center_id, center_name, center_location, center_rating, center_url, center_selection)
            self.send_response(200)
            self.end_headers()
        else:
            self.handleNotFound()


    def handleCreateUser(self):
        db = AdoptionCentersDB()
        length = int(self.headers["Content-Length"])
        request_body = self.rfile.read(length).decode("utf-8")
        print("The raw request body:", request_body)
        parsed_body = parse_qs(request_body)
        print("The parsed Body: ",parsed_body)

        user_email = parsed_body["email"][0]
        user_unencryptedpassword = parsed_body["password"][0]
        user_firstname = parsed_body["firstname"][0]
        user_lastname = parsed_body["lastname"][0]

        if db.findUserByEmail(user_email) == None:
            encrypted_password = bcrypt.hash(user_unencryptedpassword)
            db.createUser(user_email, encrypted_password, user_firstname, user_lastname)
            self.send_response(201)
            self.end_headers()
            return
        else:
            self.send_response(422)
            self.end_headers()
            print("User already exists")



#query string, urlencoded format
class threadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass #no implementation

def run():
    db = AdoptionCentersDB()
    db.createAdoptionCentersTable()
    db.createUsersTable()
    db = None

    port = 8080
    if len(sys.argv) > 1:
        port = int(sys.argv[1])

    listen = ("0.0.0.0", port)
    server = threadedHTTPServer(listen, MyRequestHandler)#do not instantiatiate this class

    print("Server listening on", "{}:{}".format(*listen))
    server.serve_forever()

run()
