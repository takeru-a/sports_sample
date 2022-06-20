import streamlit as st  
import requests
import json

endpoint = 'https://vj2jnv.deta.dev'

def app():
  st.title('ユーザー登録')

  with st.form(key='user'):
    name: str = st.text_input('学校名', max_chars=30)
    type: str = st.text_input('スポーツ名', max_chars=30)
    hometown: str = st.selectbox(
     '都道府県を選択して下さい',
     ('北海道',
    '青森県','岩手県','宮城県','秋田県','山形県','福島県',
    '茨城県','栃木県','群馬県','埼玉県','千葉県','東京都','神奈川県',
    '新潟県','富山県','石川県','福井県','山梨県','長野県','岐阜県','静岡県','愛知県',
    '三重県','滋賀県','京都府','大阪府','兵庫県','奈良県','和歌山県',
    '鳥取県','島根県','岡山県','広島県','山口県',
    '徳島県','香川県','愛媛県','高知県',
    '福岡県','佐賀県','長崎県','熊本県','大分県','宮崎県','鹿児島県','沖縄県'))
    match_size: int = 0
    win: int = 0
    lost: int = 0
    score: int = 0
    data = {
      'name': name,
      'hometown': hometown,
      'type': type,
      'score': score,
      'match_size': match_size,
      'win': win,
      'lost': lost,
    }
    submit_button = st.form_submit_button(label='登録')

  if submit_button:
    url = endpoint + '/users'
    res = requests.post(
      url,
      data = json.dumps(data)
    )

    if res.status_code == 200:
      st.success('ユーザー登録完了')
    else:
      st.error("error")