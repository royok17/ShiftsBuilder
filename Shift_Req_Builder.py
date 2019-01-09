import xlsxwriter

def buildFormat(fileName,name,lst_shifts):
    """ here we write and design on excel file that will be a requests file for each employee
    input: DB FILE NAME, emplyee's name,list of shifts"""
    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook('Requests/' + fileName + "/" + name +'.xlsx')
    worksheet = workbook.add_worksheet()

    # Some data we want to write to the worksheet.

    days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    name_format = workbook.add_format()
    worksheet.set_column(1, 10, 15, name_format)
    worksheet.set_default_row(30, name_format)
    name_format.set_align('center')
    name_format.set_align('vcenter')

    title_format = workbook.add_format()
    title_format.set_bg_color('yellow')
    title_format.set_align('center')
    title_format.set_align('vcenter')

    border_format = workbook.add_format({
        'border': 2,
        'font_size': 15
    })
    worksheet.conditional_format('A1:Z20', {'type': 'no_blanks', 'format': border_format})

    worksheet.write('B1', "Days", title_format)
    worksheet.write('C1', "Shifts Request", title_format)
    worksheet.write('D1', "Praiority", title_format)
    worksheet.write('F1', "Shifts", title_format)
    worksheet.write('G1', "Start Hour", title_format)
    worksheet.write('H1', "End Hour", title_format)


    for i in range(2, 9):
        worksheet.write('B' + str(i), days[i - 2], name_format)
        worksheet.write('C' + str(i), " - ", name_format)
        worksheet.write('D' + str(i), " - ", name_format)
    for i in range(2, len(lst_shifts)+2):
        worksheet.write('F' + str(i), lst_shifts[i - 2].name, name_format)
        worksheet.write('G' + str(i), lst_shifts[i - 2].start_hour, name_format)
        worksheet.write('H' + str(i), lst_shifts[i - 2].end_hour, name_format)



