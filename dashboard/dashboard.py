import streamlit as st
import time
import redis
import os

st.title("Dashboard de Transacciones Fraudulentas")

r = redis.Redis(host=os.getenv('REDIS_HOST', 'localhost'), port=6379, db=0, decode_responses=True)
keys = r.keys("*")

st.write("Claves en Redis:")

dict_data = {}

for key in keys:
    value = r.get(key)
    if value:
        dict_data[key] = value

if dict_data:
    st.dataframe({"card_id": list(dict_data.keys()), "tx_count": list(dict_data.values())})
else:
    st.write("No hay alertas de fraude actualmente.")

time.sleep(5)
st.rerun()