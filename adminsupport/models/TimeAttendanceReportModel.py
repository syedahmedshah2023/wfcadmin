from django.db import models


class TimeAttendanceReport(models.Model):
    Report_Date = models.TextField(max_length=255)
    Day_of_the_Week = models.TextField(max_length=255)
    Company = models.TextField(max_length=255)
    Division = models.TextField(max_length=255)
    Employee_ID = models.TextField(max_length=255)
    Employee_Name = models.TextField(max_length=255)
    Email_ID = models.TextField(max_length=255)
    Designation = models.TextField(max_length=255)
    Punch_In = models.TextField(max_length=255)
    Punch_Out = models.TextField(max_length=255)
    Actual_Duration = models.TextField(max_length=255)
    Expected_Duration = models.TextField(max_length=255)
    Temp_Expected_Duration = models.TextField(max_length=255)
    Start_Location_Name = models.TextField(max_length=255)
    DIL = models.TextField(max_length=255)
    Is_Force_Ended = models.TextField(max_length=255)
    Method = models.TextField(max_length=255)
    End_Location_Name = models.TextField(max_length=255)
    Remarks = models.TextField(max_length=255)
    Correction_Reason = models.TextField(max_length=255)
    Correction_Time_Start = models.TextField(max_length=255)
    Correction_Time_End = models.TextField(max_length=255)
    Correction_Comment = models.TextField(max_length=255)
    Leave_Type = models.TextField(max_length=255)
    Leave_Status = models.TextField(max_length=255)
    Exceptions_Expected_Duration = models.TextField(max_length=255)
    Travel_Type = models.TextField(max_length=255)
    Business_Travel_Status = models.TextField(max_length=255)
    WFH_Status = models.TextField(max_length=255)
    Department = models.TextField(max_length=255)
    Function = models.TextField(max_length=255)
    Section = models.TextField(max_length=255)
    Shift_Type = models.TextField(max_length=255)
    Shift_SubType = models.TextField(max_length=255)
    Sub_Section = models.TextField(max_length=255)
    uuid = models.TextField(max_length=255)
    Shift_Id = models.TextField(max_length=255)
    Shift_Date = models.TextField(max_length=255)
    Shift_Name = models.TextField(max_length=255)
    Employee_Shift_Type = models.TextField(max_length=255)
    Employee_Shift_SubType = models.TextField(max_length=255)
    Shift_From = models.TextField(max_length=255)
    Shift_To = models.TextField(max_length=255)
    Modified_Date = models.TextField(max_length=255)

    class Meta:
        db_table = 'TimeAttendanceReport'

    @staticmethod
    def get_trimmed_data():
        trimmed_data = []
        fields = TimeAttendanceReport._meta.get_fields()
        for field in fields:
            if isinstance(field, models.CharField):
                trimmed_data.append(field.attname)

        queryset = TimeAttendanceReport.objects.only(*trimmed_data)
        for obj in queryset:
            for field_name in trimmed_data:
                setattr(obj, field_name, getattr(obj, field_name).strip())

        return queryset
