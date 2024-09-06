import streamlit as st
import subprocess
import pandas as pd

st.set_page_config(
    page_title="WiFiPeek - Quick Access To Your Saved Network",
    page_icon="icon.png",
    menu_items={
        "About":"WiFiPeek allows you to easily retrieve and view all WiFi networks your device has connected to, along with their passwords. Secure, simple, and user-friendly access to your network credentials."
    }
)

st.write("<h2 style='color:#FF5722;font-size:31px;'>Discover All Connected Network Details</h2>",unsafe_allow_html=True)

command1=subprocess.run(["netsh","wlan","show","profiles"],capture_output=True,text=True)
output1=command1.stdout

# Fetch WiFi Name
profiles=[]
for line in output1.splitlines():
    if "All User Profile" in line:
        profiles.append(line.split(":")[1].strip())

# Fetch WiFi Password
def get_password(profile):
    password=None
    command2=subprocess.run(["netsh","wlan","show","profiles",profile,"key=clear"],capture_output=True,text=True)
    output2=command2.stdout
    for line in output2.splitlines():
            if "Key Content" in line:
                password=line.split(":")[1].strip()
                break
    return password

data_list=[]
for profile in profiles:
     password=get_password(profile)
     data_list.append({"Network Name":profile,"Password":password if password!=None else "N/A"})

data=pd.DataFrame(data_list)
st.write(data, unsafe_allow_html=True)
