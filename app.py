import streamlit as st
from multiapp import MultiApp
from apps import users, match_req, matching, result 

app = MultiApp()

app.add_app("ユーザ登録", users.app)
app.add_app("試合の申請", match_req.app)
app.add_app("マッチング", matching.app)
app.add_app("試合結果の更新", result.app)

app.run()