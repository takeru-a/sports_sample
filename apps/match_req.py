import datetime
import streamlit as st  
import requests
import json

endpoint = 'https://vj2jnv.deta.dev'

def app():
  st.title('試合申請')
  # ユーザー一覧を取得
  url_users = endpoint + '/users'
  res_user = requests.get(url_users)
  users = res_user.json()
  users_name = {}
  for user in users :
    users_name[user['name']] = user['key'] 
  with st.form(key='match_req'):
    date = st.date_input("日程を入力してください", min_value=datetime.date.today())
    username: str = st.selectbox('申請者', users_name.keys())

    submit_button = st.form_submit_button(label='登録')

  if submit_button:
    url = endpoint + '/match_reqs'
    user_key: str = users_name[username]
    
    data = {
      'user_key': user_key,
      'date': datetime.datetime(
        year=date.year,
        month=date.month,
        day=date.day,
      ).isoformat(),
    }
    res = requests.post(
      url,
      data = json.dumps(data)
    )

    if res.status_code == 200:
      st.success('試合申請完了')
    else:
      st.error("error")