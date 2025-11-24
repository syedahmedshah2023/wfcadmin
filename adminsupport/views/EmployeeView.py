from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.db import connection
from random import randint
import requests
import json
# Create Searializers,
# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from adminsupport.tasks.dbTasks import bulk_insert_ADAC_Emp_data_in_db

from adminsupport.serializers.EmployeeSerializer import EmployeeSerializer
import pandas as pd

@csrf_exempt
def fetch_timeAttendance(request):
    if request.method == 'GET':
        data = None
        data = pd.read_csv('')
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM ADAC_Emp_Master;")
            data = cursor.fetchall()
        return JsonResponse(data, safe=False)


class FetchADACEmployeeDataFullLoad(APIView):
    def post(self, request):
        ADACEmpList = []
        headersType = []
        load_type = 'F'
        if (load_type == 'F'):
            headersType = [{
                'count': 1,
                'headers': {
                    'content-type': 'application/json',
                    'X-API-Key': 'W56oMCDO/x2zOv/5pXX3RECs38wqEbYqFOiiuIX2v4zYmy4R2fu/fQ==',
                    'Username': 'aigk02RTJL5xycqcy7ksKZLjJMDKaIV4eJ6+05vvMW4=',
                    'Password': 'th1ZWqPvOqBxycqcy7ksKfGhZDg0BdOh',
                    'InitialLoad': 'true'
                }
            }]
        else:
            headersType = [{
                'count': 1,
                'headers': {
                    'content-type': 'application/json',
                    'X-API-Key': 'W56oMCDO/x2zOv/5pXX3RECs38wqEbYqFOiiuIX2v4zYmy4R2fu/fQ==',
                    'Username': 'aigk02RTJL5xycqcy7ksKZLjJMDKaIV4eJ6+05vvMW4=',
                    'Password': 'th1ZWqPvOqBxycqcy7ksKfGhZDg0BdOh',
                    'InitialLoad': 'false'
                }
            }]

        for h in headersType:
            for i in range(h['count']):
                response_api = requests.get(
                    'https://adac.datamanagement.wfcapps.com/DataExport/employees', headers=h['headers'])

                if response_api.status_code == 200:
                    data = response_api.json()
                    ADACEmpList = data
                    bulk_insert_ADAC_Emp_data_in_db.delay(ADACEmpList)

        if len(ADACEmpList) > 0:
            # serializer = EmployeeSerializer(data=ADACEmpList, many=True)
            print(ADACEmpList[0])
            # if serializer.is_valid(raise_exception=True):
            # serializer.save()
            return Response([{"message": "Employee data saved successfully"}])
            # else:
            # return Response(serializer.errors, status=400)
        else:
            return Response([{"message": "Employee data does not saved successfully"}])
