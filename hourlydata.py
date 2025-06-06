import requests
import csv
import io
import boto3   # upload to S3 bucket
 
url = "https://meteostat.p.rapidapi.com/stations/hourly"
querystring = {"station":"10637","start":"2020-01-01","end":"2020-01-01","tz":"Europe/Berlin"}
headers = {
    "x-rapidapi-key": "bbbc929294msh0e308c05a64d507p1d12ccjsn7e697e693c76",
    "x-rapidapi-host": "meteostat.p.rapidapi.com"
}
 
response = requests.get(url, headers=headers, params=querystring)
data = response.json()
hourly_data = data.get('data', [])
 
if hourly_data:
    # Create in-memory CSV as bytes
    csv_string = io.StringIO()
    fieldnames = hourly_data[0].keys()
    writer = csv.DictWriter(csv_string, fieldnames=fieldnames)
    writer.writeheader()
    for row in hourly_data:
        writer.writerow(row)
    # Encode string to bytes
    csv_bytes = io.BytesIO(csv_string.getvalue().encode('utf-8'))
    csv_bytes.seek(0)
 
    # Upload to S3
    bucket_name = 'weatherdatafrom20'
    s3_key = 'hourlydatadocker.csv'
    s3 = boto3.client('s3')
    try:
        s3.upload_fileobj(csv_bytes, bucket_name, s3_key)
        print(f"File uploaded to s3://{bucket_name}/{s3_key}")
    except Exception as e:
        print("Error uploading file:", e)
else:
    print("No data found in the response.")
