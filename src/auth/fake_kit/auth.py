
## This will be our "Backend Authentication system".

from apiserver import ApiServer, ApiRoute

class MyServer(ApiServer): 
        @ApiRoute("/popup")
        def addbar(req):
            return {"boo":req["bar"]+1}

        @ApiRoute("/baz")
        def justret(req):
            if req:
                 raise ApiError(501,"no data in for baz")
            return {"obj":1}

MyServer("127.0.0.1",8000).serve_forever()