import xlwt;
from datetime import datetime;
from xlrd import open_workbook;
from xlwt import Workbook;
from xlutils.copy import copy
from pathlib import Path

def output(filename, sheet,num, name, present):
    my_file = Path(r'D:/Study/Coding/Projects/Mini Project/main/attendance/'+filename+str(datetime.now().date())+'.xls')
    if my_file.is_file():
        rb = open_workbook(r'D:/Study/Coding/Projects/Mini Project/main/attendance/'+filename+str(datetime.now().date())+'.xls')
        #create a copy of the retreived workbook to update the attendance so that original is not affected
        book = copy(rb)
        sh = book.get_sheet(0)#get the first sheet
        # file exists
    else:
        book = xlwt.Workbook()
        sh = book.add_sheet(sheet)
    style0 = xlwt.easyxf('font: name Times New Roman, color-index blue, bold on', num_format_str='#,##0.00')
    style1 = xlwt.easyxf(num_format_str='D-MMM-YY')

    sh.write(0,0,datetime.now().date(),style1)


    col1_name = 'Name'
    col2_name = 'Present'
    col3_name = 'Time'


    sh.write(1,0,col1_name,style0)
    sh.write(1, 1, col2_name,style0)
    sh.write(1, 2, col3_name,style0)

    sh.write(num+1,0,name)
    sh.write(num+1, 1, present)
    current_time = datetime.now().time()
    indian_time_format = current_time.strftime('%H:%M:%S')
    sh.write(num+1, 2, indian_time_format)
    
    fullname=filename+str(datetime.now().date())+'.xls'
    book.save(r'D:/Study/Coding/Projects/Mini Project/main/attendance/'+fullname)
    return fullname