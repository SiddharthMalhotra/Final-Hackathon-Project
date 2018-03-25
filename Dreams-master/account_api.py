# from flask import Blueprint
from flask import *
from database import mongo
import math
from database import CURRENT_USER, farmerid
account_api = Blueprint('account_api', __name__)
 
@account_api.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
   

@account_api.route('/registerfarmer', methods=['GET', 'POST'])
def registerfarmer():
    if request.method == 'GET':
        return render_template('registerfarmer.html')
    elif request.method == 'POST':
        username = request.form['txtUsername']
        name = request.form['txtName']
        password = request.form['txtPassword']
        age = request.form['txtAge']
        DOB = request.form['txtDOB']
        Location = request.form['txtLocation']
        collate = request.form['txtcollat']
        collatamt = request.form['txtcollamt']
        loanamt = request.form['txtamt']
        # TODO: Change this shit
        yield1 = float(request.form['txtyield1'])
        yield2 = float(request.form['txtyield2'])
        yield3 = float(request.form['txtyield3'])
        avg = 0.0
        
        creditscore = 0.0
        avg = float(((yield1+yield2+yield3)/3.0)/67.5)
        creditscore = float(avg+0.55)
        csflr = math.floor(creditscore)
        csciel = math.ceil(creditscore)
        if(csflr < 1 or loanamt>collatamt):
        	flash('not eligible')
        	return redirect(url_for('account_api.registerfarmer'))
        csdec = creditscore%csflr
        if(csflr == 1):
            roi = 17.5 - (2.5 * csdec)
        if(csflr == 2):
            roi = 15 - (2.5 * csdec)
        if(csflr == 3):
            roi = 12.5 - (2.5 * csdec)
        if(csflr == 4):
            roi = 10 - (2.5 * csdec)
        if(csflr >= 5):
            roi = 7.5               
        
        db = mongo['db']
        test = db['testFarm']	
        login = mongo['db']['testLogin']
        for usr in login.find():
            if usr['_id'] == username:
                flash('The username {0} is already in use.  Please try a new username.'.format(username))
                return redirect(url_for('account_api.registerfarmer'))
        test.insert({'_id': username,'name':name,'age':age,'dob':DOB,'location':Location,'cred_cs':round(creditscore,2),'yield1':yield1,'yield2':yield2,'yield3':yield3,'collateral':collate,'collateamt':collatamt,'pwd':password,'loanamount':loanamt ,'roi':round(roi,2)})
        login.insert({'_id': username,'pwd':password,'role':"farmer"}) 

        flash('You have registered the username {0}. Please login'.format(username))
        return redirect(url_for('account_api.login'))
    else:
        abort(405)

@account_api.route('/registerinvestor', methods=['GET', 'POST'])
def registerinvestor():
    if request.method == 'GET':
        return render_template('registerinvestor.html')
    elif request.method == 'POST':
        username = request.form['txtUsername']
        name = request.form['txtName']
        password = request.form['txtPassword']
        age = request.form['txtAge']
        DOB = request.form['txtDOB']
        Location = request.form['txtLocation']
        login = mongo['db']['testLogin']
        test = mongo['db']['testInv']
        for usr in login.find():
            if usr['_id'] == username:
                flash('The username {0} is already in use.  Please try a new username.'.format(username))
                return redirect(url_for('account_api.registerinvestor'))
        test.insert({'_id': username,'name':name,'age':age,'dob':DOB,'location':Location,'pwd':password})
        login.insert({'_id': username,'pwd':password,'role':"investor"}) 
            
        flash('You have registered the username {0}. Please login'.format(username))
        return redirect(url_for('account_api.login'))
    else:
        abort(405)


@account_api.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', next=request.args.get('next'))
    elif request.method == 'POST':
        username = request.form['txtUsername']
        password = request.form['txtPassword']

        user = mongo['db']['testLogin']
        for usr in user.find():
            userName = usr['_id']
            CURRENT_USER = usr['_id']
            pwd = usr['pwd']
            role = usr['role']
            ## add pages acordingly
            if(userName == username and pwd == password):
                if(role == 'farmer'):
                    usrname = usr['_id']

                    CURRENT_USER = usrname    
                    print(CURRENT_USER)          
                    flash('Welcome back farmer {0}'.format(username))
                    try:
                        
                        return redirect(url_for('account_api.farmer'))
                    except:
                        return redirect(url_for('index'))
                else:
                    flash('Welcome back investor {0}'.format(username))
                    try:
                        #next = request.form['next']
                        return redirect(url_for('account_api.investor'))
                    except:
                        return redirect(url_for('index'))
        else:
            flash('Invalid login')
            return redirect(url_for('account_api.login'))
    else:
        return abort(405)

@account_api.route('/farmer', methods=['GET','POST'])
def farmer():
    if request.method == 'GET':
        results = []
        farmers = mongo['db']['testInvestement']
        for frm in farmers.find():
            print (CURRENT_USER)
            if frm['f_id'] == CURRENT_USER:
                results.append(frm)
        return render_template('farmer.html', result = results)

@account_api.route('/investor', methods=['GET','POST'])
def investor():
    if request.method == 'GET':
        results = []
        farmers = mongo['db']['testFarm']
        for frm in farmers.find():
            for i in frm:
                for j in i:
                    j.encode('UTF-8')
            results.append(frm)
        return render_template('investor.html', result = results)

@account_api.route('/fulfiladream',methods=['GET','POST'])
def fulfiladream():
    if request.method == 'GET':
        farmerid = request.args.get("farmer_id")
        return render_template('fulfiladream.html',result = farmerid)
    elif request.method == 'POST':
        
        farmerid = request.args.get("farmer_id")
        maturity = 3 #play
        roi = 0.0
        matureamt = 0.0
        colamt = 0.0
        db = mongo['db']
        test = db['testFarm']   
        for usr in test.find():
            if usr['_id'] == farmerid:
                colamt = float(usr['collateamt'])
                loanamount = float(usr['loanamount'])
                roi = float(usr['roi'])
                investamount = 300.0#float(request.form('txtAmount')) #play
                matureamt = investamount + (investamount*roi * (12/maturity))/100
                loanamount = loanamount - investamount
                if loanamount < 0 or investamount > colamt:
                    flash('Loan can be granted/Donation cannot be made')
                    return redirect(url_for('account_api.investor'))
        inv = db['testInvestement']
        inv.insert({'f_id':farmerid,'i_id':CURRENT_USER,'amt':investamount,'timep':maturity,'roi':round(roi,2),'maturity':matureamt})
        test.update({'_id':farmerid},{ "$set": {'loanamount':loanamount}})
        return redirect(url_for('account_api.investor'))

