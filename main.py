#program for Factory Device Identification for Product Description, Serial number and warranty period (Cloud based).
import requests                         #importing necessary libraries.
import serial                   
from tkinter import *
from tkinter.ttk import *
import time

BaudRate = 115200
URL = "https://devnbpcs.ngxconnect.co.in/api/v1/"
loginpath='user/login'
getdeviceListpath='product/'
#PARAMS = {'user':'7434565656','password':'123123','usertype':"NGXFuser"} 
devregpath="device/factoryregister"
devregparam={}
token=''
choice=''

def dialog1():
    box.showinfo('info','Correct Login')
def dialog2():
    box.showinfo('info','Invalid Login')

def LoginWindow():                                                        #Function for login User Interface
  global my_window
  my_window = Tk()
  my_window.title("NGX Technologies Pvt. Ltd.n")
  my_window.configure(width=350,height=250)

  label = Label(my_window, text="Username")                               #for label username & its positioning.
  label.pack()
  label.place(relx=0.1,rely=0.2,anchor=CENTER)

  userNameEntry = Entry(my_window)
  userNameEntry.pack()
  userNameEntry.place(relx=0.6,rely=0.2,anchor=CENTER)
  username = userNameEntry.get()
  
  print(username)

  entry2 = Entry(my_window)
  passkey = entry2.get()
  print(passkey)
  entry2.pack()
  entry2.place(relx=0.6,rely=0.3,anchor=CENTER)

  PARAMS = {'user':'username','password':'passkey','usertype':"NGXFuser"}
  label = Label(my_window, text="Password")
  label.pack()
  label.place(relx=0.1,rely=0.3,anchor=CENTER)
def LoginClick():
  print("hello world!")
  print(userNameEntry.get())
  
  button1=Button(my_window,text='Login',command=LoginClick)
  button1.pack()
  button1.place(relx=0.3,rely=0.5,anchor=CENTER)

  button2=Button(my_window,text='Quit',command=quit)
  button2.pack()
  button2.place(relx=0.8,rely=0.5,anchor=CENTER)
  
  my_window.mainloop()






def ComportInitialization():                                                           #function for Comport initialization for UART Serial communication
  try:
    ComPort = serial.Serial('COM17') # open COM24
    ComPort.baudrate = 115200 # set Baud rate to 9600
    ComPort.bytesize = 8    # Number of data bits = 8
    ComPort.parity   = 'N'  # No parity
    ComPort.stopbits = 1    # Number of Stop bits = 1   
    
    data = ComPort.write(b'0x1B 0x33\x0A')
    string = ComPort.readline()
    data1=string.decode('utf-8')
    print(data1)
    ComPort.close()

  except serial.serialutil.SerialException:
      print("Check the port")




def createFactoryDevice(device):
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
    'deviceIdentifier':"1234516182011"
    }
  #datas = {"cardno":"6248889874650987","systemIdentify":"s08","sourceChannel": 12}
  #print(headers)
  r = requests.post(url = URL+devregpath, json = devregparam,headers=headers) 
  print(devregparam)
  print(r.text)
    


def login(**PARAMS):                                                        #
  try:
    r = requests.post(url = URL+loginpath, json = PARAMS) 
    data = r.json() 
    if r.status_code == 200:
      print('Login Success!')
      dialog1()
      global token
      token=data['token']
    else:
       pass
  except requests.exceptions.RequestException as e:
    print (e)
    dialog2()


def getModelList():
  headers = {
        'x-access-token':token,
        'Content-Type': 'application/json',
        'Cache-Control': 'no-cache',
       
    }

  r=requests.get(url = URL+getdeviceListpath,headers=headers)
  data = r.json() 
  i=0
  for item in data:
 #   print (item['moduleNo'])
    if item['modelNo']=='NBP100':
      choice=i
    i+=1;  
  return data[choice]


    
def main():
  PARAM=LoginWindow()
 # login(PARAM)
 # model = getModelList()
 # print(model)
  print ("This program registers :",model['modelNo'])
  while True:
    answer = input("Do you want to continue yes or no: ")
    if answer == "y":
      createFactoryDevice(model)
    else :
      break


if __name__== "__main__":
  main()