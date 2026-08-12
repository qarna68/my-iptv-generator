import os
import requests

portal_url = os.environ.get('PORTAL_URL')
mac_address = os.environ.get('MAC_ADDRESS')

if not portal_url or not mac_address:
    print("Error: Portal URL or MAC Address is missing in secrets.")
    exit(1)

api_url = f"{portal_url}/server/api.php?action=get_all_channels&type=itv"
headers = {"Cookie": f"mac={mac_address}"}

print(f"Connecting to portal: {portal_url}")
try:
    response = requests.get(api_url, headers=headers, timeout=30)
    print(f"Response Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Response Data Sample: {str(data)[:200]}")
        channels = data.get('js', [])
        print(f"Total channels found: {len(channels)}")
        
        file_path = "channels.m3u"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            for ch in channels:
                name = ch.get('name', 'Unknown')
                cmd = ch.get('cmd', '')
                f.write(f"#EXTINF:-1,{name}\n")
                f.write(f"{portal_url}/live/{mac_address}/{mac_address}/{cmd}\n")
        print(f"Successfully generated {file_path}")
    else:
        print(f"Failed to connect, status code: {response.status_code}")
except Exception as e:
    print(f"An error occurred: {e}")
