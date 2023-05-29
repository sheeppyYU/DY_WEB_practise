from flask import Flask, render_template, request, redirect, url_for, flash, session  
import pymysql, os
from datetime import datetime 
from functools import wraps

# 創建 Flask 應用程序
app = Flask(__name__) # 建立物件
app.secret_key = os.urandom(24)

# 把確認有沒有session包成裝飾器
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'acc' not in session: 
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# 資料庫連接設定
connect = pymysql.connect(host = '127.0.0.1',
                          user = 'ming',
                          password = '',
                          db = 'pydb',
                          charset = 'utf8',
                          cursorclass = pymysql.cursors.DictCursor)

# 登入頁面路由
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':  # 如果是POST請求，則處理表單提交
        account = request.form.get('account')  # 獲取帳號
        password = request.form.get('password')  # 獲取密碼

        with connect.cursor() as cursor:
            sql = "SELECT * FROM account WHERE acc_nu = %s AND passwd = %s"
            cursor.execute(sql, (account, password))  # 從資料庫查詢該帳號和密碼
            login_result = cursor.fetchone()  # 獲取查詢結果

        # 如果查詢結果不為None，且帳號和密碼正確，則登入成功，重定向到index頁面
        if login_result is not None and login_result['acc_nu'] == account and login_result['passwd'] == password:
            session['acc'] = account  
            return redirect(url_for('index'))  

        # 如果帳號或密碼為空，則顯示錯誤信息
        elif not account or not password:
            flash('帳密不能為空', 'error')
        else:  # 如果帳號或密碼錯誤，則顯示錯誤信息
            flash('帳密輸入錯誤', 'error')

    return render_template('login.html')  # 如果是GET請求或者登入失敗，顯示登入頁面


# index頁面路由
@login_required
@app.route('/index', methods=['GET', 'POST'])  

def index():
    if 'acc' not in session:  # 如果用戶未登入，重定向到登入頁面
        return redirect(url_for('login'))

    with connect.cursor() as cursor:
        cursor.execute("SELECT * FROM work_schedule")  # 查詢所有工作排程
        work = cursor.fetchall()  # 獲取查詢結果
        print(work)

    with connect.cursor() as cursor:
        cursor.execute("SELECT * FROM end_work")  # 查詢結案工作
        finish_work = cursor.fetchall()  # 獲取查詢結果


    return render_template('index.html', work=work , finish_work=finish_work)  # 渲染index頁面，將工作排程傳遞給index頁面


# 顯示大項目路由
@login_required
@app.route('/work_item/<SID>', methods=['GET', 'POST'])  
def work_item(SID):
    with connect.cursor() as cursor:
        cursor.execute("SELECT * FROM project_option WHERE SID = %s",(SID,))  # 查詢所有工作排程
        project_option = cursor.fetchall()  # 獲取查詢結果
        print("AAAAAAAAAAAAAAA",project_option)

    return render_template('work_item.html',SID=SID,project_option=project_option)  #




if __name__ == '__main__':
    app.run(debug=True,port=5000)  # 運行Flask應用



