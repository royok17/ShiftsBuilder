import xlsxwriter

def char_range(c1, c2):
    """Generates the characters from `c1` to `c2`, inclusive."""
    for c in range(ord(c1), ord(c2)+1):
        yield chr(c)

def buildBoard(fileName,lst_shifts,no_of_employees,dict):
    """ here we write and design on excel file the shift board
    input: DB FILE NAME, list of shifts,number of employees and placed shifts dictionary"""
    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook('Final Board/' + fileName +'.xlsx')
    worksheet = workbook.add_worksheet()

    # Some data we want to write to the worksheet.

    days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

    name_format = workbook.add_format()         #desgin cell size
    worksheet.set_column(1, 12, 15, name_format)
    worksheet.set_default_row(30, name_format)
    name_format.set_align('center')
    name_format.set_align('vcenter')

    title_format = workbook.add_format()        #design title cell
    title_format.set_bg_color('yellow')
    title_format.set_align('center')
    title_format.set_align('vcenter')

    e_format = workbook.add_format()            #design employees cell
    e_format.set_bg_color('cyan')
    e_format.set_align('center')
    e_format.set_align('vcenter')

    border_format = workbook.add_format({       #design border cell
        'border': 2,
        'font_size': 15
    })
    worksheet.conditional_format('A1:Z20', {'type': 'no_blanks', 'format': border_format})

    j = 0                                       #write days as a title
    for i in char_range('B', 'H'):
        worksheet.write(i + str(1), days[j], title_format)
        j+=1

    endLine = int(no_of_employees)*len(lst_shifts)+1
    c=0
    for i in range(2,endLine):                  #merge cell for shift names
        cell = 'A'+ str(i) + ":" 'A' + str(i+int(no_of_employees)-1)
        if i == 2+no_of_employees*c:
            worksheet.merge_range( cell, "-", title_format)
            c+=1
    c=0
    A=[]
    for i in range(2,int(no_of_employees)*len(lst_shifts)+1):       #write names of shifts
        if i == 2+no_of_employees*c:
            s = lst_shifts[c].name
            worksheet.write('A'+str(i), s , title_format)
            A.append(s)
            c+=1

    j=0
    for i in char_range('B', 'H'):              #write employees names in board
        k=2
        for list in dict[days[j]]:
            numEmpLeft = 0
            for item in list:
                shift_name = item.split(":")[0]
                name = item.split(":")[1]
                c=0
                for a in A:
                    if a == shift_name:
                        k=2+no_of_employees*c +numEmpLeft
                        worksheet.write(i + str(k), name, e_format)
                        numEmpLeft +=1
                        k+=1
                    else:
                        c+=1

        j+=1

    worksheet.write('J1', "Shifts", title_format)               # write hours of shifts
    worksheet.write('K1', "Start Hour", title_format)
    worksheet.write('L1', "End Hour", title_format)
    for i in range(2, len(lst_shifts)+2):
        worksheet.write('J' + str(i), lst_shifts[i - 2].name, name_format)
        worksheet.write('K' + str(i), lst_shifts[i - 2].start_hour, name_format)
        worksheet.write('L' + str(i), lst_shifts[i - 2].end_hour, name_format)

    workbook.close()