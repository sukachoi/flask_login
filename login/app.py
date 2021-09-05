# 20210905 깃 업로드
# app.py
from flask import Flask, render_template, request, redirect, url_for

#Flask 객체 인스턴스 생성
app = Flask(__name__)

@app.route('/') # 접속하는 url
def index():
    if request.method == "POST":
        # user=request.form['user'] # 전달받은 name이 user인 데이터
        #print(request.form.get('')) # 안전하게 가져오려면 get

        return render_template('index.html')
    elif request.method == "GET":
        input_id = request.args.get('id')
        input_pw = request.args.get('pw') 

        if input_id == None:
            return render_template('index.html')






    
def login_verify(input_id,input_pw):
    sql = "select count(*) from member where id = '" + input_id +"' and pw = '" + input_pw + "';"
    
    print("쿼리 생성....")
    print(sql)

    import pymssql

    conn = pymssql.connect(server="127.0.0.1", user="test", password="test", database="park_apt", charset='EUC-KR')#파라매트 5개
    cursor=conn.cursor()#pymssql.connect는 연결을 시도한다-->연결되면 반드시 클로즈
    cursor.execute(sql)#내 db에 있는 테이블명 사용, alt+x=execute
    row = cursor.fetchone()#알트엑스를 눌렀을 때 결과를 첫번째한줄 가져온다, fetchall은 모든 결과를 가져오면 용량문제로 거의 사용안함
    conn.close()

    print(row[0])    
    result = True
    if row[0] == 0:
        result = False

    return result          


@app.route('/login',methods=('GET','POST')) # 접속하는 url
def login():
    if request.method == "POST":
        input_id=request.form['id'] # 전달받은 name이 user인 데이터
        input_pw=request.form['pw'] # 전달받은 name이 user인 데이터
        
        if input_id == None or input_id == '':
            return render_template('index.html')

        login_ok = login_verify(input_id, input_pw)
        
        if login_ok == True:
            return render_template('apt_deposit.html')#row의 이름표가 data
        else:
            return render_template('index.html', login_fail=login_ok)#row의 이름표가 data
    elif request.method == "GET":
        input_id = request.args.get('id')
        input_pw = request.args.get('pw') 

        if input_id == None or input_id == '':
            return render_template('index.html')

        login_ok = login_verify(input_id, input_pw)
        
        if login_ok == True:
            return render_template('apt_deposit.html')#row의 이름표가 data
        else:
            return render_template('index.html', login_fail=login_ok)#row의 이름표가 data




def regular(id,pw):
    import re
    word = id
    word1 = pw
    reg = re.compile(r'[a-zA-Z0-9]')
    result = False
    result1 = False

    if reg.match(word):
        print("가능")
        result = True

    if reg.match(word1):
        print("가능")
        result1 = True
     
    if result == True and result1 == True:
        return True
    else:
        return False    


def member_insert(input_id, input_pw, dong, ho):
    sql = "insert  into member (id, pw, dong, ho) values ('" +input_id +"','" + input_pw +"', '" + dong +"', '" + ho+"')"
    import pymssql

    signup_ok = regular(input_id, input_pw)

    if signup_ok: #1==1 참
        try:
            conn = pymssql.connect(server="127.0.0.1", user="test", password="test", database="park_apt", charset='EUC-KR')#파라매트 5개
            cursor=conn.cursor()#pymssql.connect는 연결을 시도한다-->연결되면 반드시 클로즈
            print(sql)
            cursor.execute(sql)#내 db에 있는 테이블명 사용, alt+x=execute
            cursor.execute('commit;')#내 db에 있는 테이블명 사용, alt+x=execute
            conn.close()
            #가입성공
            return True
        except:
            #가입실패
            print("siginup_ok가 True였는데 except로 빠진 경우")
            return False
    else:
        print("siginup_ok가 처음부터 false")
        return False        


@app.route('/new_member') # 접속하는 url
def new_member(): #def new_member(id,pw,dong,ho):request에서 변수받아온다
    if request.method == "POST":
        # user=request.form['user'] # 전달받은 name이 user인 데이터
        #print(request.form.get('')) # 안전하게 가져오려면 get

        return render_template('new_member.html')
    elif request.method == "GET":
        input_id = request.args.get('id')
        input_pw = request.args.get('pw')
        input_dong = request.args.get('dong')
        input_ho= request.args.get('ho')

        if input_id == None:
            return render_template('new_member.html')

        
        

        member_insert_ok = member_insert(input_id,input_pw,input_dong,input_ho)

        if member_insert_ok == True:
            return render_template('apt_deposit.html')#row의 이름표가 data
        else:
            return render_template('index.html', login_fail=member_insert_ok)


def cost_insert(dong, ho, cost, pay_nm ):
    sql = "insert into aptadm_pay_lst (dong, ho, cost, pay_dt, pay_nm) values ('" +dong +"','" + ho +"', '" + cost +"', "   +"convert(varchar(10),getdate(),23)"+", '"+pay_nm +"')"
    import pymssql

    conn = pymssql.connect(server="127.0.0.1", user="test", password="test", database="park_apt",  charset='UTF8')#파라매트 5개
    cursor=conn.cursor()#pymssql.connect는 연결을 시도한다-->연결되면 반드시 클로즈
    print(sql)
    cursor.execute(sql)#내 db에 있는 테이블명 사용, alt+x=execute
    cursor.execute('commit;')#내 db에 있는 테이블명 사용, alt+x=execute
    conn.close()
    return sql

@app.route('/adm_cost') # 접속하는 url
def adm_cost(): #def new_member(id,pw,dong,ho):request에서 변수받아온다
    if request.method == "POST":
        # user=request.form['user'] # 전달받은 name이 user인 데이터
        #print(request.form.get('')) # 안전하게 가져오려면 get

        return render_template('new_member.html')
    elif request.method == "GET":
        import datetime
        
        d = str(datetime.datetime.now())[0:11]
        print(d)
        #day = datetime.datetime.strptime(d, '%Y-%m-%d')
        #day=d[0:11]
        #print(day)
        input_dong = request.args.get('dong')
        print(input_dong)
        input_ho = request.args.get('ho')
        print(input_ho)
        input_cost = request.args.get('cost')
        print(input_cost)
        input_pay_nm = request.args.get('pay_nm')
        print(input_pay_nm) 
     
    cost_insert_ok= cost_insert(input_dong, input_ho, input_cost, input_pay_nm)    
    if cost_insert_ok == True:

        return render_template('apt_deposit.html')#row의 이름표가 data
    else:
        return render_template('apt_deposit.html', insert_fail=cost_insert_ok)

def db_select(sql):
    import pymssql

    conn = pymssql.connect(server="127.0.0.1", user="test", password="test", database="park_apt", charset='EUC-KR')#파라매트 5개
    cursor=conn.cursor()#pymssql.connect는 연결을 시도한다-->연결되면 반드시 클로즈
    cursor.execute(sql)#내 db에 있는 테이블명 사용, alt+x=execute
    rows = cursor.fetchall()#알트엑스를 눌렀을 때 결과를 첫번째한줄 가져온다, fetchall은 모든 결과를 가져오면 용량문제로 거의 사용안함
    conn.close()
    return rows


@app.route('/Park_apt') # 접속하는 url
def deposit():
    if request.method == "POST":
        return render_template('apt_deposit.html')
    elif request.method == "GET":
        input_strt_dt = request.args.get('strt_dt')
        input_end_dt = request.args.get('end_dt') 

        sql="select dong, ho, cost, pay_nm, pay_dt from aptadm_pay_lst where "

        if input_strt_dt == None or input_end_dt == None or input_strt_dt == '' or input_end_dt =='':
            input_strt_dt = "convert(varchar(10),dateadd(dd,1,dateadd(dd,-datepart(dd,getdate()),getdate())),23)"
            input_end_dt= "convert(varchar(10),dateadd(d,-1,dateadd(m,1,dateadd(dd,1,dateadd(dd,-datepart(dd,getdate()),getdate())))),23)"
            sql = sql + "pay_dt>="+input_strt_dt + " and "
            sql = sql + "pay_dt<="+input_end_dt
            sql = sql + "order by dong, ho, pay_dt"
        else:
            sql=sql + "pay_dt >= '"+input_strt_dt+"' and pay_dt <= '" + input_end_dt + "' order by dong, ho, pay_dt"
        
        print(sql)
        datas = db_select(sql)
        print("가공전...............................................")
        print(datas)
        #print(len(datas))

       
        result=[]
        for i in datas:
            print(i)
            print("---------------------------")
            data = {'dong':i[0],'ho':i[1],'cost':i[2],'pay_nm':i[3],'pay_dt':i[4]}
            result.append(data)
            #db의 한 개의 row는 한개의 튜플==>그 각각의 요소를 따로 불러와 딕셔너리 만듦
            # ==>리스트(result)를 만들어 딕셔너리(data)를 요소로한다
            #[ {'dong':i[0],'ho':i[1],'cost':i[2],'pay_nm':i[3],'pay_dt':i[4]}, ...]
        print("가공후...............................................")
        print(result)
        return render_template('apt_deposit.html',datas=result)#row의 이름표가 data


        '''sql = "select cost from aptadm_pay_lst where pay_nm = '" + input_pay_nm + "';"
        print("쿼리 생성....")
        print(sql)

        import pymssql

        conn = pymssql.connect(server="127.0.0.1", user="test", password="test", database="park_apt", charset='EUC-KR')#파라매트 5개
        cursor=conn.cursor()#pymssql.connect는 연결을 시도한다-->연결되면 반드시 클로즈
        cursor.execute(sql)#내 db에 있는 테이블명 사용, alt+x=execute
        row = cursor.fetchone()#알트엑스를 눌렀을 때 결과를 첫번째한줄 가져온다, fetchall은 모든 결과를 가져오면 용량문제로 거의 사용안함
        conn.close()'''



        """data = {
        'line1':num*1,
        'line2':num*2,
        'line3':num*3,
        'line4':num*4,
        'line5':num*5,
        'line6':num*6,
        'line7':num*7,
        'line8':num*8,
        'line9':num*9

        }"""


@app.route('/id_check') # 접속하는 url
def id_check(): #def new_member(id,pw,dong,ho):request에서 변수받아온다
    if request.method == "POST":
        # user=request.form['user'] # 전달받은 name이 user인 데이터
        #print(request.form.get('')) # 안전하게 가져오려면 get

        return render_template('new_member.html')
    elif request.method == "GET":
        input_id = request.args.get('check_id')

        if input_id == None:
            return render_template('new_member.html')


        sql = "select count(*) from member where id = '"+input_id +"';"
    
        print("쿼리 생성....")
        print(sql)

        import pymssql

        conn = pymssql.connect(server="127.0.0.1", user="test", password="test", database="park_apt", charset='EUC-KR')#파라매트 5개
        cursor=conn.cursor()#pymssql.connect는 연결을 시도한다-->연결되면 반드시 클로즈
        cursor.execute(sql)#내 db에 있는 테이블명 사용, alt+x=execute
        row = cursor.fetchone()#알트엑스를 눌렀을 때 결과를 첫번째한줄 가져온다, fetchall은 모든 결과를 가져오면 용량문제로 거의 사용안함
        conn.close()

        print(row[0])
        tmp = "중복입니다."
        if row[0] == 0:
            tmp = "중복이아닙니다."
        return render_template('new_member.html',data=tmp)#row의 이름표가 data


        #sql = "insert into member(id,pw,dong,ho) values('" + input_id + "'," + "'" + input_pw + "'," + "'" + input_dong + "','" + input_ho + "');"
        
        sql = "insert into member(id,pw,dong,ho) values('" + input_id + "'," + "'" + input_pw + "', '" + input_dong + "','" + input_ho + "');"
        print("쿼리 생성....")
        print(sql)

        import pymssql

        conn = pymssql.connect(server="127.0.0.1", user="test", password="test", database="park_apt", charset='EUC-KR')#파라매트 5개
        cursor=conn.cursor()#pymssql.connect는 연결을 시도한다-->연결되면 반드시 클로즈
        cursor.execute(sql)#내 db에 있는 테이블명 사용
        cursor.execute('commit;')
        conn.close()
        result="가입 축하"
        return render_template('index.html', result=result)#row의 이름표가 data



if __name__=="__main__":
  app.run(debug=True)
  # host 등을 직접 지정하고 싶다면
  # app.run(host="127.0.0.1", port="5000", debug=True)