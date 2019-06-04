import subprocess
import os
import time
from tkinter import * 
import csv
from tkinter import messagebox
master = Tk()
e1 = Entry(master)
e2 = Entry(master)
Label(master,text="\n").grid(row=0)
Label(master,text="start number.").grid(row=0)
e1.grid(row=0,column=2)
Label(master,text="\n").grid(row=2)
Label(master,text="End number.").grid(row=2)
e2.grid(row=2,column=2)

Label(master,text="\t").grid(column=3)
Label(master,text="\n").grid(row=4)
t1= open('abc.prm','r')
lines=t1.readlines()
s1=open('printerserial.csv', 'r')
count =0
for i in s1:
    count += 1
print(count)
def read_cell(x, y):
    with open('printerserial.csv', 'r') as f:
        reader = csv.reader(f)
        y_count = 0
        for n in reader:
            if y_count == y:
                cell = n[x]
                return cell
            y_count += 1
def sr_no():
    tem1=int(e1.get())
    tem2=int(e2.get())
    if 0 < tem1 and tem1 <= tem2:
        for i in range(tem1,tem2 +1):
            f1=read_cell(0, i)
            f2=read_cell(1, i)
            f3=read_cell(2, i)
            f4=read_cell(3, i)
            f5=read_cell(4, i)
            print(f5)
            f6=read_cell(5, i)
            t2=open('temp.prm','w')
            for line in lines:
                if "%%f1" in line:
                    tem1=line.replace("%%f1",f1)
                    t2.write(tem1)
                elif "%%f2" in line:
                    tem1=line.replace("%%f2",f2)
                    t2.write(tem1)
                elif "%%f3" in line:
                    tem1=line.replace("%%f3",f3)
                    t2.write(tem1)
                elif "%%f4" in line:
                    tem1=line.replace("%%f4",f4)
                    t2.write(tem1)
                elif "%%f5" in line:
                    tem1=line.replace("%%f5",f5)
                    t2.write(tem1)
                elif "%%f6" and "BARCODE" in line:
                    ff=f6.replace(",","!100,")
                    tem1=line.replace("%%f6",ff)
                    t2.write(tem1)
                elif "%%f6" in line:
                    tem1=line.replace("%%f6",f6)
                    t2.write(tem1)
                else :
                    t2.write(line)
            t2.close()
            time.sleep(1)
        
            cmdCommand = "Rawprint.exe \"Bar Code Printer T-9650 Plus\" temp.prm"   #specify your cmd command
            returned_value=os.system(cmdCommand)
    else:
        messagebox.showinfo("Error","Invalid Value.,please check the database!")
Button(master,text="Quit",command=master.quit).grid(row=3,column=3,sticky=W,pady=4)
Button(master,text="Print",command=sr_no).grid(row=3,column=2,sticky=W,pady=4)
    #t2.close()
master.mainloop()