from flask import Blueprint

account_api = Blueprint('account_api', __name__)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    HomeFolder = db.Column(db.String)
    ShellType = db.Column(db.String)
    privilege = db.Column(db.String)

@login_manager.user_loader
def user_loader(user_id):
    user = User.query.filter_by(id=user_id)
    if user.count() == 1:
        return user.one()
    return None

@account_api.before_first_request
def init_request():
    db.create_all()

@account_api.route('/options', methods=['GET', 'POST'])
@login_required
def options():
    if request.method == 'GET':
        users = User.query.all()
        return render_template('options.html',test=users)
       
    elif request.method == 'POST':
        id = request.form['txtid']
        user = User.query.filter_by(id=id)
        db.session.delete(user.one())
        
        #a = db.session.query(Submission).filter_by(username=username,password=password).count()
        db.session.commit()
        flash('You have deleted the username')
        return redirect(url_for('logout'))
        
        
    else:
        abort(405)



    
@account_api.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@account_api.route('/signup', methods=['GET','SET'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        username = request.form['txtUsername']
        name = request.form('txtName')
        password = request.form['txtPassword']
        age = request.form['txtAge']
        DOB = request.form['txtDOB']
        Location = request.form['txtLocation']
        user = User.query.filter_by(username=username).filter_by(password=password)
        if user.count() == 0:
            user = User(username=username, password=password, HomeFolder=HomeFolder, ShellType=ShellType, privilege=privilege)
            db.session.add(user)
            db.session.commit()
            #session['user']=username
            test = mongo.db.testFarm
            test.insert({'_id': username,'name':name,'age':age,'dob':DOB,'location':Location,'pwd':password})
            #mongoDB
            

            #
            flash('You have registered the username {0}. Please login'.format(username))
            return redirect(url_for('login'))
        else:
            flash('The username {0} is already in use.  Please try a new username.'.format(username))
            return redirect(url_for('signup'))
        

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
        yield1 = float(request.form['txtyield1'])
        yield2 = float(request.form['txtyield2'])
        yield3 = float(request.form['txtyield3'])
        avg = 0.0
        
        creditscore = 0.0
        avg = float(((yield1+yield2+yield3)/3.0)/67.5)
        creditscore = float(avg+0.55)
                        
        user = User.query.filter_by(username=username).filter_by(password=password)
        
        test = mongo.db.testFarm
        login = mongo.db.testLogin
        for usr in test.find():
            if usr['_id'] == username:
                flash('The username {0} is already in use.  Please try a new username.'.format(username))
                return redirect(url_for('registerfarmer'))
        test.insert({'_id': username,'name':name,'age':age,'dob':DOB,'location':Location,'cred_cs':creditscore,'yield1':yield1,'yield2':yield2,'yield3':yield3,'pwd':password})
        login.insert({'_id': username,'pwd':password,'role':"farmer"}) 
            #mongoDB
            #session['user']=username
        flash('You have registered the username {0}. Please login'.format(username))
        return redirect(url_for('login'))
        # else:
        #     flash('The username {0} is already in use.  Please try a new username.'.format(username))
        #     return redirect(url_for('register'))
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
        login = mongo.db.testLogin
        test = mongo.db.testInv
        for usr in test.find():
            if usr['_id'] == username:
                flash('The username {0} is already in use.  Please try a new username.'.format(username))
                return redirect(url_for('registerinvestor'))
        test.insert({'_id': username,'name':name,'age':age,'dob':DOB,'location':Location,'pwd':password})
        login.insert({'_id': username,'pwd':password,'role':"farmer"}) 
            
        flash('You have registered the username {0}. Please login'.format(username))
        return redirect(url_for('login'))
        # else:
        #     flash('The username {0} is already in use.  Please try a new username.'.format(username))
        #     return redirect(url_for('register'))
    else:
        abort(405)


@account_api.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', next=request.args.get('next'))
    elif request.method == 'POST':
        username = request.form['txtUsername']
        password = request.form['txtPassword']

        #user = User.query.filter_by(username=username).filter_by(password=password)
        user = mongo.db.testLogin
        for usr in user.find():
            userName = usr['_id']
            pwd = usr['pwd']
            role = usr['role']
            ## add pages acordingly
            if(userName == username and pwd == password):
                if(role == 'farmer'):
                    usrname = usr['_id']
                        # csflr = math.floor(creditscore)
                        # csciel = math.ceil(creditscore)
                        # csdec = creditscore%csflr
                        # if(csflr < 1):
                        #     flash('not eligible')
                        # if(csflr == 1):
                        #     roi = 17.5 - (2.5 * csdec)
                        # if(csflr == 2):
                        #     roi = 15 - (2.5 * csdec)
                        # if(csflr == 3):
                        #     roi = 12.5 - (2.5 * csdec)
                        # if(csflr == 4):
                        #     roi = 10 - (2.5 * csdec)
                        # if(csflr >= 5):
                        #     roi = 7.5

                        
                    flash('Welcome back farmer {0}'.format(username))
                    try:
                        next = request.form['next']
                        return redirect(next)
                    except:
                        return redirect(url_for('index'))
                else:
                    flash('Welcome back investor {0}'.format(username))
                    try:
                        next = request.form['next']
                        return redirect(next)
                    except:
                        return redirect(url_for('index'))
        # if user.count() == 1:
        #     login_user(user.one())
        #     flash('Welcome back {0}'.format(username))
        #     try:
        #         next = request.form['next']
        #         return redirect(next)
        #     except:
        #         return redirect(url_for('index'))
        else:
            flash('Invalid login')
            return redirect(url_for('login'))
    else:
        return abort(405)

@account_api.route('/modify', methods=['GET', 'POST'])
def modify():
    if request.method == 'GET':
        return render_template('modify.html')
    elif request.method == 'POST':
        username = request.form['xUsername']
        password = request.form['xPassword']
        HomeFolder = request.form['xHomeFolder']
        ShellType = request.form['xShellType']
        privilege = request.form['xprivilege']
        id=request.form['txtid']
        user = User.query.filter_by(username=username).filter_by(password=password)
        if user.count() == 1:
            user = User(username=username, password=password, HomeFolder=HomeFolder, ShellType=ShellType, privilege=privilege)
            db.session.delete(user.one())
            db.session.add(user)
            db.session.commit()
            #session['user']=username
            flash('You have registered the username {0}. Please login'.format(username))
            return redirect(url_for('modify'))
        else:
            flash('The username {0} is already in use.  Please try a new username.'.format(username))
            return redirect(url_for('modify'))
    else:
        abort(405)