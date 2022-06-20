import datetime
import streamlit as st  
import requests
import json
import pandas as pd

endpoint = 'https://vj2jnv.deta.dev'

def app():
  st.title('試合結果の更新')
  # ユーザー一覧を取得
  url_users = endpoint + '/users'
  res_user = requests.get(url_users)
  users = res_user.json()

  users_name = {}
  for user in users :
    users_name[user['name']] = user['key'] 
  users_key = {}
  for user in users:
    users_key[user['key']] = {
        'name':user['name'],
        'hometown': user['hometown'],
        'type': user['type'],
        'score': user['score'] ,
        'match_size': user['match_size'] ,
        'win': user['win'] ,
        'lost': user['lost'],  
    }
  # 試合一覧を取得
  url_matchings = endpoint + '/matchings'
  res_matching = requests.get(url_matchings)
  matchings = res_matching.json()

  matchings_key = {}
  for matching in matchings:
    matchings_key[matching['key']] = {
      'date': matching['date'],  
      'user1_key': matching['user1_key'],
      'user2_key': matching['user2_key'],
      'match_id': matching['match_id'],
      'finished': matching['finished'],
      'winner': matching['winner'],
      'loser': matching['loser']
    }

  if any(matchings_key) is True:
      match_key = st.selectbox('試合番号を選択して下さい', matchings_key.keys())
      selected_data = matchings_key[match_key]
      member_list = [users_key[selected_data['user1_key']]['name'],users_key[selected_data['user2_key']]['name']]
      st.write("0: "+member_list[0])
      st.write("1: "+member_list[1])
      winner_num :int = st.radio('勝者を選択してください', [0,1])
      winner = member_list[winner_num]

      with st.form(key='result'):
        st.write('### 選択中の試合情報')
        if selected_data['finished']==True:
            st.write("＊この試合は終了しています")
        st.write('日程： '+selected_data['date'])
        st.write('対戦： '+member_list[0]+' vs '+member_list[1]) 
        member_list.remove(winner)
        loser: str = member_list[0]
        st.write("更新後の勝者: "+winner )
        st.write("更新後の敗者: "+loser )
        # submit_button = st.form_submit_button(label='登録') 
        match_data = {
            'date': selected_data['date'],
            'user1_key': selected_data['user1_key'],
            'user2_key': selected_data['user2_key'],
            'match_id': selected_data['match_id'],
            'finished': True,
            'winner' : winner,
            'loser' : loser,
        }
        winner_key = users_name[winner]
        loser_key = users_name[loser]
        winner_info = users_key[winner_key]
        loser_info = users_key[loser_key] 
        winner_data = {
        'name': winner,
        'hometown': winner_info['hometown'],
        'type': winner_info['type'],
        'score': winner_info['score'] + 3,
        'match_size': winner_info['match_size'] + 1,
        'win': winner_info['win'] + 1,
        'lost': winner_info['lost'],
        }
        loser_data = {
        'name': loser,
        'hometown': loser_info['hometown'],
        'type': loser_info['type'],
        'score': loser_info['score'],
        'match_size': loser_info['match_size']+1,
        'win': loser_info['win'],
        'lost': loser_info['lost']+1,
        }
        submit_button = st.form_submit_button(label='登録')
  else:
       st.write('# 現在更新する試合はありません')

  if submit_button and selected_data['finished']==False:
    url1 = endpoint + '/users/' + winner_key
    res1 = requests.put(
      url1,
      data = json.dumps(winner_data)
    )
    url2 = endpoint + '/users/' + loser_key
    res2 = requests.put(
      url2,
      data = json.dumps(loser_data)
    )
    url3 = endpoint + '/matchings/' + match_key
    res3 = requests.put(
      url3,
      data = json.dumps(match_data)
    )
    if res1.status_code == 200 and res2.status_code == 200 and res3.status_code == 200:
      st.success('試合結果の更新完了')
    else:
      st.error("error")