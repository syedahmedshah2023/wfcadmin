from celery import shared_task
from adminsupport.models.EmployeeModels import EmployeeModel
from adminsupport.models.TimeAttendanceReportModel import TimeAttendanceReport

from random import randint
import csv


@shared_task
def bulk_insert_ADAC_Emp_data_in_db(data):
    ADACEmpList = data
    EmployeeModel.objects.bulk_create(
        [EmployeeModel(**item) for item in ADACEmpList])


@shared_task
def process_time_attendance_report_csv(filepath):
    with open(filepath, 'r') as file:
        csv_data = csv.reader(file)
        TAData = [TimeAttendanceReport(
            Report_Date=row[0],
            Day_of_the_Week=row[1],
            Company=row[2],
            Division=row[3],
            Employee_ID=row[4],
            Employee_Name=row[5],
            Email_ID=row[6],
            Designation=row[7],
            Punch_In=row[8],
            Punch_Out=row[9],
            Actual_Duration=row[10],
            Expected_Duration=row[11],
            Temp_Expected_Duration=row[12],
            Start_Location_Name=row[13],
            DIL=row[14],
            Is_Force_Ended=row[15],
            Method=row[16],
            End_Location_Name=row[17],
            Remarks=row[18],
            Correction_Reason=row[19],
            Correction_Time_Start=row[20],
            Correction_Time_End=row[21],
            Correction_Comment=row[22],
            Leave_Type=row[23],
            Leave_Status=row[24],
            Exceptions_Expected_Duration=row[25],
            Travel_Type=row[26],
            Business_Travel_Status=row[27],
            WFH_Status=row[28],
            Department=row[29],
            Function=row[30],
            Section=row[31],
            Shift_Type=row[32],
            Shift_SubType=row[33],
            Sub_Section=row[34],
            uuid=row[35],
            Shift_Id=row[36],
            Shift_Date=row[37],
            Shift_Name=row[38],
            Employee_Shift_Type=row[39],
            Employee_Shift_SubType=row[40],
            Shift_From=row[41],
            Shift_To=row[42],
            Modified_Date=row[43]) for row in csv_data]
        TimeAttendanceReport.objects.bulk_create(TAData)
