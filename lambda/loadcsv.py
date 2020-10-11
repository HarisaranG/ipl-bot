import boto3
import csv

def lambda_handler(event, context):
    region='us-east-1'
    recList=[]
    try:            
        s3=boto3.client('s3')            
        dyndb = boto3.client('dynamodb', region_name=region)
        confile= s3.get_object(Bucket='ipl2019data', Key='data.csv')
        recList = confile['Body'].read().split('\n')
        firstrecord=True
        csv_reader = csv.reader(recList, delimiter=',', quotechar='"')
        for row in csv_reader:
            if (firstrecord):
                firstrecord=False
                continue
            matchid = row[0]
            season = row[1].replace(',','').replace('$','') if row[1] else '-'
            city = row[2].replace(',','').replace('$','') if row[1] else '-'
            date = str(row[3]).replace(',','').replace('$','') if row[1] else '-'
            team1 = row[4].replace(',','').replace('$','') if row[1] else '-'
            team2 = row[5].replace(',','').replace('$','') if row[1] else '-'
            toss = row[6].replace(',','').replace('$','') if row[1] else '-'
            decision = row[7].replace(',','').replace('$','') if row[1] else '-'
            result = row[8].replace(',','').replace('$','') if row[1] else '-'
            dl =  row[9]
            winner = row[10].replace(',','').replace('$','') if row[1] else '-'
            winRun = row[11]
            winWicket = row[12]
            mom = row[13].replace(',','').replace('$','') if row[1] else '-'
            venue = row[14].replace(',','').replace('$','') if row[1] else '-'
            umpire1 = row[15].replace(',','').replace('$','') if row[1] else '-'
            umpire2 = row[16].replace(',','').replace('$','') if row[1] else '-'
            response = dyndb.put_item(
                TableName='Cricket',
                Item={
                'id' : {'N':str(matchid)},
                'season': {'S': season},
                'city': {'N':city},
                'date': {'S': str(date)},
                'team1': {'S': team1},
                'team2': {'S': team2},
                'toss': {'S': toss},
                'decision': {'S': decision},
                'result': {'S': result},
                'dl': {'N': str(dl)},
                'winner': {'S': winner},
                'winRun': {'N': str(winRun)},
                'winWicket': {'N': str(winWicket)},
                'mom': {'S': mom},
                'venue': {'S': venue},
                'umpire1': {'S': umpire1},
                'umpire2': {'S': umpire2},
                'umpire3': {'S': '-'},
                }
            )
        print('Put succeeded:')
    except Exception, e:
        print (str(e))