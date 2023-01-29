import sqlite3

def get_data(data):
    username = data['username']
    email = data['email']
    password = data['password']

    query_data = (username,email,password)
    print(query_data)
    return query_data

msg = {}

def validate_username(username):
    try:
        with sqlite3.connect("auth.db") as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE username=?", (username,))

            query_result = cur.fetchone()
            if query_result:
                is_username_available = False
                user = {'user_id':query_result[0],
                        'name':query_result[1],
                        'username':query_result[2],
                        'email':query_result[3],
                        'password':query_result[4]}
                username_msg = "This username is not available."
                msg['username_msg']=username_msg
            else:
                is_username_available = True
                username_msg = "This username is available."
                msg['username_msg']=username_msg
    except:
        error_msg = "Error in query operation."
        msg['error_msg']=error_msg
    finally:
        con.close()
        return msg, is_username_available,user

def validate_email(email):  
    try:
        with sqlite3.connect("auth.db") as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE email=?", (email,))
            query_result = cur.fetchone()
            if query_result:
                is_email_available = False
                user = {'user_id':query_result[0],
                        'name':query_result[1],
                        'username':query_result[2],
                        'email':query_result[3],
                        'password':query_result[4]}
                email_msg = "This email is not available."    
                msg['email_msg']=email_msg
            else:
                is_email_available = True
                email_msg = "This email is available."    
                msg['email_msg']=email_msg    
    except:
        error_msg = "Error in query operation."
        msg['error_msg']=error_msg
    finally:
        con.close()
        return msg, is_email_available, user

def validate_password(username,password):
    try:
        with sqlite3.connect("auth.db") as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE username=? and password=?", (username,password,))
            query_result = cur.fetchone()
            print(query_result)
            if query_result[0] == username and query_result[1] == password:
                print("Test")
                does_password_match = True
                user = {'user_id':query_result[0],
                        'name':query_result[1],
                        'username':query_result[2],
                        'email':query_result[3],
                        'password':query_result[4]}
                password_msg = "The credentials match."    
                msg['password_msg']=password_msg
            else:
                does_password_match = False
                password_msg = "This credentials do not match."    
                msg['password_msg']=password_msg    
    except:
        error_msg = "Error in query operation."
        msg['error_msg']=error_msg
    finally:
        con.close()
        print(msg)
        return msg, does_password_match, user


def register_user(data):    
    username = data['username']
    email = data['email']
    password = data['password']
    name = data['name']

    msg = []
    msg, is_username_available,user = validate_username(username)
    msg, is_email_available,user = validate_email(email)
                

    if is_username_available == True and is_email_available == True:
        try:
            with sqlite3.connect("auth.db") as con:
                cur = con.cursor()
                cur.execute("""INSERT INTO "users" ("username", "email", "password", "name") VALUES (?, ?, ?, ?)""", (username, email, password, name))
                con.commit()
                success_msg = "Table entry inserted successfully."   
                msg['success_msg']=success_msg 
        except: 
            error_msg = "Error in insert operation." 
            msg['error_msg']=error_msg 
            con.rollback()
        finally:
            con.close()    
            return msg
    else:
        msg['success_msg']=""
        error_msg = "Error in insert operation." 
        msg['error_msg']=error_msg 

        return msg

def log_in_user(data):
    username = data['username']
    password = data['password']

    msg, is_username_available, user = validate_username(username)
    msg,does_password_match,password = validate_password(username,password)
    
    if does_password_match == True:
        can_login = True
        success_msg = "User credentials match."    
        msg['success_msg']=success_msg     
    else:
        can_login = False
        error_msg = "User credentials do not match."
        msg['error_msg']=error_msg     
    
    return msg,can_login,username,password
    


def load_user_query(user_id):
    try:
        with sqlite3.connect("auth.db") as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
            query_result = cur.fetchone()
            user = {'user_id':query_result[0],
                    'name':query_result[1],
                    'username':query_result[2],
                    'email':query_result[3],
                    'password':query_result[4]}
            success_msg = "Load user success."
            msg['success_msg']=success_msg
    except:
        error_msg = "Error in query operation."
        msg['error_msg']=error_msg
    finally:
        con.close()
        return msg, user