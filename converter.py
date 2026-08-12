import os
import requests

portal_url = os.environ.get('PORTAL_URL')
mac_address = os.environ.get('MAC_ADDRESS')

if not portal_url or not mac_address:
    print("Error: Portal URL or MAC Address is missing in secrets.")
    exit(1)

print(f"Current working directory: {os.getcwd()}")

api_url = f"{portal_url}/server/api.php?action=get_all_channels&type=itv"
headers = {"Cookie": f"mac={mac_address}"}

print(f"Connecting to portal...")
try:
    response = requests.get(api_url, headers=headers, timeout=30)
    if response.status_code == 200:
        data = response.json()
        channels = data.get('js', [])
        
        file_path = "channels.m3u"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            for ch in channels:
                name = ch.get('name', 'Unknown')
                cmd = ch.get('cmd', '')
                f.write(f"#EXTINF:-1,{name}\n")
                f.write(f"{portal_url}/live/{mac_address}/{mac_address}/{cmd}\n")
                
        abs_path = os.path.abspath(file_path)
        print(f"Successfully generated channels.m3u at: {abs_path}")
    else:
        print(f"Failed, status code: {response.status_code}")
except Exception as e:
    print(f"Error: {e}")
