from GeminiAIChat.process import GET

class API:
    def __init__(self,api=None) -> None:
        self.api = api
        self.getRes = GET(self.api)

    def prompt(self,prompt):
        self.res = self.getRes.sendResponse(prompt)
        
    def response(self):
        return self.getRes.retrieveResponse(self.res.json())
