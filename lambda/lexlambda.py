import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
import os
import time

def win_by_wicket_ipl(intent_request):
    slots = intent_request['currentIntent']['slots']
    client = boto3.resource('dynamodb')
    table = client.Table('CricketIPL')
    response = table.scan(
        FilterExpression=Attr('date').gte(slots['matchDay1'])
    )
    for i in response['Items']:
        if i['winner'] == slots['teamO']:
            row = i
            break
    return {
            "dialogAction": {
                "type": "ElicitIntent",
                "message": {
                    "contentType": "PlainText",
                    "content": row['winner']+" won by "+row['win_by_wickets']+" wickets"
                }
            }
        }

def win_by_run_ipl(intent_request):
    slots = intent_request['currentIntent']['slots']
    print(slots)
    client = boto3.resource('dynamodb')
    table = client.Table('CricketIPL')
    response = table.scan(
        FilterExpression=Attr('date').gte(slots['matchDayF'])
    )
    for i in response['Items']:
        if i['winner'] == slots['teamF']:
            row = i
            break
    print(response['Items'])
    return {
            "dialogAction": {
                "type": "ElicitIntent",
                "message": {
                    "contentType": "PlainText",
                    "content": row['winner']+" won by "+row['win_by_runs']+" runs"
                }
            }
        }
    
def winner_ipl(intent_request):
    slots = intent_request['currentIntent']['slots']
    client = boto3.resource('dynamodb')
    table = client.Table('CricketIPL')
    """response = table.get_item(
        Key={
            'id':11148
        }
    )"""
    response = table.scan(
        FilterExpression=Attr('date').gte(slots['matchDate'])
    )
    for i in response['Items']:
        if i['team1'] == slots['teamOne'] and i['team2'] == slots['teamTwo'] or i['team2'] == slots['teamOne'] and i['team1'] == slots['teamTwo']:
            row = i
    return {
            "dialogAction": {
                "type": "ElicitIntent",
                "message": {
                    "contentType": "PlainText",
                    "content": row['winner']+" won the match"
                }
            }
        }
    """
    sessionAttributes = intent_request['currentIntent']['sessionAttributes']
    if "toss_winner" in sessionAttributes.keys():
        client = boto3.resource('dynamodb')
        table = client.Table('CricketIPL')
        response = table.scan(
            FilterExpression=Attr('date').gte(sessionAttributes['match_date'])
        )
        for i in response['Items']:
            if i['toss_winner'] == sessionAttributes['toss_winner']:
                row = i
        return {
            "dialogAction": {
                "type": "ElicitIntent",
                "message": {
                    "contentType": "PlainText",
                    "content": row['winner']
                }
            }
        }
    """
    
            
        
def toss_winner_ipl(intent_request):
    slots = intent_request['currentIntent']['slots']
    if slots['toss_date'] == 'null':
        return {
            "dialogAction": {
                "type": "ElicitSlot",
                "message": {
                "contentType": "PlainText or SSML or CustomPayload",
                "content": "On which date?"
                },
                "intentName": "TossWinner_IPL",
                "slots": slots,
                "slotToElicit" : "toss_date"
            }
        }
    client = boto3.resource('dynamodb')
    table = client.Table('CricketIPL')
    """response = table.get_item(
        Key={
            'id':11148
        }
    )"""
    response = table.scan(
        FilterExpression=Attr('date').gte(slots['toss_date'])
    )
    
    for i in response['Items']:
        if i['team1'] == slots['tossTeamOne'] and i['team2'] == slots['tossTeamTwo'] or i['team2'] == slots['tossTeamOne'] and i['team1'] == slots['tossTeamTwo']:
            row = i
    """
    print("++++++++++++++")
    print(row)
    """
    return {
        "sessionAttributes": { 
             "toss_winner": row['toss_winner'],
             "match_date": slots['toss_date']
          },
        "dialogAction":{
            'type':"ElicitIntent",
            'message': {
            "contentType": "PlainText",
            "content": row['toss_winner']+" won the toss"
            }
        }
    }

def welcome_ipl(intent_request):
    """slots = intent_request['currentIntent']['slots']"""
    return {
        "dialogAction":{
            'type':"ElicitIntent",
            'message': {
            "contentType": "PlainText",
            "content": "How can I help you?"
            }
        }
    }

def dispatch(intent_request):
    intent_name = intent_request['currentIntent']['name']
    if intent_name == 'Welcome_IPL':
        return welcome_ipl(intent_request)
    elif intent_name == 'TossWinner_IPL':
        return toss_winner_ipl(intent_request)
    elif intent_name == 'Winner_IPL':
        return winner_ipl(intent_request)
    elif intent_name == "WinByRun_IPL":
        return win_by_run_ipl(intent_request)
    elif intent_name == "WinByWicket_IPL":
        return win_by_wicket_ipl(intent_request)
    else:
        pass

def lambda_handler(event, context):
    # TODO implement
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    return dispatch(event)