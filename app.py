import os
from flask import Flask,render_template,request, redirect
app = Flask(__name__)

app.vars = {}
f1, f2, f3, f4 = ['Open','Close','High','Low']

# create a dict of questions
app.questions = {}
app.questions['How many eyes do you have?']=('1','2','3')
app.questions['Which fruit do you like best?']=('banana','mango','pineapple')
app.questions['Do you like cupcakes?']=('yes','no','maybe')

app.nquestions = len(app.questions)

@app.route('/',methods=['GET','POST'])
def homepg():
    return redirect('/index')

@app.route('/index',methods=['GET','POST'])
def index():
    nquestions= app.nquestions
    if request.method == 'GET':
        return render_template('userinfo.html',num=nquestions)
    else:
        #request was a POST
        app.vars['name'] = request.form['name']
        app.vars['age'] = request.form['age']
        
        f = open('%s_%s.txt'%(app.vars['name'],app.vars['age']),'w')
        f.write('Name: %s\n'%(app.vars['name']))
        f.write('Age: %s\n\n'%(app.vars['age']))
        f.close()
        
        return redirect('/main')

@app.route('/main')
def main2():
    if len(app.questions) == 0: return render_template('end.html')
    return redirect('/next')

#####################################
## IMPORTANT: I have separated /next INTO GET AND POST
## You can also do this in one function, with If and Else
## The attribute that contains GET and POST is: request.method
#####################################

@app.route('/next',methods=['GET'])
def next(): #remember the function name does not need to match the URL
    # for clarity (temp variables)
    n = app.nquestions - len(app.questions) + 1
    q = list(app.questions.keys())[0] #python indexes at 0
    a1, a2, a3 = list(app.questions.values())[0] #this will return the answers corresponding to q
    
    # save the current question key
    app.currentq = q
    
    return render_template('layout.html',num=n,question=q,ans1=a1,ans2=a2,ans3=a3)

@app.route('/next',methods=['POST'])
def next2():  #can't have two functions with the same name
    # Here, we will collect data from the user.
    # Then, we return to the main function, so it can tell us whether to
    # display another question page, or to show the end page.
    
    f = open('%s_%s.txt'%(app.vars['name'],app.vars['age']),'a') #a is for append
    f.write('%s\n'%(app.currentq))
    f.write('%s\n\n'%(request.form['answer_from_layout'])) #this was the 'name' on layout.html!
    f.close()
    
    # Remove question from dictionary
    del app.questions[app.currentq]
    
    return redirect('/main')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
