Python 3.12.2 (tags/v3.12.2:6abddd9, Feb  6 2024, 21:26:36) [MSC v.1937 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> from flask import Flask, render_template, request, redirect, url_for, flash, session
... from flask_mysqldb import MySQL
... from flask_bcrypt import Bcrypt
... from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
... 
... app = Flask(__name__)
... app.secret_key = 'your_secret_key'
... 
... # MySQL 設定
... app.config['MYSQL_HOST'] = 'your-db-host'
... app.config['MYSQL_USER'] = 'your-db-user'
... app.config['MYSQL_PASSWORD'] = 'your-db-password'
... app.config['MYSQL_DB'] = 'your-database'
... mysql = MySQL(app)
... 
... bcrypt = Bcrypt(app)
... login_manager = LoginManager(app)
... login_manager.login_view = 'login'
... 
... class User(UserMixin):
...     def __init__(self, user_id, name, email):
...         self.id = user_id
...         self.name = name
...         self.email = email
... 
... @login_manager.user_loader
... def load_user(user_id):
...     cur = mysql.connection.cursor()
...     cur.execute("SELECT UserID, Name, Email FROM Users WHERE UserID = %s", (user_id,))
...     user = cur.fetchone()
...     cur.close()
...     if user:
...         return User(user[0], user[1], user[2])
...     return None
... 
... @app.route('/register', methods=['GET', 'POST'])
... def register():
...     if request.method == 'POST':
...         name = request.form['name']
...         email = request.form['email']
...         password = request.form['password']
...         hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
... 
...         cur = mysql.connection.cursor()
...         cur.execute("INSERT INTO Users (Name, Email, PasswordHash) VALUES (%s, %s, %s)", (name, email, hashed_pw))
...         mysql.connection.commit()
...         cur.close()
...         flash("註冊成功，請登入！")
...         return redirect(url_for('login'))
...     return render_template('register.html')
... 
... @app.route('/login', methods=['GET', 'POST'])
... def login():
...     if request.method == 'POST':
...         email = request.form['email']
...         password = request.form['password']
... 
...         cur = mysql.connection.cursor()
...         cur.execute("SELECT UserID, Name, Email, PasswordHash FROM Users WHERE Email = %s", (email,))
...         user = cur.fetchone()
...         cur.close()
... 
...         if user and bcrypt.check_password_hash(user[3], password):
...             login_user(User(user[0], user[1], user[2]))
...             flash("登入成功！")
...             return redirect(url_for('dashboard'))
...         else:
...             flash("帳號或密碼錯誤")
...     return render_template('login.html')
... 
... @app.route('/dashboard')
... @login_required
... def dashboard():
    return f"歡迎 {current_user.name}，這是你的儀表板！"

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("登出成功")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
