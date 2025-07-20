import streamlit as st
import subprocess
import speedtest
import matplotlib.pyplot as plt

st.title("Connection Checking App")
st.markdown("### Ping a Website or IP Address")
st.markdown("Use this tool to check the connectivity and response time of a website or IP address.")

website = st.text_input("Enter the website/IP address whose ping you want to calculate", placeholder="google.com")
if not website:
    flag = False
else:
    flag = True

if (st.button("Click to get ping") and flag):
    try:
        command = ["ping", "-n", "4", website]  
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            st.text_area(f"Ping result:\n", result.stdout, height=300)
            st.success("Command executed successfully!")
        else:
            st.error(f"Error pinging {website}:\n{result.stderr}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

st.markdown("### Get IP configuration")
if(st.button("Click for configuration (ipconfig command)")):
    try:
        command1 = ["ipconfig"] 
        result1 = subprocess.run(command1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result1.returncode == 0:
            st.text_area("IP Configuration Output", result1.stdout, height=400)
            st.success("Command executed successfully!")
        else:
            st.error(f"Error occurred")
    except Exception as e:
        st.error(f"An Error occurred: {e}")

st.markdown("### Run nslookup on any website/IP address")
website1 = st.text_input("Enter the website to Run nslookup command on", placeholder="google.com")
if not website1:
    flag1 = False
else:
    flag1 = True
if (st.button("Run nslookup command") and flag1):
    try:
        nslookup = ["nslookup", website1]
        result2 = subprocess.run(nslookup, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result2.returncode == 0:
            st.text_area(f"nslookup result:\n", result2.stdout, height=350)
            st.success("Command executed successfully!")
        else:
            st.error(f"Error running command for {website1}:\n{result2.stderr}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

st.markdown("### Get network stats")
if(st.button('Click for Netstat')):
    try:
        command3 = ["netstat", "-a", "-n"]
        result3 = subprocess.run(command3, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result3.returncode == 0:
            st.text_area("Netstat Output", result3.stdout, height=400)
            st.success("Command executed successfully!")
        else:
            st.error(f"Error occurred")
    except Exception as e:
        st.error(f"An Error occurred: {e}")
st.markdown("### Run Traceroute")
website2 = st.text_input("Enter the website/IP address to Run traceroute on", placeholder="google.com")
if not website2:
    flag2 = False
else:
    flag2 = True
if (st.button("Run Traceroute command") and flag2):
    try:
        command4 = ["tracert", website2]
        result4 = subprocess.run(command4, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result4.returncode == 0:
            st.text_area("Traceroute Output", result4.stdout, height=400)
            st.success("Command executed successfully!")
        else:
            st.error(f"Error running traceroute for {website2}:\n{result4.stderr}")
    except Exception as e:
        st.error(f"An error occurred: {e}")


def calculate_speed():
    try:
        st_instance = speedtest.Speedtest()
        st_instance.get_best_server()
        download_speed = st_instance.download() / 1_000_000  
        upload_speed = st_instance.upload() / 1_000_000  
        return round(download_speed, 2), round(upload_speed, 2)
    except Exception as e:
        st.write(e)
        return None, None

st.markdown("### Network Speed Test")

if st.button("Test Network Speed"):
    download, upload = calculate_speed()
    if download is not None and upload is not None:
        st.write(f"**Download Speed:** {download} Mbps")
        st.write(f"**Upload Speed:** {upload} Mbps")
        st.success("Command executed successfully!")
        average_speed = (download + upload) / 2
        
        
        if average_speed < 10:
            quality = "Poor"
        elif average_speed < 50:
            quality = "Average"
        else:
            quality = "Fast"
        st.write(f"**Network Quality:** {quality}")
        fig, ax = plt.subplots()
        ax.bar(["Download Speed", "Upload Speed"], [download, upload], color=['blue', 'green'])
        ax.set_title("Network Speed Analysis")
        ax.set_ylabel("Speed (Mbps)")
        ax.set_ylim(0, max(download, upload) + 10) 
        st.pyplot(fig)
    else:
        st.error("An error occurred during the speed test.")
   
