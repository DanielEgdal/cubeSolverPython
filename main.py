from flask import Flask,render_template,request
import os
from wsgiref.simple_server import make_server
import pickle
from cube2 import solveScrambleAllDRAxis,solveScrambleAllDRAxisExtraDRStep,getFromEOToDRPrune,getFromDRPrune


from flask import Flask,render_template,request

print("loading files")
 # Prune to finish cube
if os.path.exists('fromDRPrune.pickle'):
    with open('fromDRPrune.pickle','rb') as f:
        fromDRPrune = pickle.load(f)
else:
    print('first time, genning prune table to finish the cube. Should take like 5 sec with pypy')
    fromDRPrune =getFromDRPrune()
    with open('fromDRPrune.pickle','wb') as f:
        pickle.dump(fromDRPrune,f)

# Prune to fast DR
if os.path.exists('fromEOToDRPrune.pickle'):
    with open('fromEOToDRPrune.pickle','rb') as f:
        fromEOToDRPrune = pickle.load(f)
else:
    print('first time, genning prune table to get EO -> DR. Should take like 5 sec with pypy')
    fromEOToDRPrune =getFromEOToDRPrune()
    with open('fromEOToDRPrune.pickle','wb') as f:
        pickle.dump(fromEOToDRPrune,f)
 
app = Flask(__name__)
print("starting server")
@app.route('/')
def form():
    return render_template('form.html')
 
@app.route('/data/', methods = ['POST', 'GET'])
def data():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        form_data = request.form
        scram = form_data["Scramble"]
        if request.form["substepDR"] == '1':
            solutions = solveScrambleAllDRAxisExtraDRStep(scram,fromEOToDRPrune,fromDRPrune)
        else:
            solutions = solveScrambleAllDRAxis(scram,fromEOToDRPrune,fromDRPrune)
        # print(form_data)
        # print(solutions)
        return render_template('data.html',solutions = solutions,scramble=scram)
 
 
# app.run(host="172.31.120.34", port=8000)
# app.run(host="localhost", port=8000)
# app.run(host="0.0.0.0", port=4000)

with make_server('',8000,app) as server:
    print('serving on port 8000...\nvisit http://127.0.0.1:8000\nTo exit press ctrl + c')
    server.serve_forever()