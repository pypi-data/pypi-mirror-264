import os
import httpx
from dotenv import load_dotenv
import json
load_dotenv()

class GET:
    def __init__(self,api):
        self.KEY =  f"{os.environ.get('KEY')}"
        self.API_URL =  f"{os.environ.get('API_URL') + self.KEY}"
        self.PROMPT =  f"{os.environ.get('PROMPT')}"
        self.PROMPT = json.loads(self.PROMPT)

        
    def sendResponse(self,prompt):
        self.PROMPT['contents'][0]['parts'][0]['text'] = prompt
        self.response = httpx.post(
            self.API_URL,
              headers={'Content-Type': 'application/json'},
              json=self.PROMPT)
        return self.response

    def retrieveResponse(self,response):
        try:
            return response['candidates'][0]['content']['parts'][0]['text']
        except:
            return {"message":"violat gemini ai safety rules"}