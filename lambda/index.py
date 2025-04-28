import json
import os
import urllib.request
from urllib.error import URLError


API_URL = "https://1f22-35-204-30-163.ngrok-free.app/generate" 

def lambda_handler(event, context):
    try:
        print("Received event:", json.dumps(event))
        
        # リクエストボディの解析
        body = json.loads(event['body'])
        message = body['message']
        conversation_history = body.get('conversationHistory', [])
        
        print("Processing message:", message)
        
        # 会話履歴を使用
        messages = conversation_history.copy()
        
        # ユーザーメッセージを追加
        messages.append({
            "role": "user",
            "content": message
        })
        
        # APIリクエストの準備
        request_data = {
            "prompt": message, 
            "max_new_tokens": 512,
            "do_sample": True,
            "temperature": 0.7,
            "top_p": 0.9
        }
        
        # POSTリクエストのための準備
        req_data = json.dumps(request_data).encode('utf-8')
        req = urllib.request.Request(
            API_URL,
            data=req_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print("Calling custom API with payload:", json.dumps(request_data))
        
        # APIを呼び出す
        with urllib.request.urlopen(req) as response:
            response_data = response.read().decode('utf-8')
            response_body = json.loads(response_data)
        
        print("API response:", json.dumps(response_body, default=str))
        
     
        assistant_response = response_body.get('generated_text', '')
        
        # アシスタントの応答を会話履歴に追加
        messages.append({
            "role": "assistant",
            "content": assistant_response
        })
        
        # 成功レスポンスの返却
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({
                "success": True,
                "response": assistant_response,
                "conversationHistory": messages
            })
        }
        
    except URLError as e:
        print("API Connection Error:", str(e))
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "success": False,
                "error": f"Failed to connect to API: {str(e)}"
            })
        }
    except Exception as error:
        print("Error:", str(error))
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "success": False,
                "error": str(error)
            })
        }
