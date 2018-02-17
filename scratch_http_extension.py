#-*- coding:utf-8 -*-
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import urllib

# 작성일: 2018.02.17 
# 작성자: 박성완(adsloader99@gmail.com)
# Scratch 2.0 http extension doc 참고했음.
# https://wiki.scratch.mit.edu/wiki/File:ExtensionsDoc.HTTP-9-11.pdf

PORT_NUMBER = 50505

# DB처럼 값을 저장하기 
DB = {}
def initDB():
    global DB
    DB = { "x" : 0, "y" : 0 }

# poll처리  
def onReq_Poll(params):
    lines = []
    lines.append('value/x ' + str (DB["x"]) )
    lines.append('value/y ' + str (DB["y"]) )
    response = '\n'.join(lines)
    
    print response        
    return response    

# reset_all처리  
# !!!!!! 가끔 flag 버튼을 누르면 호출된다.!!!! 
# 결론: flag 버튼을 누르면 기능이 완료되고 reset_all이 호출된다. 
# 통신상의 문제는 전혀없다. 컨셉이다.  
def onReq_reset_all(params):
    print "reset all 처리!"   
    initDB()

# crossdomain처리  
def onReq_crossdomain(params):
    return '<cross-domain-polocy>\n' \
                   '  <allow-access-from domain="*" to-ports="{}"/>\n' \
                   '</cross-domain-polocy>\x00'.format(50505)


# myCommand 처리   
def onReq_myCommand(params):
    response = ""
    response = ADDED_COMMANDS.get(params[0], onReq_myCommand)(params)
    return response

# myCommand 처리 - setValue  
def onReq_myCommand_setValue(params):
    response = ""
    if(params[1] == "x"):
        DB["x"] =  params[2]
                
    elif(params[1] == "y"):
        DB["y"] =  params[2]

    print DB    
    return response

# Scratch 2.0 HTTP extension 커맨드 & Handler table
BASIC_COMMANDS = {
    "crossdomain.xml" : onReq_crossdomain, 
    "poll"            : onReq_Poll,
    "reset_all"       : onReq_reset_all  
}

# 추가로 구현한 커맨드 & Handler table 
ADDED_COMMANDS = {
    "setValue" : onReq_myCommand_setValue
}

# HTTP Handler
class reqHandler(BaseHTTPRequestHandler):
	
    def do_GET(self):
        params = urllib.unquote_plus(self.path.strip('/')).split('/')
        result = self.process(params)

        self.send_response(200)
        self.end_headers()
        self.wfile.write(result)

    def process(self, params):
        response = ""
        response = BASIC_COMMANDS.get(params[0], onReq_myCommand)(params)
        return response	            	    

if __name__ == "__main__":
    
    try:
        initDB()
        server = HTTPServer(('', PORT_NUMBER), reqHandler)
        print 'Started httpserver on port ' , PORT_NUMBER
    	
        server.serve_forever()

    except KeyboardInterrupt:
        print '^C received, shutting down the web server'
        server.socket.close()
	