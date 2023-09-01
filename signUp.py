import streamlit as st
import streamlit_authenticator as auth
import datetime
from deta import  Deta


DETA_KEY = 'd0csrk7wfgm_jjHnWgdFsJeYZGqUQ1eKyonaNYkZoyo6'

deta = Deta(DETA_KEY)

db = deta.Base('StreamlitAuth')


def insert_user(email,username,password):
    date_joined = str(datetime.datetime.now())
    return db.put({'key':email,'username':username,'password':password,'date_joined':date_joined})

# insert_user('test@gm.com','test','12345')

def fetch_users():
    users = db.fetch()
    return users.items

def fetch_users_emails():
    users = db.fetch()
    emails = []
    for user in users.items:
        emails.append(user['key'])
    return emails



def fetch_users_username():
    users = db.fetch()
    emails = []
    for user in users.items:
        emails.append(user['username'])
    return emails

print(fetch_users_username())

def sign_uo():
    with st.form(key='signup',clear_on_submit=True):
        st.subheader(':green[Sign Up]')
        email = st.text_input(':violet[Email]',placeholder='Enter your Email')
        username = st.text_input(':violet[Username]',placeholder='Enter your Username')
        password1 = st.text_input(':violet[Password]',placeholder='Enter your Password',type='password')
        password2 = st.text_input(':violet[Confirm Password]',placeholder='Enter your Confirm password',type='password')

        if email:
            if email not in fetch_users_emails():
                if username not in fetch_users_username():
                    if len(username) >= 3:
                        if len(password1)>=6:

                            if password1 == password2:
                                hashedpassword = auth.Hasher([password2]).generate()

                                insert_user(email,username,hashedpassword[0])
                                st.success('Account Registered')
                                st.balloons()
                            else:
                                st.warning('Password do not match')

                        else:
                            st.warning('Password is to sort')

                    else:
                        st.warning('user should be at least 4 character')
                else:
                    st.warning('Invalid Username/Already exist')
            else:
                st.warning('Email already Exists')
        else:
            st.warning('Invalid Email')

        btn1,btn2,btn3,btn4,btn5 = st.columns(5)
        with btn3:
            st.form_submit_button('SignUp')


sign_uo()