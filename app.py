from flask import Flask, render_template, request, redirect, url_for, flash, session
import pymysql
import os
from datetime import datetime
from functools import wraps
import json

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 創建 Flask 應用程序
app = Flask(__name__)  # 建立物件
app.secret_key = os.urandom(24)

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 把確認有沒有session包成裝飾器
def login_required(f):
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'acc_nu' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#當發生404錯誤時，跳轉404.html
@app.errorhandler(404)
def errorhandler(e):
    return render_template("404.html"), 404
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 資料庫連接設定
connect = pymysql.connect(host='127.0.0.1',
                          user='root',
                          password='',
                          db='pydb',
                          charset='utf8',
                          cursorclass=pymysql.cursors.DictCursor)

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 登入頁面路由

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':  # 如果是POST請求，則處理表單提交
        account = request.form.get('acc_nu')  # 獲取帳號
        password = request.form.get('passwd')  # 獲取密碼

        with connect.cursor() as cursor:
            sql = "SELECT * FROM account WHERE acc_nu = %s AND passwd = %s"
            cursor.execute(sql, (account, password))  # 從資料庫查詢該帳號和密碼
            acc_data = cursor.fetchone()  # 獲取查詢結果

        # 如果查詢結果不為None，且帳密和密碼正確，則登入成功，重定向到index頁面
        if acc_data is not None and acc_data['acc_nu'] == account and acc_data['passwd'] == password:
            session['acc_nu'] = account
            return redirect(url_for('index'))

        # 如果帳號或密碼為空，則顯示錯誤信息
        elif not account or not password:
            flash('帳密不能為空', 'error')
            return render_template('login.html')

        else:  # 如果帳號或密碼錯誤，則顯示錯誤信息
            flash('帳密輸入錯誤', 'error')
            return render_template('login.html')

    else:
        return render_template('login.html')  # 如果是GET請求或者登入失敗，顯示登入頁面

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# index頁面路由

@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    with connect.cursor() as cursor:
        cursor.execute("SELECT * FROM work_schedule WHERE state = 0")  # 查詢所有工作排程
        work = cursor.fetchall()  # 獲取查詢結果

    with connect.cursor() as cursor:
        cursor.execute("SELECT * FROM work_schedule WHERE state = 1")  # 查詢結案工作
        finish_work = cursor.fetchall()  # 獲取查詢結果




    # 渲染index頁面，將工作排程傳遞給index頁面
    return render_template('index.html', work=work, finish_work=finish_work)

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 修改密碼畫面跟處理

@app.route('/chg_passwd', methods=['GET', 'POST'])
@login_required
def chg_passwd():

    if request.method == 'POST':
        account = session.get('acc_nu')
        old_passwd = request.form.get('old_passwd')
        new_passwd = request.form.get('new_passwd')
        check_passwd = request.form.get('check_passwd')

        with connect.cursor() as cursor:
            sql = "SELECT * FROM account WHERE acc_nu = %s AND passwd = %s"
            cursor.execute(sql, (account, old_passwd))
            acc_data = cursor.fetchone()

        # 如果查詢結果不為None，且查詢帳號 = 輸入帳號，且查詢密碼 = 輸入密碼
        if acc_data is not None and acc_data['acc_nu'] == account and acc_data['passwd'] == old_passwd:
            # 如果輸入新密碼 = 檢查密碼
            if new_passwd == check_passwd:
                with connect.cursor() as cursor:
                    sql = "UPDATE account SET passwd = %s WHERE acc_nu = %s"
                    cursor.execute(sql, (check_passwd, account))
                    connect.commit()

                    return redirect(url_for('index'))

            else:
                flash('新密碼不相同', 'error')
                return redirect(url_for('chg_passwd'))
        else:
            flash('帳號或密碼輸入錯誤', 'error')
            return redirect(url_for('chg_passwd'))
    else:
        return render_template('chg_passwd.html')

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 跳到帳戶管理

@app.route('/account_manage')
@login_required
def account_manage():

    with connect.cursor() as cursor:
        cursor.execute("SELECT * FROM account")
        display_acc = cursor.fetchall()

    return render_template('account_manage.html', display_acc=display_acc)

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 刪除帳號

@app.route('/delete/<acc_nu>')
@login_required
def delete(acc_nu):

    with connect.cursor() as cursor:
        sql = "DELETE FROM account WHERE acc_nu = %s"
        cursor.execute(sql, (acc_nu,))
        connect.commit()

    return redirect(url_for('account_manage'))

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 修改帳戶和處理

@app.route('/chg_account/<acc_nu>', methods=['GET', 'POST'])
@login_required
def chg_account(acc_nu):

    if request.method == 'POST':
        passwd = request.form.get('passwd')
        name = request.form.get('name')
        department = request.form.get('department')
        limits = request.form.get('limits')

        with connect.cursor() as cursor:
            sql = "UPDATE account SET passwd = %s, name = %s, department = %s, limits = %s WHERE acc_nu = %s"
            cursor.execute(sql, (passwd, name, department, limits, acc_nu))
            connect.commit()

        return redirect(url_for('account_manage'))
    else:
        with connect.cursor() as cursor:
            sql = "SELECT *FROM account WHERE acc_nu = %s"
            cursor.execute(sql, (acc_nu,))
            display_acc = cursor.fetchone()

        if display_acc:
            return render_template('chg_account.html', user=display_acc)
        else:
            return redirect(url_for('account_manage'))

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 建立帳戶和處理

@app.route('/add_account', methods=['GET', 'POST'])
@login_required
def add_account():

    if request.method == 'POST':
        acc_nu = request.form.get('acc_nu')
        passwd = request.form.get('passwd')
        name = request.form.get('name')
        department = request.form.get('department')
        limits = request.form.get('limits')

        with connect.cursor() as cursor:
            sql = "INSERT INTO account (acc_nu, passwd, name, department, limits) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (acc_nu, passwd, name, department, limits))
            connect.commit()

        return redirect(url_for('account_manage'))
    else:
        return render_template('add_account.html')

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 登出
@app.route('/logout')
def logout():

    # 清除 session 中的所有的值
    session.clear()
    return redirect(url_for('login'))

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 新增專案和處理

@app.route('/add_project', methods = ['GET', 'POST'])
@login_required
def add_project():

    if request.method == 'POST':
       
        SID = request.form.get('SID')
        project_name = request.form.get('project_name')
        work_mode = request.form.get('work_mode')
        start_time = request.form.get('start_time')
        expected_end_time = request.form.get('expected_end_time')
        end_time = request.form.get('end_time')
        date1 = datetime.strptime(start_time, '%Y-%m-%d')
        date2 = datetime.strptime(expected_end_time, '%Y-%m-%d')
        date3 = ''
        estimated_working_day = (date2 - date1).days
        actual_working_day = ''
        remark = request.form.get('remark')

        if end_time:
            date3 = datetime.strptime(end_time, '%Y-%m-%d')
            actual_working_day = (date3 - date1).days

        try:
            with connect.cursor() as cursor:
                sql = "INSERT INTO work_schedule (SID, project_name, work_mode, start_time, expected_end_time, end_time, estimated_working_day, actual_working_day, state, remark) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (SID, project_name, work_mode, start_time, expected_end_time, end_time, estimated_working_day, actual_working_day, 0, remark))
                connect.commit()                   
        except:
            print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
            SID_error = "專案代號重複，請重新填寫"
            return render_template('add_project.html', SID_error=SID_error)

        return redirect(url_for('index'))

    else:
        return render_template('add_project.html')



# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 刪除專案

@app.route('/delete_work/<SID>')
@login_required
def delete_work(SID):

    with connect.cursor() as cursor:
        sql = "DELETE FROM work_schedule WHERE SID = %s"
        cursor.execute(sql, (SID,))
        connect.commit()

    return redirect(url_for('index'))

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 修改專案和處理

@app.route('/chg_project/<SID>', methods=['GET', 'POST'])
@login_required
def chg_project(SID):

    if request.method == 'POST':
        project_name = request.form.get('project_name')
        work_mode = request.form.get('work_mode')
        start_time = request.form.get('start_time')
        expected_end_time = request.form.get('expected_end_time')
        end_time = request.form.get('end_time')
        date1 = datetime.strptime(start_time, '%Y-%m-%d')
        date2 = datetime.strptime(expected_end_time, '%Y-%m-%d')
        date3 = ''
        estimated_working_day = (date2 - date1).days
        actual_working_day = ''
        remark = request.form.get('remark')

        if end_time:
            date3 = datetime.strptime(end_time, '%Y-%m-%d')
            actual_working_day = (date3 - date1).days

        with connect.cursor() as cursor:
            sql = "UPDATE work_schedule SET project_name = %s, work_mode = %s, start_time = %s, expected_end_time = %s, end_time = %s, estimated_working_day = %s, actual_working_day = %s, remark = %s WHERE SID = %s"
            cursor.execute(sql, (project_name, work_mode, start_time, expected_end_time,
                           end_time, estimated_working_day, actual_working_day, remark, SID))
            connect.commit()

        return redirect(url_for('index'))
    else:
        with connect.cursor() as cursor:
            sql = "SELECT * FROM work_schedule WHERE SID = %s"
            cursor.execute(sql, (SID))
            work = cursor.fetchone()

        if work:
            start_time = datetime.strptime(work['start_time'], '%Y-%m-%d')
            expected_end_time = datetime.strptime(
                work['expected_end_time'], '%Y-%m-%d')
            date1 = start_time.strftime('%Y-%m-%d')
            date2 = expected_end_time.strftime('%Y-%m-%d')

            if work.get('end_time'):
                end_time = datetime.strptime(work['end_time'], '%Y-%m-%d')
                date3 = end_time.strftime('%Y-%m-%d')
            else:
                date3 = ''

            return render_template('chg_project.html', project=work, date1=date1, date2=date2, date3=date3)
        else:
            return redirect(url_for('index'))

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# "顯示"大項目路由

@app.route('/work_option/<SID>', methods=['GET', 'POST'])
@login_required
def work_option(SID):

    with connect.cursor() as cursor:
        cursor.execute(
            "SELECT project_name FROM work_schedule WHERE SID = %s ", (SID,))   # 查詢所有工作排程
        SID_name = cursor.fetchone()  # 獲取查詢結果

    session['SID'] = SID
    session['SID_name'] = SID_name
    with connect.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM project_option WHERE SID = %s ORDER BY option_id ASC", (SID,))   # 查詢所有工作排程
        project_option = cursor.fetchall()  # 獲取查詢結果

    project_order = ['前期規劃', '現場工程', '設備吊裝', '貨櫃預置工程', '機電現場工程', '貨櫃現場工程', '廠區現場工程']
    try:
        project_option.sort(key=lambda x: project_order.index(x['option_value']))
    except:
        ''
    

# 計算大項目完成%數，顯示在work_schedule----------------------------------------------
    all_work_schedule_percentage=0
    for i in project_option:
        all_work_schedule_percentage += i["option_percentage"]
    try:
        work_schedule_percentage = round(all_work_schedule_percentage / len(project_option))

    except:
        work_schedule_percentage = 0
    with connect.cursor() as cursor:
        sql = "UPDATE work_schedule SET percent_complete = %s WHERE SID = %s"
        cursor.execute(sql, (work_schedule_percentage, SID))
        connect.commit()

    return render_template('work_option.html', SID=SID, project_option=project_option, SID_name=SID_name)

#  大項目"刪除"路由-------------------------------------------------------------------------------------------------------

@app.route('/delete_option/<option_id>', methods=['GET'])
@login_required
def delete_option(option_id):

    SID=session.get('SID')  # 取得專案名字
    with connect.cursor() as cursor:
        sql = f"DELETE FROM project_option WHERE option_id = %s"

        try:
            cursor.execute(sql, (option_id))
            print("成功刪除")
        except Exception as e:
            print("刪除失敗:", e)
            ''

        connect.commit()

    return redirect(url_for('work_option', SID=SID))
    # return render_template('work_option.html', SID=SID)  #


# "建立"大項目路由-----------------------------------------------------------------

@app.route('/add_work_option/<SID>', methods=['GET', 'POST'])
@login_required
def add_work_option(SID):


    with connect.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM project_option WHERE SID = %s ORDER BY option_id ASC", (SID,))   # 查詢所有工作排程
        project_option = cursor.fetchall()  # 獲取查詢結果

    project_option_json = json.dumps(project_option)  # 轉為JSON ，用於JS判斷是否已重複

    option_value = request.form.get('option')
    option_start_time = request.form.get('option_start_time')
    option_end_time = request.form.get('option_end_time')


    if request.method == 'POST':  # 如果是POST請求，則處理表單提交
        with connect.cursor() as cursor:

            sql = f"INSERT INTO project_option (option_id, option_value, SID, option_percentage, option_start_time, option_end_time) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, ('', option_value, SID, '',
                           option_start_time, option_end_time))
            connect.commit()
        return redirect(url_for('work_option', SID=SID))

    return render_template('add_work_option.html', project_option=project_option, SID=SID, project_option_json=project_option_json)  #


# # "點擊"大項目進入小項目路由----------------------------------------------------------------------------------------------------------

@app.route('/add_option_item/<option_id>', methods=['GET', 'POST'])
@login_required
def add_option_item(option_id):

    try:
        session['option_name'] = False
        session['option_id'] = False
    except:
        print("session['option_name']=空的")

    session['option_id'] = option_id
    with connect.cursor() as cursor:
        sql = f"SELECT option_value FROM project_option WHERE option_id = %s"
        cursor.execute(sql, (option_id,))
        option_name = cursor.fetchone()
        session['option_name'] = option_name

    if 'SID' in session:
        option_name = session.get('option_name')  # 取得專案名字
    else:
        return redirect(url_for('index'))

    with connect.cursor() as cursor:

        sql = f"SELECT * FROM option_item WHERE item_id = %s ORDER BY item_id ASC"
        cursor.execute(sql, (option_id,))
        option_item = cursor.fetchall()
        
        if option_item:
            SID = option_item[0]['SID']

            return render_template('add_option_item.html', option_id=option_id, option_item=option_item, SID=SID, option_name=option_name)
        else:
            SID = session.get('SID')
            return render_template('add_option_item.html', SID=SID,  option_name=option_name)


# "儲存"小項目路由----------------------------------------------------------------------------------------------------------

@app.route('/item_save/', methods=['POST'])
@login_required
def item_save():

    delete_id=[]
    data = json.loads(request.form.get('data'))
    old_data = data.get('old', [])
    # print("old_data old_data old_data:",old_data)
    new_data = data.get('new', [])
    percentage = request.form.get('percentage')
    option_id = session.get('option_id')
    SID = session.get('SID')




    with connect.cursor() as cursor:
        sql = f"SELECT * FROM option_item WHERE item_id = %s ORDER BY item_id ASC"
        cursor.execute(sql, (option_id,))
        all_option_item = cursor.fetchall()
        print('AAAAAAAAAAAAAAAAAA',all_option_item)

# ---------------------
    
    with connect.cursor() as cursor:
        
        for old_item in old_data:
            id = old_item['id'].replace('old', '')
            print("現在有的id=",id) 
            delete_id.append(id)
            sql = "UPDATE `option_item` SET `item_value`=%s, `is_checked`=%s WHERE `id`=%s"
            cursor.execute(sql, (old_item['value'], old_item['checked'], id))

        for new_item in new_data:
            id = new_item['id'].replace('new', '')
            # print("idididid=", id)
            sql = "INSERT INTO `option_item` (`item_id`, `item_value`, `is_checked`, `SID`) VALUES (%s, %s, %s, %s)"
            cursor.execute(
                sql, (option_id, new_item['value'], new_item['checked'], SID))

        sql = "UPDATE `project_option` SET `option_percentage`=%s WHERE `option_id`=%s"
        cursor.execute(sql, (percentage, option_id))

    connect.commit()

    target_ids = [item['id'] for item in all_option_item if str(item['id']) not in delete_id]
    print("target_ids===",target_ids)

    for i in target_ids:
        print(i)#這是要刪掉的ID
        with connect.cursor() as cursor:
            sql = "DELETE FROM `option_item` WHERE `id`=%s"
            cursor.execute(sql, (i))


    connect.commit()



    return redirect(url_for('work_option', SID=SID))

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# 首頁-進行中專案轉去結案

@app.route('/finish_project/<SID>', methods=['GET', 'POST'])
@login_required
def finish_project(SID):
    with connect.cursor() as cursor:
        sql = "UPDATE work_schedule set state = %s WHERE SID = %s"
        cursor.execute(sql, (1,SID))
        connect.commit()


    return redirect(url_for('index'))

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    # app.run(debug=True, port=5000)  # 運行Flask應用
    app.run(debug=True, host="0.0.0.0", port=5000)
























































#                    ___====-_  _-====___
#              _--^^^     //      \\     ^^^--_
#           _-^          // (    ) \\          ^-_
#          -            //  |\^^/|  \\            -
#        _/            //   (@::@)   \\            \_
#       /             ((     \\//     ))             \
#      -               \\    (oo)    //               -
#     -                 \\  / VV \  //                 -
#    -                   \\/      \//                   -
#   _ /|          /\      (   /\   )      /\          |\ _
#   |/ | /\ /\ /\/  \ /\  \  |  |  /  /\ /  \/\ /\ /\ | \|
#     |/  V  V     V  \ \| |  | |/ /  V   '  V  V  \|  '
#      `   `  `      `   / | |  | | \   '      '  '   '
#                       (  | |  | |  )
#                      __\ | |  | | /__
#                     (vvv(VVV)(VVV)vvv)
#                     神獸保佑，程式碼沒Bug!


#                                             __----~~~~~~~~~~~------___
#                                     .  .   ~~//====......          __--~ ~~
#                     -.            \_|//     |||\\  ~~~~~~::::... /~
#                  ___-==_       _-~o~  \/    |||  \\            _/~~-
#          __---~~~.==~||\=_    -_--~/_-~|-   |\\   \\        _/~
#      _-~~     .=~    |  \\-_    '-~7  /-   /  ||    \      /
#    .~       .~       |   \\ -_    /  /-   /   ||      \   /
#   /  ____  /         |     \\ ~-_/  /|- _/   .||       \ /
#   |~~    ~~|--~~~~--_ \     ~==-/   | \~--===~~        .\
#            '         ~-|      /|    |-~\~~       __--~~
#                        |-~~-_/ |    |   ~\_   _-~            /\
#                             /  \     \__   \/~                \__
#                         _--~ _/ | .-~~____--~-/                  ~~==.
#                        ((->/~   '.|||' -_|    ~~-/ ,              . _||
#                                   -_     ~\      ~~---l__i__i__i--~~_/
#                                   _-~-__   ~)  \--______________--~~
#                                 //.-~~~-~_--~- |-------~~~~~~~~
#                                        //.-~~~--\
#                                 神獸保佑，程式碼沒Bug!


#                                  |~~~~~~~|
#                                  |       |
#                                  |       |
#                                  |       |
#                                  |       |
#                                  |       |
#       |~.\\\_\~~~~~~~~~~~~~~xx~~~         ~~~~~~~~~~~~~~~~~~~~~/_//;~|
#       |  \  o \_         ,XXXXX),                         _..-~ o /  |
#       |    ~~\  ~-.     XXXXX`)))),                 _.--~~   .-~~~   |
#        ~~~~~~~`\   ~\~~~XXX' _/ ';))     |~~~~~~..-~     _.-~ ~~~~~~~
#                 `\   ~~--`_\~\, ;;;\)__.---.~~~      _.-~
#                   ~-.       `:;;/;; \          _..-~~
#                      ~-._      `''        /-~-~
#                          `\              /  /
#                            |         ,   | |
#                             |  '        /  |
#                              \/;          |
#                               ;;          |
#                               `;   .       |
#                               |~~~-----.....|
#                              | \             \
#                              | /\~~--...__    |
#                             (|  `\       __-\|
#                             ||    \_   /~    |
#                             |)     \~-'      |
#                              |      | \      '
#                              |      |  \    :
#                               \     |  |    |
#                                |    )  (    )
#                                 \  /;  /\  |
#                                 |    |/   |
#                                 |    |   |
#                                  \  .'  ||
#                                  |  |  | |
#                                  (  | |  |
#                                  |   \ \ |
#                                  || o `.)|
#                                  |`\\\\) |
#                                  |       |
#                                  |       |
#     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                       耶穌保佑                永無 BUG
