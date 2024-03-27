from flask import Flask,session
from flask_restful import Api,Resource
from flask_cors import *
import datetime,os
import sys

from FastCNN.prx.ValidProxy2 import insValider
from IutyLib.connectutils.tcp import TcpService
import json
"""
import api
"""
#from package.namespace.demo_ import DemoApi
from FastCNN.api.pytorchfastcnn_ import FastCNNApi


app = Flask(__name__,static_folder='static/',template_folder='static/template/')
api = Api(app)
CORS(app, supports_credentials=True)

host = '0.0.0.0'
"""
set port
"""
port = 7738


app.config['SECRET_KEY'] = 'myskey'
app.config['SESSION_COOKIE_HTTPONLY'] = False
app.config['SESSION_PERMANENT'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=30)


"""
set api url
"""
#api.add_resource(DemoApi,'/api/namespace/demo')
api.add_resource(FastCNNApi,'/api/nn/fastcnn')

def handleSocket(sender,msg,args):
    if msg == "receive":
        rtn = {"success":False}
        try:
            data = json.loads(args)
            if not "cmd" in data:
                rtn["error"] = "cmd is nesserary"
                sender.send(json.dumps(rtn))
                return
            
            if not "projectid" in data:
                rtn["error"] = "projectid is nesserary"
                sender.send(json.dumps(rtn))
                return
            
            if not "modeltag" in data:
                rtn["error"] = "modeltag is nesserary"
                sender.send(json.dumps(rtn))
                return
            
            if not "imagepath" in data:
                rtn["error"] = "imagepath is nesserary"
                sender.send(json.dumps(rtn))
                return
            data = insValider.predictYNet(data["projectid"],data["modeltag"],data["imagepath"])
            rtn["data"] = data
            rtn["success"] = True
            sender.send(json.dumps(rtn))
        except Exception as err:
            print(err)
    if msg == "connected":
        print("connected")
    pass

def main():
    s = TcpService()
    s.Port = 7638
    s.OnEvent.append(handleSocket)
    s.connect()
    app.run(host = host,port = port,debug = False)

def test():
    app.run(host = host,port = port,debug = True)

if __name__ == "__main__":
    main()
