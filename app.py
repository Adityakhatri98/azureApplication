from flask import Flask
from flask import request, render_template
import os
from werkzeug import secure_filename
import csv
import pandas as pd
import warnings
from flask import Flask
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
app = Flask(__name__)


UPLOAD_FOLDER = 'static/uploadFile/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
import glob





@app.route('/aaa')
def hello_world():
    return 'Hello World!'

@app.route('/',methods=['GET'])
def check():
    return render_template("welcome.html")


@app.route('/uploadPage')
def uploadPage():

    # print("hi")
    return render_template('/multipleupload.html')

@app.route('/uploadFile',methods=['GET', 'POST'])
def upload():

    img=request.files.getlist('fileUpload')
    for file in img:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

    return render_template('/multipleupload.html',msg="File Uploaded Sucessfully..............")

@app.route('/searchPage')
def searchPage():
    return render_template('/search.html')

@app.route('/searchname',methods=['Post'])
def search():
    name = request.form['name']
    reader = csv.DictReader(open("static/uploadFile/people.csv"))
    dirPath = UPLOAD_FOLDER
    print(dirPath)
    for raw in reader:
        print(raw)
        if (name == raw['name']):
            dirPath= "static/uploadFile/" +raw['picture']
            print(raw['name'])
    if(dirPath != UPLOAD_FOLDER):
        print(dirPath)
    else:
        print("IMAGE NOT FOUND IN DATABASE")
    print(name)

    return render_template("/search.html", path=dirPath,msg="found",error="Image Not Found")

@app.route('/editSearch')
def editSearch():
    return render_template('/editSearch.html')


@app.route('/edit',methods=['Post'])
def edit():
    name = request.form['name']
    reader = csv.DictReader(open("static/uploadFile/people.csv"))
    dirPath = UPLOAD_FOLDER
    record=''
    print(dirPath)
    for raw in reader:

        if (name == raw['name']):
            record = raw
    return render_template("/edit.html", data=record)


@app.route('/editDetails',methods=['Post'])
def editDetails():
   f = open("static/uploadFile/people.csv", "r")
   csvr=csv.reader(f)
   found=0
   m1=[]
   name = request.form['name']
   salary = request.form['salary']
   room = request.form['room']
   telnum = request.form['telnum']
   picture = request.form['picture']
   Keywords = request.form['Keywords']
   for r in csvr:
       if(r[0]==name):
           r[0] = name
           r[1] = salary
           r[2] = room
           r[3] = telnum
           r[4] = picture
           r[5] = Keywords
           found=1
       m1.append(r)
   f.close()
   if(found==0):
       print("Data not found")
   else:
       f=open("static/uploadFile/people.csv", "w",newline='')
       csvr=csv.writer(f)
       csvr.writerows(m1)
       f.close()

   return render_template("/editSearch.html",msg="Record Updated sucessfully...........")


if __name__ == '__main__':
    app.run()
