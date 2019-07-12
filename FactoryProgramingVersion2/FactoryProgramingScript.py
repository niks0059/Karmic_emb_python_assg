'''------------------------------------------main script for Factory device Registration using python----------------------------------------------------'''

import requests                                                                           #   import necessarry files
import serial  
import json 
import getpass                                    
import serial.tools.list_ports


URL = "https://devnbpcs.ngxconnect.co.in/api/v1/"                                         #   providing necessary Url's, variables and paths    
loginpath='user/login'
getdeviceListpath='product/' 
devregpath="device/factoryregister"
devregparam={}
token=''
choice=''




# Function for Internet connection Check
def checkInternetConnection():                                                            
  url='https://www.ngxtechnologies.com/'
  timeout=5
  try:
    _ = requests.get(url, timeout=timeout)
    return True
  except requests.ConnectionError:
    print("Check Your Internet Connection!")
    exit()
    return False






# Function for COM opening and its related Settings
def openComPort():                                                              
  
  try:
    
    ports = serial.tools.list_ports.comports(include_links=False)
    for port in ports :
      print(port.device)
    print("enter your port number")
    portNumber = input()
    port=int(portNumber)
    
    if port > 0 and port <= 256:                                                           #   checking valid Max and Min port Number for Windows
      ComportNumber=str(port)
      COM = 'COM'+ComportNumber
    else:
      print("Please,Enter Valid Port Number!")
      exit()
    
    ComPort = serial.Serial(COM)                                                           #   open COM
    ComPort.baudrate = 115200                                                              #   Baud rate set to 115200
    ComPort.bytesize = 8                                                                   #   Number of data bits = 8
    ComPort.parity   = 'N'                                                                 #   No parity
    ComPort.stopbits = 1                                                                   #   Number of Stop bits = 1
    ComPort.timeout = 3                                                                    #   setting timeout for 10 sec's'
    return ComPort

  except serial.SerialException:                                                           #   check for proper COM Port settings
    print("Check whether Your Device is Connected to specified Port Properly")
    exit()




# Functionn for Closing COM port
def ComPortClose(ComPort):                                                      
  ComPort.close()



# Function to write Serial No, Dev_id and Key onto Device
def StatusForWriteOntoDevice(reply,ComPort):                                    

  #  Converting required String Format to write correctly onto the device.
  StringtoWriteOnDevice = "SerialNo:" +  reply["serialNumber"] + ",Key:" + reply["key"] + ",DeviceId:" + reply["dev_id"] + ","    
    
  NumberOfBytesWritten = ComPort.write(b'\x1b\x32')                                       #   x1b\x32 writing onto device
  ReadStatus = ComPort.write(StringtoWriteOnDevice.encode())  

  WriteStatus = ComPort.read(10)                                                          #   Reading Status of ComPortwrite                                
  Status = WriteStatus.decode('utf-8')                  
  return Status                                                                           #   returning status of WriteOntoDevice





# Function for getting Product Descriptor from device
def GetProductDescriptor(ComPort):                                              
  NumberOfBytesWritten = ComPort.write(b'\x1b\x33')                                       #   Command to write for getting ProductDescriptor from device 
  
  RecievedProductDescriptor = ComPort.read(32)                                  
  ProductDescriptor = RecievedProductDescriptor.decode('utf-8')                    
  return ProductDescriptor                                                                #   returning the recieved ProductDescriptor






#Creating Factory Device by sending device details
def createFactoryDevice(device,ReturnedToken,productdescriptor):
  headers = {
        'x-access-token':ReturnedToken,                                                   #   providing necessary parameters for http post method
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
  
  r = requests.post(url = URL+devregpath, json = devregparam,headers=headers)             #    requesting data
  data = r.json()
  
  if r.status_code == 400:                                                                #    checking possible status code for error checking
    print("Message:"+data['message'] + " (" +"error code:" + data['responsecode']+")")
    exit()
  elif r.status_code == 401:
    print("Message:"+data['message'] + " (" +"error code:" + data['responsecode']+")")
    exit()
  elif r.status_code == 500:
    print("Message:"+data['message'] + " (" +"error code:" + data['responsecode']+")")
    print(r.status_code)
    exit()
  else:
    return r.text






#Function for getting the Model List from server by passing recieved token from login
def getModelList(ReturnedToken):
  headers = {
        'x-access-token':ReturnedToken,                                                     #    providing necessary parameters for http get method
        'Content-Type': 'application/json',
        'Cache-Control': 'no-cache',
       
    }

  r=requests.get(url = URL+getdeviceListpath,headers=headers)                           
  data = r.json()
  
  if r.status_code == 500:                                                                  #   checking possible status code for error checking
    print('Server Not Responding!')
    exit()
  else: 
    i=0
    for item in data:                                                                       #   getting the model No
      if item['modelNo']=='NBP100':
        choice=i
      i+=1  
    return data[choice]  






# Function For Login
def login():                            
  print("enter username")                                                                   #    fetch username & from user through cmd
  username = input()                                                                        
  print("enter password")
  password = getpass.getpass()
  PARAMS = {'user':username,'password':password,'usertype':"NGXFuser"}                      #    Passing necessary parameters in json format
  try:
    r = requests.post(url = URL+loginpath, json = PARAMS)                                   #    login path and necessary parameters
    data = r.json()
    #print(data) 
    if r.status_code == 200:                                                                #    check status code for login verify 
      print('Login Success!')                                                              
      global token                                                                          
      token=data['token']
      return token
    elif r.status_code == 402:                                                              #    Error checking.
      print("Message:"+data['message'] + " (" +"error code:" + data['responsecode']+")")
      exit()
    elif r.status_code == 403:
      print("Message:"+data['message'] + " (" +"error code:" + data['responsecode']+")")
      exit()
    elif r.status_code == 500:
      print("Message:"+data['message'] + " (" +"error code:" + data['responsecode']+")")
      exit()
    else:
      pass 
  except requests.exceptions.RequestException as e:
      print (e)
      exit()






# Function to Check Server reply to the passed object serverReply
def serverReplyToObject(serverReply):
  serverReply_dict = json.loads(serverReply)
  serialNumber = serverReply_dict['serialNo']
  key = serverReply_dict['key']
  dev_id = serverReply_dict['upserted'][0]['_id']

   
  deviceReply={                                                 #   extracting necessary parameters from server Object
      'serialNumber':serialNumber,
      'key':key,
      'dev_id':dev_id
  }
  return deviceReply                                            #   return serialNO, key and dev_id from server






# main function starts from here
def main():                                                    
  checkInternetConnection()                                               
  ComPort = openComPort()     
  ReturnedToken = login()
  model = getModelList(ReturnedToken)
  print ("This program registers :",model['modelNo'])
  while True:
    checkInternetConnection()
    answer = input("Do you want to continue yes(press y) or No(press any key):")
    if answer == "y":
      productDescriptor = GetProductDescriptor(ComPort)
      if(len(productDescriptor)>0):
          serverReply = createFactoryDevice(model,ReturnedToken,productDescriptor)
          reply = serverReplyToObject(serverReply)
          ReadStatus = StatusForWriteOntoDevice(reply,ComPort)
          if('SUCCESS' in ReadStatus ):
            print("Device Write Sucessful!")
          else:
            print("Device Write Failed!")
            exit()
      else:
          print("error communicating with device check the connections Properly!")
          exit()
    else:
      break





if __name__== "__main__":
  main()
