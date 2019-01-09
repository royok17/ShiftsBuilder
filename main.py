from copy import deepcopy
import os
from Shift_Req_Builder import buildFormat
from DB_Reader import *
from Shifts_Reader import readEmployeeReq
from random import shuffle
from Board_Builder import buildBoard

days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

def setEmployees():
    """in this function we ask the user to fill all the emplyees in the company
        return: list of employees"""
    count_employees = 0
    lst_employees = []

    while (True):
        employee = input('Please enter emplyee, to finish press q ')        # input from user q to quit
        if employee == "q":
            break
        if employee != "":
            lst_employees.append(Employee(employee))        #add to list
            count_employees += 1    #count employees
            print("Great you insert: *** " + employee + " *** & now you have " + str(count_employees) + " employees\n")

    return lst_employees

def setShifts():
    """in this function we ask the user to fill all the shifts he want
            return: list of shifts"""
    lst_shifts = []

    while (True):
        print("Now we set shifts - to finish press q any time")     # input from user q to quit
        name = input("Please enter shift name")
        if name == "q":
            break
        start_hour = input("Please enter shift start hour, <EXAMPLE: for 19:00 insert 19>: ")
        if start_hour == "q":
            break
        end_hour = input("Please enter shift end hour, <EXAMPLE: for 21:00 insert 21>: ")
        if end_hour == "q":
            break

        if name != "" and start_hour != "" and end_hour != "":      #check if all value are sets
            lst_shifts.append(Shift(name,start_hour,end_hour))

    return lst_shifts

def deleteShifts(dict):
    """in this function we let the user to delete any shift he want in any day at the week
            input: dictionary of shifts by day
            return: dictionary shift after deleted"""
    i=1
    print("Please select day")  #select day in week
    for k,v in dict.items():
        print(str(i)+") " +k)
        i+=1
    print("0) quit from delete shifts")  #select shift
    day = input()
    if day == "0":
        return
    if int(day)>=1 and int(day)<=7:
        print("Please select shift to delete")
        index =int(day)-1
        i = 1
        for s in dict[days[index]]:
            print(str(i)+ ") " + s.name)
            i+=1
        print("0) quit from delete shifts")
        shift = input()
        sIndex = int(shift)
        if sIndex == '0':
            return
        if sIndex >=1 and sIndex<=i:        #delete day from list
            del dict[days[index]][sIndex-1]

    return dict

def initNewBoard():
    """in this function we initiailize the first setting of the board that user want
        the user can to add employees,add shifts, set the number of employees in one shift,delete shift
        by day and save the setting by writing in DB File when he is finish
    """
    lst_employees = []          #employees list
    lst_shifts = []             #shifts list
    no_of_emplyees = "1"        #default == 1
    dict_shiftsByDays = {}

    while(True):
        print("\n\n- OK.. lets start to build your board -")
        print("1) Add employees")
        print("2) Add shifts")
        print("3) Select number of employees per shift - Default is 1")
        print("*** Only after you set Employees and shifts ***")
        print("4) Delete shifts per day")
        print("5) Save board")
        print("0) back to menu")
        number = input()

        if number == '0':
            return
        if number == '1':
            lst_tmp = setEmployees()            #list of employees
            lst_employees = lst_employees+lst_tmp

        if number == '2':
            lst_tmp = setShifts()           #list of shifts
            lst_shifts = lst_shifts+lst_tmp
            for i in range(0,7):
                dict_shiftsByDays[days[i]] = deepcopy(lst_shifts)

        if number == '3':                  #number of employees
            no_of_emplyees = input("\nPlease enter the number of emplyees in one shift")

        if number == '4' and len(lst_shifts)>0:     # get in only if shifts and employees is sets
            dict_shiftsByDays = deleteShifts(dict_shiftsByDays)

        if number == '5' and len(lst_shifts)>0 and len(lst_employees)>0:        #save board
            name = input("Please select Board name:")
            file = open('DB Files/'+name+'.txt', 'w')           #write to this file
            for e in lst_employees:
                file.write(e.name + ",")
            for k,v in dict_shiftsByDays.items():
                file.write("\n-"+k+",")         #writing...
                for s in v:
                    file.write(s.name + "," + s.start_hour + "," + s.end_hour + ",")
            file.write("\n")
            file.write(no_of_emplyees)
            file.close()
            return
            # dir_path = os.path.dirname(os.path.realpath('DB Files/' + file.name+ '.txt'))
            # os.startfile(dir_path + "/" + file.name + '.txt')

def getAllShifts(dict):
    """get the longest list to know the maximum nuber of shift in day
                input: dictionary of shifts by day
                return: list of shifts"""
    maxList = []
    for k, v in dict.items():
        if len(v) > len(maxList):   # get the max list of shifts
            maxList = deepcopy(v)
    return maxList

def createReqFiles(fileName):
    """in this function we create request file for each employee
                input: DB FILE name
    """
    lst_employees = readEmployees(fileName) #list of employees from DB
    dict = readShifts(fileName)             #read shifts form DB
    lst_shifts = getAllShifts(dict)

    newpath = r'Requests/'+fileName
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    for e in lst_employees:
        buildFormat(fileName,e.name, lst_shifts)        #create file for each user

def dayToIndex(k):
    """ sub method that convert key of dictionary to index
    input: key - str
    return index - int """
    for i in range(0,7):
        if k == days[i]:
            return i

def isEmpWorked(name,dict,key,lst_ind):
    """ sub method that check if employee allready worked shift before
        input: employee's name, dict of placed shifts,day and index of shift list
        return true/false """
    list=[]
    if lst_ind == 0 and key == "Sunday":    #id its first shift in week
        return True
    if lst_ind != 0:
        list = dict[key][lst_ind-1]

    yesterday = ""
    if lst_ind == 0:
        for k,v in dict.items():
            if k!=key:
                yesterday = k       #the new day to sets
            else:
                break
        list = dict[yesterday][-1]

    for emp in list:
        if name == emp.split(":")[1]:
            return False

    return True

def placedEmployees(l_emp,d_placed,pri,shift,k,no_of_emplyees,sCount):
    """ in this function we set all the employees in the board according to his file request
        input: list of all employees, dict of placed shifts,priority level shift name,
                num of employees in shift,index of shift in list"""
    i = dayToIndex(k)
    shuffle(l_emp)          #shuffle employees
    for e in l_emp:
        if e.sft_request[i][1] == pri:      #check proirity
            for s in e.sft_request[i][0]:       #check request of emplyees
                if s == shift and len(d_placed[k][sCount]) < no_of_emplyees:
                    if isEmpWorked(e.name,d_placed,k,sCount):       #check if employee was not work shift before
                        d_placed[k][sCount].append(shift + ":" +e.name)

def insertByRandom(lst_miss, dict_placed,lst_employees):
    """ in this function we insert employees randomaly in the shifts thst not all the employees are sets
        input:  list of miss shifts,dict of placed shifts,list of employees
        return:: dict of placed shifts updated """

    eIsWork = False
    for l in lst_miss:
        j=l[3]          # number of employees left
        k = l[0]        # day
        shuffle(lst_employees)
        for e in lst_employees:
            if j==0:
                pass
            for v in dict_placed[k][l[1]]:      #run on dictionary
                name = v.split(":")[1]
                if name == e.name:
                    eIsWork = True
                else:
                    eIsWork = False
            if eIsWork == False and j > 0:
                dict_placed[k][l[1]].append(l[2] + ":" +e.name)
                j-=1

    return dict_placed

def placeShifts(fileName):
    """in this function we set all the employees in the board according to his file request and after the board is
     complete we finish if not we let the user choose if he want to keep it like this or put employees randomaly
     input:DB File Name"""
    lst_employees = readEmployees(fileName)     # read list of employees from DB
    dict_allShifts = readShifts(fileName)       # read shifts from DB
    no_of_emplyees = readNoEmployees(fileName)  # read numbers of employees
    lst_shifts = getAllShifts(dict_allShifts)

    dict_placed = {}
    lst_priority = [1,2,3]              #days praiorities list
    for e in lst_employees:
        readEmployeeReq(fileName,e)     #read all employees requests

    for k,v in dict_allShifts.items():
        dict_placed.setdefault(k, [])
        sCount = 0
        for s in v:             #for each shift in day
            if len(dict_placed[k]) < len(v):
                dict_placed[k].append([])
            for p in lst_priority:
                placedEmployees(lst_employees,dict_placed,p,s.name,k,no_of_emplyees,sCount)
            sCount +=1

    x = isShiftsFull(dict_placed,dict_allShifts, no_of_emplyees)        #check if all board complete
    if len(x) == 0 :
        buildBoard(fileName, lst_shifts, no_of_emplyees,dict_placed)
    else:                                                               #if board not complete
        print("\nThe  board is not complete, Press the number of the option you want.\n")
        print("1) Build the board as it is.")
        print("2) Insert employees randomly.")
        number = input()
        if (number == '1'):
            buildBoard(fileName, lst_shifts, no_of_emplyees, dict_placed)
        if (number == '2'):
            buildBoard(fileName, lst_shifts, no_of_emplyees, insertByRandom(x, dict_placed, lst_employees))
        dir_path = os.path.dirname(os.path.realpath('Final Board/' + fileName +'.xlsx'))
        os.startfile(dir_path +"/"+ fileName +'.xlsx' )

def printDict(dict_placed):
    """print any dictionary for debug
    input: dictionary"""
    for k, v in dict_placed.items():
        for s in v:
            for item in s:
                print(str(k) + ": " + item)

def shiftNotHere(lists,allShifts):
    """check which shift is empty and not set with any employee
    input: list of shift in some day, list of all the shifts in the system
     return : the name of shift that miss"""
    shiftIsHere = False
    for s in allShifts:
        for l in lists:
            if len(l)>0  and s.name == l[0].split(":")[0] :     #check if shift exist
                shiftIsHere = True
        if shiftIsHere == False:
            return s.name

def isShiftsFull(dict_placed,dict_all_shifts,no_of_emplyees):
    """check if all board is complete and set in all his shifts"""
    lst_Miss =[]
    for k, v in dict_placed.items():
        i=0
        for s in v:
            x = shiftNotHere(v, dict_all_shifts[k])         #check if shift exist
            if len(s) < len(dict_all_shifts[k]) and x is not None :
                l = [k, i, x, no_of_emplyees]
                print("On " + l[0] +" "+ str(l[3]) + " employees missing at shift: "+ l[2])
                lst_Miss.append(l)
            for item in s:
                l = [k, i, item.split(":")[0], no_of_emplyees - len(s)]
                if len(s) < no_of_emplyees and l not in lst_Miss:
                    print("On " + l[0] +" "+ str(l[3]) + " employees missing at shift: " + l[2])
                    lst_Miss.append(l)
            i+=1

    return lst_Miss

def main():
    """ this main simulate an user interface and this is the start of the program"""
    print("Welcome to shifts board builder!")
    while(True):
        print("\nPress the number of the option you want.\n")
        print("1) Initialize New Board")
        print("2) start create Requests files")
        print("3) build board")
        print("0) Exit")

        number = input()
        if(number == '1'):
            initNewBoard()
        if (number == '2'):
            fileName = input("\nplease enter your board name: \n")
            try:
                createReqFiles(fileName)
            except Exception as e: print(e)

        if (number == '3'):
            fileName = input("\nplease enter your board name: \n")
            try:
                placeShifts(fileName)
            except Exception as e: print(e)
        if (number == '0'):
            return

if __name__ == "__main__":
    main()