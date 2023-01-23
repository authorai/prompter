import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account

import json
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds)

# Streamlit widgets to let a user create a new post
prompt = st.text_input("Prompt")
temperature = st.slider("Temperature", 0.0, 1.0, 0.5)
submit = st.button("Create new prompt")

# Once the user has submitted, upload it to the database
if prompt and temperature and submit:
	doc_ref = db.collection("prompts").document(prompt)
	doc_ref.set({
		"prompt": prompt,
		"temperature": temperature
	})

# And then render each post, using some light Markdown
posts_ref = db.collection("prompts")
for doc in posts_ref.stream():
	post = doc.to_dict()
	title = post["prompt"]
	url = post["temperature"]

	st.subheader(f"Prompt: {prompt}")
	st.write(f"Temperature: {temperature}")