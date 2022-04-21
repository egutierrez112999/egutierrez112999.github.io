import base64, os


class SessionStore:

    def __init__(self):
        self.sessions = {} #dict of dcts

    def createSession(self):
        newSessionID = self.generateSessionID()
        self.sessions[newSessionID] = {}
        return newSessionID

    def generateSessionID(self):
        rnum = os.urandom(32)
        rstr = base64.b64encode(rnum).decode("utf-8")
        return rstr

    def loadSessionData(self, sessionID):
        if sessionID in self.sessions:
            return self.sessions[sessionID]
        else:
            return None
