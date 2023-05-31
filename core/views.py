import csv
import io
import os
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from django.conf import settings
from rest_framework.response import Response

def front(request):
    context = {}
    return render(request, "index.html", context)

@api_view(['POST'])
def upload_csv(request):
    files = request.FILES.getlist('files')
    merged_file_data = io.StringIO()
    writer = csv.writer(merged_file_data)

    for file in files:
        decoded_file = file.read().decode('utf-8')
        csv_reader = csv.reader(io.StringIO(decoded_file))
        for row in csv_reader:
            writer.writerow(row)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="merged_file.csv"'
    response.write(merged_file_data.getvalue())

    base_url = request.build_absolute_uri('/')  # Get the base URL of the current request
    download_link = f'{base_url}download-csv/?fileData={merged_file_data.getvalue()}'  # Pass fileData as a query parameter

    return Response({'downloadLink': download_link, 'fileData': merged_file_data.getvalue()})


@api_view(['GET'])
def download_csv(request):
    file_data = request.GET.get('fileData')
    response = HttpResponse(file_data, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="merged_file.csv"'
    return response
	