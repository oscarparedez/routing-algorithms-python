import asyncio
from pickle import FALSE
from threading import Thread
import slixmpp
import xmpp
from slixmpp.xmlstream import ET
from slixmpp.exceptions import IqError, IqTimeout
from flooding import *
from aioconsole import *

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

class XMPPChat(slixmpp.ClientXMPP):

    def __init__(self, jid, password, algorithmToUse):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.user = jid
        self.algorithmToUse = algorithmToUse
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.messageNotifications)

    async def messageNotifications(self, event):
        message = event['body']
        message_from = event['from']
        await aprint("%s says: %s" % (message_from, message) )

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
            # Ejecutar algoritmo
            jumps = ""
            distance = ""
            listNodes = ""

            if (self.algorithmToUse == "1"):
                destiny = flooding()
            elif (self.algorithmToUse == "2"):
                destiny = flooding()
            elif (self.algorithmToUse == "3"):
                destiny = flooding()
            else:
                # Default algorithm
                destiny = flooding()

            for i in destiny:
                await aprint('aaaa', i)
                protocolMessage += self.user + ';' + userDestiny + ';' + jumps + ';' + distance + ';' + listNodes + ';' + message
                
                # self.send_message(mto=userDestiny, mbody=protocolMessage, mtype='chat')
                await asyncio.sleep(0.5)

            await self.start(event)
        elif (option == "2"):

            self.disconnect()
            await self.start(event)
        else: 
            await aprint("Try another option!")
            await self.start(event)


print("--- Log In ---")
email = input("Email: ")
password = input("Password: ")

print("1. LSR \n2. Floding \n3. DVR")
algorithmToUse = input("Please type algorithm to use: ")

email = "alvarez@alumchat.fun"
password = "swais"

chat = XMPPChat(email, password, algorithmToUse) 
chat.register_plugin('xep_0030') # Service Discovery
chat.register_plugin('xep_0199') # XMPP Ping
chat.register_plugin("xep_0085")
chat.register_plugin("xep_0133")
chat.register_plugin('xep_0045') # Mulit-User Chat (MUC)

# Connect to the XMPP server and start processing XMPP stanzas.
chat.connect(disable_starttls=True)
chat.process(forever=False)
