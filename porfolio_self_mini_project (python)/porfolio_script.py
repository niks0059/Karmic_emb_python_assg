import subprocess
import os
import time
import csv

t1= open('html_code.html','r')
lines=t1.readlines()
s1=open('details.csv', 'r')
count =0
for i in s1:
    count += 1
print(count)
def read_cell(x, y):
    with open('details.csv', 'r') as f:
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
            Name=read_cell(0, 1)
            Post=read_cell(1, 1)
            About=read_cell(2, 1)
            Age=read_cell(3, 1)
            Email=read_cell(4, 1)

            Phone=read_cell(5, 1)
            Address=read_cell(6, 1)
            Languages=read_cell(7, 1)
            Summary=read_cell(8, 1)
            Exp=read_cell(9, 1)
            Company=read_cell(10, 1)
            print(Email)
            
            t2=open('html_code.html','w')
            for line in lines:
                if "%%name" in line:
                    tem1=line.replace("%%name1",Name)
                    t2.write(tem1)
                elif "%%post" in line:
                    tem1=line.replace("%%post",Post)
                    t2.write(tem1)
                elif "%%about" in line:
                    tem1=line.replace("%%about",About)
                    t2.write(tem1)
                elif "%%age" in line:
                    tem1=line.replace("%%age",Age)
                    t2.write(tem1)
                elif "%%email" in line:
                    tem1=line.replace("%%email",Email)
                    t2.write(tem1)
                elif "%%phone" in line:
                    tem1=line.replace("%%phone",Phone)
                    t2.write(tem1)
                elif "%%addr" in line:
                    tem1=line.replace("%%addr",Address)
                    t2.write(tem1)

                 elif "%%lang" in line:
                    tem1=line.replace("%%lang",Languages)
                    t2.write(tem1)
                elif "%%sum" in line:
                    tem1=line.replace("%%sum",Summary)
                    t2.write(tem1)
                elif "%%from_to" in line:
                    tem1=line.replace("%%from_to",Exp)
                    t2.write(tem1)
                elif "%%company" in line:
                    tem1=line.replace("%%company",Company)
                    t2.write(tem1)
                else :
                    t2.write(line)
            t2.close()
            time.sleep(1)
        
           # cmdCommand = "Rawprint.exe \"Bar Code Printer T-9650 Plus\" temp.prm"   #specify your cmd command
            #returned_value=os.system(cmdCommand)
