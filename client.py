import asyncio
from pickle import FALSE
from threading import Thread
import slixmpp
import xmpp
from slixmpp.xmlstream import ET
from slixmpp.exceptions import IqError, IqTimeout

class XMPPChat(slixmpp.ClientXMPP):

    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.user = jid
        self.add_event_handler("session_start", self.start)
    
    async def start(self, event):

        print("Welcome! ", self.user)
        await self.get_roster()

        print("1. Send Private Message \n2. Log Out")
        option = input("")
        if option == "1":
            userDestiny = input("Type email to send message: ")
            message = input("Message: ")

            protocolMessage = ""
            # Ejecutar algoritmo
            jumps = ""
            distance = ""
            listNodes = ""

            protocolMessage += self.user + ';' + userDestiny + ';' + jumps + ';' + distance + ';' + listNodes + message
            
            self.send_message(mto=userDestiny, mbody=protocolMessage, mtype='chat')
            await asyncio.sleep(0.5)

            await self.start(event)
        elif (option == "2"):

            self.disconnect()
            await self.start(event)
        else: 
            print("Try another option!")
            await self.start(event)


print("--- Log In ---")
email = input("Email: ")
password = input("Password: ")

email = "alvarez@alumchat.fun"
password = "swais"

chat = XMPPChat(email, password) 
chat.register_plugin('xep_0030') # Service Discovery
chat.register_plugin('xep_0199') # XMPP Ping
chat.register_plugin("xep_0085")
chat.register_plugin("xep_0133")
chat.register_plugin('xep_0045') # Mulit-User Chat (MUC)

# Connect to the XMPP server and start processing XMPP stanzas.
chat.connect(disable_starttls=True)
chat.process(forever=False)
