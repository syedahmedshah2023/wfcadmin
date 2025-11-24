from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.db import connection
from random import randint
import requests
import json
import io
import csv
import pandas as pd
import math
from datetime import datetime
# Create Searializers,
# Create your views here.

from adminsupport.serializers.FileUploadSerializer import FileUploadSerializer
from adminsupport.tasks.dbTasks import process_time_attendance_report_csv
from adminsupport.models.TimeAttendanceReportModel import TimeAttendanceReport
from adminsupport.serializers.TimeAttendanceReportSerializer import TimeAttendanceSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import parsers
import tempfile
import os


class UploadTimeAttendanceReport(APIView):
    parser_classes = [parsers.MultiPartParser]

    def post(self, request):
        print(request.FILES)
        csv_file = request.FILES.get('csv_file')
        file_path = os.path.join('./files/TimeAttendance.csv')
        print(file_path)
        with open(file_path, 'wb+') as tmpFile:
            for chunk in csv_file.chunks():
                tmpFile.write(chunk)

        process_time_attendance_report_csv.delay(file_path)
        return Response([{"msg": "CSV file uploaded and processing started."}])


class FetchTimeAttendaceReport(APIView):
    def get(self, request):
        query_params = request.GET
        pageNumber = int(query_params.get('pageNumber'))
        recordsPerPage = int(query_params.get('recordsPerPage')) if query_params.get(
            'recordsPerPage') else 20
        employeeId = query_params.get('employeeId')
        reportDate = query_params.get('reportDate')
        reportDateFrom = query_params.get('reportDateFrom')
        reportDateTo = query_params.get('reportDateTo')
        employeeName = query_params.get('employeeName')
        company = query_params.get('company')
        division = query_params.get('division')
        function = query_params.get('function')
        department = query_params.get('department')
        section = query_params.get('section')
        leaveType = query_params.get('leaveType')
        leaveStatus = query_params.get('leaveStatus')
        travelType = query_params.get('travelType')
        wfhStatus = query_params.get('wfhStatus')
        shiftName = query_params.get('shiftName')

        filteredList = []

        filterKywargs = {}

        if employeeId:
            filterKywargs['Employee_ID__icontains'] = employeeId
        if reportDate:
            filterKywargs['Report_Date__icontains'] = reportDate
        if employeeName:
            filterKywargs["Employee_Name__icontains"] = employeeName
        if company:
            filterKywargs['Company__icontains'] = company
        if division:
            filterKywargs['Division__icontains'] = division
        if function:
            filterKywargs['Function__icontains'] = function
        if department:
            filterKywargs['Department__icontains'] = department
        if section:
            filterKywargs['Section__icontains'] = section
        if leaveType:
            filterKywargs['Leave_Type__icontains'] = leaveType
        if leaveStatus:
            filterKywargs['Leave_Status__icontains'] = leaveStatus
        if travelType:
            filterKywargs['Travel_Type__icontains'] = travelType
        if wfhStatus:
            filterKywargs['WFH_Status__icontains'] = wfhStatus
        if shiftName:
            filterKywargs['Shift_Name__icontains'] = shiftName

        pageEndIndex = pageNumber * recordsPerPage
        pageStartIndex = 0
        totalRecords = TimeAttendanceReport.objects.count()
        totalPages = math.ceil(totalRecords / recordsPerPage)

        if len(filterKywargs) > 0:
            tar = TimeAttendanceReport.objects.filter(
                **filterKywargs)[pageStartIndex:pageEndIndex]
        else:
            tar = TimeAttendanceReport.objects.all(
            )[pageStartIndex:pageEndIndex]
        serializer = TimeAttendanceSerializer(tar, many=True)

        if reportDateFrom is not None:
            dateFormatSQL = "%d/%m/%Y"
            dateFormat = "%Y-%m-%d"
            reportDateFrom = datetime.strptime(
                reportDateFrom, dateFormat).date()
            reportDateTo = datetime.strptime(reportDateTo, dateFormat).date()
            for item in serializer.data:
                if 'Report_Date' not in item['Report_Date']:
                    Report_Date = datetime.strptime(
                        item['Report_Date'], dateFormatSQL).date()
                    if Report_Date >= reportDateFrom and Report_Date <= reportDateTo:
                        filteredList.append(item)
        else:
            filteredList = serializer.data

        # SORT THE RECORDS BY REPORT_DATE
        filteredList = sorted(
            filteredList, key=lambda x: x["Report_Date"], reverse=True)

        if serializer.is_valid:
            return Response([{
                "msg": "Time Attendance Report Data Has Been Fetched Successfully",
                "search": len(filterKywargs),
                "totalRecords": totalRecords,
                "totalPages": totalPages,
                "recordsPerPage": recordsPerPage,
                "totalRecordsPerPage": len(filteredList),
                "pageNumber": pageNumber,
                "pageStartIndex": pageStartIndex,
                "pageEndIndex": pageEndIndex,
                "timeAttendanceReport": filteredList
            }])
        else:
            return Response([{
                "msg": "Invalid Time Attendance Data Found",
                "err": serializer.errors
            }])


class FetchUniqueColumns(APIView):
    def post(self, request):
        queryParams = request.data
        print("JSON +++", queryParams.get('fieldNames'))
        fieldNames = json.loads(queryParams.get('fieldNames'))
        dataList = []
        if fieldNames:
            for fn in fieldNames:
                cols = TimeAttendanceReport.objects.values_list(
                    fn, flat=True).distinct()
                dataList.append({"name": fn, "data": cols})
            return Response([{
                "msg": "Columns Data Has Been Fetched Successfully",
                "count": len(cols),
                "data": dataList
            }])
        else:
            return Response([{
                "msg": "No Data",
                "count": 0,
                "data": []
            }])
