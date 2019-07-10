'''---------------------------------main script for Factory device Registration in python---------------------------------------------------------------'''

import requests                                                               # import necessarry files
import serial  
import json                                     

URL = "https://devnbpcs.ngxconnect.co.in/api/v1/"        
loginpath='user/login'
getdeviceListpath='product/' 
devregpath="device/factoryregister"
devregparam={}
token=''
choice=''

def openComPort():
  ComPort = serial.Serial('COM17')                                            # open COM17
  ComPort.baudrate = 115200                                                   # set Baud rate to 115200
  ComPort.bytesize = 8                                                        # Number of data bits = 8
  ComPort.parity   = 'N'                                                      # No parity
  ComPort.stopbits = 1                                                        # Number of Stop bits = 1
  ComPort.timeout = 3                                                         # setting timeout for 10 sec's'
  return ComPort

def ComPortClose(ComPort):
  ComPort.close()

def StatusForWriteOntoDevice(reply,ComPort):
    serialNumber = reply['serialNumber']
    #print(serialNumber)
    key = reply['key']
    dev_id = reply['dev_id']
    StringtoWriteOnDevice= "SerialNo:" +  reply["serialNumber"] + ",Key:" + reply["key"] + ",DeviceId:" + reply["dev_id"] + ","
    
    NumberOfBytesWritten = ComPort.write(b'\x1b\x32')
    ReadStatus = ComPort.write(StringtoWriteOnDevice.encode())  

    WriteStatus = ComPort.read(10)                                
    Status = WriteStatus.decode('utf-8')                  
    return Status

def GetProductDescriptor(ComPort):
  NumberOfBytesWritten = ComPort.write(b'\x1b\x33')                           # output given byte string over serial port
  RecievedProductDescriptor = ComPort.read(32)                                # read over the serial port
  ProductDescriptor = RecievedProductDescriptor.decode('utf-8')               # convert byte    
  return ProductDescriptor

def createFactoryDevice(device,productdescriptor):
  headers = {
        'x-access-token':token,
        'Content-Type': 'application/json',
        'Cache-Control': 'no-cache',
       
    }

  devregparam = {
    'productModelName':device['modelNo'],
    'productModelId':device['_id'],
    'factoryFirmwareVersion':"1.1.1",
    'warrantyDuration':device['warranty'],
    'deviceIdentifier':productdescriptor
    }
  r = requests.post(url = URL+devregpath, json = devregparam,headers=headers) 
  return r.text


def getModelList(ReturnedToken):
  headers = {
        'x-access-token':ReturnedToken,
        'Content-Type': 'application/json',
        'Cache-Control': 'no-cache',
       
    }

  r=requests.get(url = URL+getdeviceListpath,headers=headers)
  data = r.json() 
  i=0
  for item in data:
    if item['modelNo']=='NBP100':
      choice=i
    i+=1;  
  return data[choice]  


def login():
  print("enter username")
  username=input()        
  print("enter password")
  password=input()
  PARAMS = {'user':username,'password':password,'usertype':"NGXFuser"}
  try:
    r = requests.post(url = URL+loginpath, json = PARAMS) 
    data = r.json() 
    if r.status_code == 200:
      print('Login Success!')
      global token
      token=data['token']
      return token
    else:
      pass 
  except requests.exceptions.RequestException as e:
      print (e)
      exit()

def serverReplyToObject(serverReply):
    serverReply_dict = json.loads(serverReply)
    serialNumber = serverReply_dict['serialNo']
    print(serialNumber)
    key = serverReply_dict['key']
    dev_id=serverReply_dict['upserted'][0]['_id']

   
    deviceReply={
        'serialNumber':serialNumber,
        'key':key,
        'dev_id':dev_id
    }
    return deviceReply

def main():                                                     #main function starts from here                                               
  ComPort = openComPort()     
  ReturnedToken = login()
  model= getModelList(ReturnedToken)
  print ("This program registers :",model['modelNo'])
  while True:
    answer = input("Do you want to continue yes or no: ")
    if answer == "y":
      productDescriptor = GetProductDescriptor(ComPort)
      if(len(productDescriptor)>0):
          serverReply = createFactoryDevice(model,productDescriptor)
          print(serverReply)
          reply = serverReplyToObject(serverReply)
          ReadStatus = StatusForWriteOntoDevice(reply,ComPort)
          if('SUCCESS' in ReadStatus ):
              print("Device Write Sucessful!")
          else:
              print("Device Write Failed!")
      else:
          print("error communicating with device")
    else:
      break


if __name__== "__main__":
  main()
