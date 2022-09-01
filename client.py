import asyncio
from pickle import FALSE
from threading import Thread
from unicodedata import name
import slixmpp
import xmpp
import json
from slixmpp.xmlstream import ET
from slixmpp.exceptions import IqError, IqTimeout
from flooding import *
from aioconsole import *

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

dicLetters = {
    "A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8,
    "J": 9, "K": 10, "L": 11, "M": 12, "N": 13, "O": 14, "P": 15, "Q": 16, "R": 17,
    "S": 18, "T": 19, "U": 20, "V": 21, "W": 22, "X": 23, "Y": 24, "Z": 25
  }
class XMPPChat(slixmpp.ClientXMPP):

    def __init__(self, jid, password, algorithmToUse):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.user = jid
        self.algorithmToUse = algorithmToUse
        self.firstTimeFilling = True
        self.G = nx.Graph()
        self.totalNodes = 0
        self.listNodes = {}
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.messageNotifications)

    async def messageNotifications(self, event):
        message = event['body']

        params = message.split(';')

        # If we are the destiny we print message
        if (self.user == params[1]):
            message_from = event['from']
            await aprint("%s says: %s" % (message_from, params[5]))
        else:
            jumps = str(int(params[2]) + 1)
            params[2] = jumps

            listNodes = json.loads(params[4].replace("'", "\""))

            nextNode = list(listNodes.values())[int(jumps)]

            newMessage = ';'.join(params)

            self.send_message(mto=nextNode, mbody=newMessage, mtype='chat')
            await asyncio.sleep(0.5)

    async def start(self, event):
        self.send_presence('chat', 'a')

        await aprint("Welcome! ", self.user)
        await self.get_roster()

        await aprint("1. Send Private Message \n2. Log Out")
        option = await ainput("")
        if option == "1":
            userDestiny = await ainput("Type email to send message: ")
            message = await ainput("Message: ")
            protocolMessage = ""

            if (self.algorithmToUse == "1"):
                # Filling email values of nodes just one time
                if (self.firstTimeFilling):
                    self.firstTimeFilling = False
                    namesNodes = []
                    
                    with open("topologia.txt") as f:
                        json_data = json.load(f)

                        for i in json_data['config']:
                            self.totalNodes+=1
                            head = i
                            namesNodes.append(head)
                            for neighbor in json_data['config'][i]:
                                self.G.add_edge(head, neighbor, weight = 1)

                    nodes = namesNodes[1:]
                    
                    for i in range(len(nodes)):
                        email = await ainput("For the node %s please enter a valid email " % (nodes[i]))
                        self.listNodes[nodes[i]] = email
                nodeToSend = list(self.listNodes.keys())[list(self.listNodes.values()).index(userDestiny)]
                destiny = flooding(nodeToSend, self.totalNodes, self.G)
            elif (self.algorithmToUse == "2"):

                G = [] # adjacency matrix
                userDestiny = await ainput("Type email to send message: ")
                message = await ainput("Message: ")
                protocolMessage = ""

                with open("topologia.txt") as f:
                    json_data = json.load(f)
                    sizeMatrix = len(json_data['config'])

                    for i in json_data['config']:
                        lst = [999] * sizeMatrix
                        for neighbor in json_data['config'][i]:
                            lst[dicLetters[neighbor]] = 1
                        G.append(lst)

                # destiny = lsrAlgorithm(self.user, userDestiny, sizeMatrix, G)
            elif (self.algorithmToUse == "3"):
                destiny = flooding()
            else:
                # Default algorithm
                destiny = flooding()

            jumps = "0"
            distance = str(len(destiny))
            firstNodeEmail = list(self.listNodes.values())[0]
            listNodes = str(self.listNodes)

            protocolMessage = self.user + ';' + userDestiny + ';' + jumps + ';' + distance + ';' + listNodes + ';' + message

            self.send_message(mto=firstNodeEmail, mbody=protocolMessage, mtype='chat')
            await asyncio.sleep(0.5)

            await self.start(event)
        elif (option == "2"):
            await aprint("See you!")
            self.disconnect()
        else: 
            await aprint("Try another option!")
            await self.start(event)


print("--- Log In ---")
email = input("Email: ")
password = input("Password: ")

print("1. Floding \n2. LSR \n3. DVR")
algorithmToUse = input("Please type algorithm to use: ")

# email = "alvarez@alumchat.fun"
# password = "swais"

chat = XMPPChat(email, password, algorithmToUse) 
chat.register_plugin('xep_0030') # Service Discovery
chat.register_plugin('xep_0199') # XMPP Ping
chat.register_plugin("xep_0085")
chat.register_plugin("xep_0133")
chat.register_plugin('xep_0045') # Mulit-User Chat (MUC)

# Connect to the XMPP server and start processing XMPP stanzas.
chat.connect(disable_starttls=True)
chat.process(forever=False)
