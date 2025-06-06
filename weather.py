import requests
import csv
import boto3

url = "https://meteostat.p.rapidapi.com/point/monthly"

querystring = {"lat":"52.5244","lon":"13.4105","alt":"43","start":"2020-01-01","end":"2020-12-31"}

headers = {
	"x-rapidapi-key": "6886ab47a9mshf61f5db01b28535p12d8cajsn4de7a2ba49f8",
	"x-rapidapi-host": "meteostat.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

data = response.json()

weatherdata = data.get('data',[]) 

if weatherdata:
    with open('weatherdata.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = weatherdata[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in weatherdata:
            writer.writerow(row)
    print("Data saved to weatherdata.csv successfully!")

bucket_name = 'weatherdatafrom20'
s3_key = 'weatherdata.csv'

s3 = boto3.client('s3')
try:
    s3.upload_file('weatherdata.csv',bucket_name,s3_key)
    print(f"file uploaded to S3://{bucket_name}/{s3_key}")
except Exception as e:
    print("error uploading file",e) 

#print(response.json())