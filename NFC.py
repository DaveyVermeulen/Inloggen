from smartcard.scard import *
import time
import pymysql

hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)

assert hresult==SCARD_S_SUCCESS

hresult, readers = SCardListReaders(hcontext, [])

assert len(readers)>0
reader = readers[0]

def NFCReader():
        try:
            hresult, hcard, dwActiveProtocol = SCardConnect(
                hcontext,
                reader,
                SCARD_SHARE_SHARED,
            SCARD_PROTOCOL_T0 | SCARD_PROTOCOL_T1)
    
            hresult, response = SCardTransmit(hcard,dwActiveProtocol,[0xFF,0xCA,0x00, 0x00, 0x00])
            if response == [99, 0]:
                print("Sorry, probeer opnieuw")
                return
    
            else:
                tag = "".join(str(x) for x in response)
                text=open("tags.txt","w")
                text.write(tag)
                text.close()
                print "tag ontvangen:", (tag)
                        
        except:
            return

while 1:
    NFCReader()
    time.sleep(0.9)
