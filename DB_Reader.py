from Employee import Employee
from Shift import Shift

days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

def readEmployees(fileName):
    """read from DB file all the employees in the system
    input: DB FILE NAME
    return list of employees"""
    f = open("DB Files/" + fileName + ".txt", "rt")
    lst_e = f.readline().split(",")             #read list of employees
    lst_e.remove("\n")
    lst_employees = []

    for e in lst_e:
        lst_employees.append(Employee(e))

    f.close()
    return lst_employees

def readNoEmployees(fileName):
    """read from DB file the number of employees in one shift
       input: DB FILE NAME
       return lnumber of employees - int"""
    f = open("DB Files/" + fileName + ".txt", "rt")
    r = f.readlines()
    number = int(r[-1])         #read number of employees
    f.close()
    return number

def readShifts(fileName):
    """read from DB file all the shifts in the system
       input: DB FILE NAME
       return dictionary of shifts by day"""
    f = open("DB Files/" + fileName + ".txt", "rt")
    r=f.readlines()
    lst_s = []
    for line in r:                      #read shifts from DB
        if line[0] =="-":
            lst_s.append(line.split(","))

    dict = {}
    for s in lst_s:
        s.remove("\n")
        s[0] = s[0][1:]                 #
        s.remove(s[0])

    j=0
    for s in lst_s:
        l= []
        for i in range(len(s)):
            if i%3 == 0:
                sName = s[i]
            if i%3 == 1:
                sSH = s[i]
            if i%3 == 2:
                sEH = s[i]
                l.append(Shift(sName,sSH,sEH))
        q = {days[j]:l}
        dict.update(q)
        j+=1
    f.close()
    return dict