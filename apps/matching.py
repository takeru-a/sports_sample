import streamlit as st  
import requests
import json
import pandas as pd
import datetime

endpoint = 'https://vj2jnv.deta.dev'

def app():
  st.title('マッチング')
 
  # ユーザー一覧を取得
  url_users = endpoint + '/users'
  res_user = requests.get(url_users)
  users = res_user.json()

  users_dict =[]
  for user in users:
    user_dict = {}
    user_dict['name'] = user['name']
    user_dict['type'] = user['type']
    user_dict['hometown'] = user['hometown']
    user_dict['rating'] = user['score']
    user_dict['match_size'] = user['match_size']
    user_dict['win'] = user['win']
    user_dict['lost'] = user['lost']
    users_dict.append(user_dict)

  user_list = pd.DataFrame(users_dict) 

  st.write('### ユーザー一覧')
  st.table(user_list)

  users_name = {}
  for user in users :
    users_name[user['name']] = user['key'] 

  users_key = {}
  for user in users:
    users_key[user['key']] = user['name']

  # 申請中の試合を取得
  url_match_req = endpoint + '/match_reqs'
  res_match_req = requests.get(url_match_req)
  match_reqs = res_match_req.json()

  match_reqs_key = {}
  for match_req in match_reqs:
    match_reqs_key[match_req['key']] = {
      'user_key': match_req['user_key'],
      'date': datetime.datetime.fromisoformat(match_req['date']).strftime('%Y/%m/%d'),
    }

  match_reqs_dict =[]
  for match_req in match_reqs:
    match_req_dict = {}
    match_req_dict['date'] = datetime.datetime.fromisoformat(match_req['date']).strftime('%Y/%m/%d')
    match_req_dict['username'] = users_key[match_req['user_key']]
    match_reqs_dict.append(match_req_dict)

  match_req_list = pd.DataFrame(match_reqs_dict)

  st.write('### 申請中の試合一覧')
  st.table(match_req_list)
 
  # 試合一覧を取得
  url_matchings = endpoint + '/matchings'
  res_matching = requests.get(url_matchings)
  matchings = res_matching.json()
  
  matchings_dict =[]
  for matching in matchings:
    matching_dict = {}
    matching_dict['name1'] = users_key[matching['user1_key']]
    matching_dict['name2'] = users_key[matching['user2_key']]
    matching_dict['date'] = matching['date']
    if matching['finished'] == True:
        matching_dict['winner'] = matching['winner']
        matching_dict['loser'] = matching['loser']
        matching_dict['finished'] = "終了"
    else:
        matching_dict['winner'] = ""
        matching_dict['loser'] = ""
        matching_dict['finished'] = "予定"

    matchings_dict.append(matching_dict)

  matching_list = pd.DataFrame(matchings_dict)   
  
  st.write('### 試合一覧')
  st.table(matching_list)
  if any(match_reqs_key) is True:
      match_req_key = st.selectbox('試合番号を選択して下さい', match_reqs_key.keys())
  with st.form(key='matching'):
    data = {
          'date': None,
          'user1_key': None,
          'user2_key': None,
          'match_id': None,
          'finished': None,
          'winner' : None,
          'loser' : None,
        }
    if any(match_reqs_key) is True:
      # match_req_key = st.selectbox('試合番号を選択して下さい', match_reqs_key.keys())
      match_info = match_reqs_key[match_req_key]
      user1_key = match_info["user_key"]
      match_date = match_info["date"]
      st.write("日程: "+match_date)
      username1: str = users_key[user1_key]
      st.write("対戦相手: "+username1)
      member_list =  list(users_name.keys())
      member_list.remove(username1)
      username2: str = st.selectbox('申請者名', member_list)
      submit_button = st.form_submit_button(label='予約')

      if submit_button:
        user1_key: str = users_name[username1]
        user2_key: str = users_name[username2]
        match_id: str = match_req_key
        data = {
          'date': match_date,
          'user1_key': user1_key,
          'user2_key': user2_key,
          'match_id': match_id,
          'finished': False,
          'winner' : "",
          'loser' : "",
        }
    else:
        st.write('# 現在申請中の試合はありません')
        submit_button = st.form_submit_button(label='❌')
        
 
    url = endpoint + '/matchings'
    res = requests.post(
        url,
        data = json.dumps(data)
      )
    if res.status_code == 200:
        st.success('登録完了しました。')
        delete_url = endpoint + '/match_reqs' + '/' + match_id
        requests.delete(delete_url)
      # st.write(res.status_code)
    elif res.status_code == 404 and res.json()['detail'] == 'Already booked':
        st.error('失敗しました')