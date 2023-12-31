import streamlit as st
from google.cloud import firestore
import pandas as pd

def firestore_to_panda_old():
    # Authenticate to Firestore with the JSON account key.
    db = firestore.Client.from_service_account_json("jobsniffer-firestore-key.json")
    users_ref = db.collection("user")

    # for doc in users_ref.stream():
    #     #get fields
    #     job_position = doc.id
    #     company = doc.to_dict().get("Company", "")
    #     status = doc.to_dict().get("Status", "")

    #     # do the do with the data you gotta do
    #     st.write("Company: ", company, " / Job Position: ", job_position, " / Status: ", status)

    # column names
    columns = ['Company', 'Job Position', 'Status']

    # dataframe
    df = pd.DataFrame(columns=columns)

    # firestore into panda
    big_array=()
    for doc in users_ref.stream():
        #get fields
        job_position = doc.id
        company = doc.to_dict().get("company", "")
        status = doc.to_dict().get("status", "")
        array=(company, job_position, status)
        big_array=big_array+(array,)
    # do the do with the data you gotta do
    df = pd.DataFrame(big_array)
    return df

def firestore_to_panda():
    db = firestore.Client.from_service_account_json("jobsniffer-firestore-key.json")
    users = list(db.collection(u'user').stream())

    users_dict = list(map(lambda x: {'Company': x.get('company'), 'Job Position': x.id, 'Status': x.get('status'), "Date": "11/19/2023"}, users)) # users_dict = list(map(lambda x: x.to_dict(), users))
    df = pd.DataFrame(users_dict)
    return df

def load_view():
    test=st.button("VIEW CHART")
    if test:
        # st.write("magic time")
        # df=firestore_to_panda_old()
        df=firestore_to_panda()
        
        # table_props = [
        #     ('width','100vw')
        #     ]
        # #dict(selector='table',props=table_props),
        # styles = [
        #     dict(selector='table',props=table_props),
        # ]
        # st.markdown(df.style.set_table_styles(styles).to_html(),unsafe_allow_html=True)

        # output
        if not df.empty:
            print(df)
            st.write(df)