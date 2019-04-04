class Node:

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.state = None
        self.state_data = None
        self.isAlive = False

    def getIp(self):
        return self.ip

    def setIp(self, ip):
        self.ip = ip

    def setState(self, state):
        self.state = state

    def getPort(self):
        return self.port

    def setPort(self, port):
        self.port = port

    def getHostAndPort(self):
        return {"ip": self.ip, "port": self.port}

    def getIsAlive(self):
        return self.isAlive

    def setIsAlive(self, boolean):
        self.isAlive = boolean
