from flask import Flask, render_template, request, redirect, url_for, flash, session
import pymysql
import os
from datetime import datetime
from functools import wraps
import json

# 創建 Flask 應用程序
app = Flask(__name__)  # 建立物件
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
connect = pymysql.connect(host='127.0.0.1',
                          user='root',
                          password='',
                          db='pydb',
                          charset='utf8',
                          cursorclass=pymysql.cursors.DictCursor)

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
            # 方便測試方便測試方便測試方便測試方便測試方便測試方便測試方便測試方便測試方便測試方便測試方便測試方便測試方便測試方便測試方便測試
            return redirect(url_for('index'))
        else:  # 如果帳號或密碼錯誤，則顯示錯誤信息
            flash('帳密輸入錯誤', 'error')

    return render_template('login.html')  # 如果是GET請求或者登入失敗，顯示登入頁面


# index頁面路由
@login_required
@app.route('/index', methods=['GET', 'POST'])
def index():
    with connect.cursor() as cursor:
        cursor.execute("SELECT * FROM work_schedule")  # 查詢所有工作排程
        work = cursor.fetchall()  # 獲取查詢結果
        # print(work)

    with connect.cursor() as cursor:
        cursor.execute("SELECT * FROM end_work")  # 查詢結案工作
        finish_work = cursor.fetchall()  # 獲取查詢結果

    # 渲染index頁面，將工作排程傳遞給index頁面
    return render_template('index.html', work=work, finish_work=finish_work)


# "顯示"大項目路由
@login_required
@app.route('/work_option/<SID>', methods=['GET', 'POST'])
def work_option(SID):

    with connect.cursor() as cursor:
        cursor.execute(
            "SELECT project_name FROM work_schedule WHERE SID = %s ", (SID,))   # 查詢所有工作排程
        SID_name = cursor.fetchone()  # 獲取查詢結果

    print('SID_name================',SID_name)

    session['SID'] = SID
    session['SID_name'] = SID_name
    print("---------------------------------------------------------------------")
    print("SID = ", SID)
    with connect.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM project_option WHERE SID = %s ORDER BY option_id ASC", (SID,))   # 查詢所有工作排程
        project_option = cursor.fetchall()  # 獲取查詢結果

        # print("project_option獲取查詢結果 = " , project_option)
    # username = session['username']
    #
    return render_template('work_option.html', SID=SID, project_option=project_option,SID_name=SID_name)

#  大項目"刪除"路由


@app.route('/delete_option/<SID>/<option_id>', methods=['GET'])
def delete_option(SID, option_id):

    with connect.cursor() as cursor:
        sql = f"DELETE FROM project_option WHERE option_id = %s"

        try:
            cursor.execute(sql, (option_id))
            # print("成功刪除啦QQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
        except Exception as e:
            # print("刪除失敗:", e)
            ''

        connect.commit()

    return redirect(url_for('work_option', SID=SID))
    # return render_template('work_option.html', SID=SID)  #


# "建立"大項目路由
@login_required
@app.route('/add_work_option/<SID>', methods=['GET', 'POST'])
def add_work_option(SID):
    # print("---------------------------------------------------------------------")
    # print("SID = ", SID)

    with connect.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM project_option WHERE SID = %s ORDER BY option_id ASC", (SID,))   # 查詢所有工作排程
        project_option = cursor.fetchall()  # 獲取查詢結果

    project_option_json = json.dumps(project_option)  # 轉為JSON ，用於JS判斷是否已重複

    option_value = request.form.get('option')
    option_start_time = request.form.get('option_start_time')
    option_end_time = request.form.get('option_end_time')
    # print("ADDDD")
    # print(option_value,option_start_time,option_end_time)

    # option_percentage=''

    if request.method == 'POST':  # 如果是POST請求，則處理表單提交
        with connect.cursor() as cursor:

            sql = f"INSERT INTO project_option (option_id, option_value, SID, option_percentage, option_start_time, option_end_time) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, ('', option_value, SID, '',
                           option_start_time, option_end_time))
            connect.commit()
        return redirect(url_for('work_option', SID=SID))

    return render_template('add_work_option.html', project_option=project_option, SID=SID, project_option_json=project_option_json)  #


# # "點擊"大項目進入小項目路由
@login_required
@app.route('/add_option_item/<option_id>', methods=['GET', 'POST'])
def add_option_item(option_id):

    try:
        session['option_name'] = False
        session['option_id'] =False
    except:
        print("session['option_name']=空的")

    session['option_id']=option_id
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
        print('option_item==========',option_item)
        if option_item:
            SID = option_item[0]['SID']

            return render_template('add_option_item.html', option_id=option_id, option_item=option_item, SID=SID, option_name=option_name)
        else:
            SID = session.get('SID')
            return render_template('add_option_item.html', SID=SID,  option_name=option_name)


# "儲存"小項目路由
@login_required
@app.route('/item_save/', methods=['POST'])
def item_save():

    data = json.loads(request.form.get('data'))
    old_data = data.get('old', [])
    new_data = data.get('new', [])
    percentage = request.form.get('percentage')
    option_id=session.get('option_id')
    SID=session.get('SID')
    with connect.cursor() as cursor:
        print("BBB")
        for old_item in old_data:
            id = old_item['id'].replace('old', '')
            sql = "UPDATE `option_item` SET `item_value`=%s, `is_checked`=%s WHERE `id`=%s"
            cursor.execute(sql, (old_item['value'], old_item['checked'], id))

        for new_item in new_data:
            id = new_item['id'].replace('new', '')
            print("idididid=",id)
            sql = "INSERT INTO `option_item` (`item_id`, `item_value`, `is_checked`, `SID`) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (option_id, new_item['value'], new_item['checked'], SID))

        sql = "UPDATE `project_option` SET `option_percentage`=%s WHERE `option_id`=%s"
        cursor.execute(sql, (percentage, option_id))
    connect.commit()
    return redirect(url_for('work_option',SID=SID))


# # "儲存"小項目路由
# @login_required
# @app.route('/item_save/<option_id>', methods=['GET', 'POST'])
# def add_option_item(option_id):
#     item_values = request.form.getlist('item-value')
#     item_getID = request.form.getlist('option_ID')
#     percentage = int(request.form.get('percentage'))

#     cursor = connect.cursor()
#     for i in range(len(option_getID)):

#         tempVar = "option" + str(i+1)
#         tempRes = request.form.get(tempVar)
#         sql = "UPDATE " + table_check + " SET is_checked = {} WHERE option_ID = {};".format(1 if tempRes=="on" else 0, option_getID[i])
#         cursor.execute(sql)

#     connect.commit()

#     return render_template('add_option_item.html', option_id = option_id , option_item=option_item, SID=SID)
if __name__ == '__main__':
    app.run(debug=True, port=5000)  # 運行Flask應用


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
