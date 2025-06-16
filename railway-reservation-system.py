#Modules & Connect
import pickle as p
import os
import mysql.connector

connect=mysql.connector.connect(host='localhost',user='root',password='tiger',database='test')
mycursor=connect.cursor()

#Functions
def menu():
    print('''   START:                            END:
                trivandrum                        chennai
                chennai                           bangalore
                bangalore                         bhopal
                hyderabad                         bubaneswar
                panaji                            chandigarh
                                                  dehradun
                                                  delhi
                                                  gandhinagar
                                                  hyderabad
                                                  jaipur
                                                  jammu
                                                  kolkata
                                                  lucknow
                                                  mumbai
                                                  panaji
                                                  patna
                                                  raipur
                     		                  ranchi
                                                  shimla
                                                  agartala
                                                  trivandrum''')

def frontpage(x,y):
    sql1=("select * from schedule where start='{}' and end='{}'".format(x,y))
    mycursor.execute(sql1)
    dt=mycursor.fetchall()
    if dt!=[]:
        for i in dt:
            print("Start:{:<20}\n Stop:{:<20}\n Time:{:<20}\n Duration:{:<20}\n Price:{:<20}\n Train:{:<20}\n Trainno :{:<20}\n".format( i[0],i[1],i[2],i[3],i[4],i[5],i[6]))
            print()
    else:
        print('RECORD NOT FOUND')


        
def enterinput(a,b):
    ticket={}
    name=input('Name: ')
    age=input('Age: ')
    berth=input('Berth: ')
    gen=input('Gender(F/M/O): ')
    date=a
    train=b

    ticket['train']=train
    ticket['date']=date
    ticket['name']=name
    ticket['age']=age
    ticket['berth']=berth
    ticket['gen']=gen
    return ticket



def writefile(data):
    with open('project.dat','ab') as outfile:
        p.dump(data,outfile)
        outfile.flush()
        
def deletefile(nam):
    flag=False
    infile=open('project.dat','rb')
    outfile=open('Project.dat','wb')

    try:
        while True:
            ticket=p.load(infile)
            if ticket['name']!=nam:
                p.dump(ticket,outfile)
                outfile.flush()
            else:
                flag=True
                
    except EOFError:
        
        infile.close()
        outfile.close()
        if os.path.exists('project.dat'):
            os.remove('project.dat')
            os.rename('Project.dat','project.dat')
        if flag:
            print('Ticket deleted successfully')
        else:
            print('No ticket found')

def displayfile():
    with open('project.dat','rb') as infile:
        try:
            while True:
                data=p.load(infile)
                print('Train: ',data['train'])
                print('Departure date: ',data['date'])
                print('Name: ',data['name'])
                print('Age: ',data['age'])
                print('Berth: ',data['berth'])
             
                print('Gender: ',data['gen'])
                print()

        except EOFError:
            pass

def checkout(x):
    with open('project.dat','rb') as infile:
        cnt=0
        try:
            while True:
                data=p.load(infile)
                cnt+=1
            
        except EOFError:
            pass
        sql=('select price from schedule where trainno={}'.format(x))
        mycursor.execute(sql)
        x=mycursor.fetchall()
        for i in x:
            
            a=' '.join(map(str,i))
            a=int(a)
            totalprice=cnt*a
            print('Total price: ',totalprice)

#Main Body
print('******************** WELCOME TO RAILBOOKING ********************')
menu()
begin=input('From: ')
stop=input('To: ')
date=input('Departure date: ')
print()
frontpage(begin,stop)

trainnumber=int(input('Train number: '))
print('*****************************************************************************')
print()


choice='Y'
while choice.upper()=='Y':
    info=enterinput(date,trainnumber)
    writefile(info)
    print()
    choice=input('Another Ticket (Y/N): ')
else:
    print('*****************************************************************************')


option=input('Delete ticket (Y/N): ')
if option.upper()=='Y':
    info=input('Name ticket to be deleted: ')
    deletefile(info)
    
    print('YOUR TICKETS: ')
    print()
    displayfile()
    checkout(trainnumber)
    print('************************ Thank you for booking via Rail Booking !!! ************************')
   
else:
    print('YOUR TICKETS: ')
    print()
    displayfile()
    checkout(trainnumber)
    print('************************ Thank you for booking via Rail Booking !!! ************************')
