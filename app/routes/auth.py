from flask import Blueprint, render_template,request,redirect,url_for,flash,session

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validation
        if not all([username, email, password, confirm_password]):
            flash('All fields are required', 'danger')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters', 'danger')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return render_template('register.html')
        
        if '@' not in email:
            flash('Please enter a valid email address', 'danger')
            return render_template('register.html')
        
        # Simple registration (store in session/users dict for demo)
        if 'users' not in session:
            session['users'] = {}
        
        if username in session['users']:
            flash('Username already exists. Please choose another.', 'danger')
        else:
            # Store user (password in plain for demo only)
            session['users'][username] = {
                'password': password,
                'email': email
            }
            flash(f'Account created successfully for {username}! Please login.', 'success')
            return redirect(url_for('auth.login'))
    
    return render_template('register.html')


@auth_bp.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        # Check registered users
        users = session.get('users', {})
        
        # Check registered user
        if username in users and users[username]['password'] == password:
            session['user'] = username
            flash(f'Welcome back, {username}!', 'success')
            return redirect(url_for('tasks.view_tasks'))
        else:
            flash('Invalid credentials', 'danger')
    
    return render_template('login.html')



@auth_bp.route('/logout')
def logout():
    session.pop('user',None)
    flash('Logged Out',"info")
    return redirect(url_for('auth.login'))
