
import os
import sys
import time
import json
import random
import ssl
import gzip
import http.client
from io import BytesIO
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from google.protobuf.json_format import MessageToDict
import requests
import follow_pb2
import MajoRLoGinrEq_pb2
import MajoRLoGinrEs_pb2
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed


GOLD     = '\033[38;5;220m'
RED      = '\033[38;5;196m'
GREEN    = '\033[38;5;46m'
BLUE     = '\033[38;5;51m'
PURPLE   = '\033[38;5;141m'
ORANGE   = '\033[38;5;208m'
CYAN     = '\033[38;5;87m'
WHITE    = '\033[38;5;255m'
YELLOW   = '\033[38;5;226m'
TEAL     = '\033[38;5;44m'
PINK     = '\033[38;5;205m'
LIME     = '\033[38;5;118m'
MAGENTA  = '\033[38;5;201m'
CORAL    = '\033[38;5;210m'
SKY      = '\033[38;5;117m'
LAVENDER = '\033[38;5;183m'
ROSE     = '\033[38;5;175m'
MINT     = '\033[38;5;157m'
PEACH    = '\033[38;5;216m'
VIOLET   = '\033[38;5;135m'
NEON     = '\033[38;5;154m'
HOT_PINK = '\033[38;5;199m'
ICE      = '\033[38;5;159m'
BOLD     = '\033[1m'
RESET    = '\033[0m'
DIM      = '\033[2m'


REGIONS = {
    '1': {'name': 'BD',  'url': 'https://clientbp.ggpolarbear.com/Follow'},
    '2': {'name': 'IND', 'url': 'https://client.ind.freefiremobile.com/Follow'},
    '3': {'name': 'PK',  'url': 'https://clientbp.ggpolarbear.com/Follow'},
    '4': {'name': 'SG',  'url': 'https://clientbp.ggpolarbear.com/Follow'},
    '5': {'name': 'Taiwan', 'url': 'https://clientbp.ggpolarbear.com/Follow'},
    '6': {'name': 'TH',  'url': 'https://clientbp.ggpolarbear.com/Follow'},
    '7': {'name': 'RU',  'url': 'https://clientbp.ggpolarbear.com/Follow'},
    '8': {'name': 'ID',  'url': 'https://clientbp.ggpolarbear.com/Follow'},
    '9': {'name': 'NA',  'url': 'https://client.us.freefiremobile.com/Follow'},
    '10': {'name': 'BR', 'url': 'https://client.us.freefiremobile.com/Follow'},
    '11': {'name': 'ME',  'url': 'https://clientbp.ggblueshark.com/Follow'},
    '12': {'name': 'VN',  'url': 'https://clientbp.ggpolarbear.com/Follow'},
}

KEY           = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
IV            = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
AES_KEY       = b'Yg&tc%DEuh6%Zc^8'
AES_IV        = b'6oyZDr22E3ychjM%'
ACCOUNTS_FILE = "access.txt"
TOKENS_FILE   = "tokens.json"
PORT          = 8080


COLOR_POOL = [
    PURPLE, CYAN, PINK, GOLD, LIME, ORANGE,
    TEAL, MAGENTA, ROSE, SKY, CORAL, MINT,
    VIOLET, NEON, HOT_PINK, ICE, LAVENDER, PEACH
]


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_rainbow_colors(n):
    pool = COLOR_POOL[:]
    random.shuffle(pool)
    colors = []
    for i in range(n):
        colors.append(pool[i % len(pool)])
    return colors

def print_banner():
    clear_screen()
    c = get_rainbow_colors(20)
    border = random.choice([GOLD, CYAN, VIOLET, HOT_PINK, LIME, MAGENTA])

    banner = f"""
{border}╔══════════════════════════════════════════════════════════════════════════════════╗
║                                                                                  ║
║  {c[0]}███████╗██╗  ██╗██╗██╗  ██╗ █████╗ ██████╗                               {border}║
║  {c[1]}██╔════╝██║  ██║██║██║  ██║██╔══██╗██╔══██╗                              {border}║
║  {c[2]}███████╗███████║██║███████║███████║██████╔╝                              {border}║
║  {c[3]}╚════██║██╔══██║██║██╔══██║██╔══██║██╔══██╗                              {border}║
║  {c[4]}███████║██║  ██║██║██║  ██║██║  ██║██████╔╝                              {border}║
║  {c[5]}╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝                              {border}║
║                                                                                  ║
║  {border}══════════════════════════════════════════════════════════════════════════════  ║
║                                                                                  ║
║         {c[12]}✦  {c[13]}S{c[14]}H{c[15]}I{c[16]}H{c[17]}A{c[12]}B  {c[15]}✦{border}          ║
║                                                                                  ║
║  {border}══════════════════════════════════════════════════════════════════════════════  ║
║                                                                                  ║
║    {c[0]}★{RESET}  {c[1]}PREMIUM EDITION{RESET}   {c[3]}|{RESET}   {c[4]}ELITE POWER{RESET}   {c[6]}|{RESET}   {c[7]}MADE BY XANAF{RESET}  {c[8]}★{RESET}          ║
║                                                                                  ║
{border}╚══════════════════════════════════════════════════════════════════════════════════╝{RESET}
"""
    print(banner)
    time.sleep(0.3)

def print_status(message, status_type="info"):
    icons = {
        "success": f"{GREEN}[+]{RESET}",
        "error":   f"{RED}[X]{RESET}",
        "warning": f"{YELLOW}[!]{RESET}",
        "info":    f"{SKY}[i]{RESET}",
        "loading": f"{CYAN}[~]{RESET}",
        "gold":    f"{GOLD}[*]{RESET}",
    }
    print(f"  {icons.get(status_type, '[i]')} {message}")

def encrypt_proto(data: bytes) -> bytes:
    cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
    padded = pad(data, AES.block_size)
    return cipher.encrypt(padded)

def get_access_token(uid, password):
    url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    headers = {
        "Host": "100067.connect.garena.com",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; ASUS_Z01QD Build/QKQ1.190825.002)",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "close",
    }
    data = {
        "uid": str(uid),
        "password": str(password),
        "response_type": "token",
        "client_type": "2",
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067",
    }
    try:
        r = requests.post(url, headers=headers, data=data, timeout=15)
        if r.status_code == 200:
            j = r.json()
            return j.get('access_token'), j.get('open_id')
        return None, None
    except:
        return None, None

def major_login_protobuf(access_token, open_id):
    try:
        major_login = MajoRLoGinrEq_pb2.MajorLogin()
        major_login.event_time = str(datetime.now())[:-7]
        major_login.game_name = "free fire"
        major_login.platform_id = 2
        major_login.client_version = "1.126.2"
        major_login.client_version_code = "2024010012"
        major_login.system_software = "Android OS 11 / API-30 (RQ3A.210805.001)"
        major_login.system_hardware = "Handheld"
        major_login.device_type = "Handheld"
        major_login.telecom_operator = "Verizon"
        major_login.network_operator_a = "Verizon"
        major_login.network_type = "WIFI"
        major_login.network_type_a = "WIFI"
        major_login.screen_width = 1080
        major_login.screen_height = 2400
        major_login.screen_dpi = "440"
        major_login.processor_details = "ARMv8"
        major_login.cpu_type = 2
        major_login.cpu_architecture = "64"
        major_login.memory = 6144
        major_login.gpu_renderer = "Adreno (TM) 650"
        major_login.gpu_version = "OpenGL ES 3.2 V@1.50"
        major_login.graphics_api = "OpenGLES3"
        major_login.unique_device_id = f"Google|34a7dcdf-a7d5-4cb6-8d7e-3b0e448a0c{random.randint(10,99)}"
        major_login.client_ip = ""
        major_login.language = "en"
        major_login.open_id = open_id
        major_login.open_id_type = "4"
        major_login.login_open_id_type = 4
        major_login.access_token = access_token
        major_login.login_by = 3
        major_login.platform_sdk_id = 2
        major_login.origin_platform_type = "4"
        major_login.primary_platform_type = "4"
        
        memory_available = major_login.memory_available
        memory_available.version = 55
        memory_available.hidden_value = 81
        
        major_login.external_storage_total = 128512
        major_login.external_storage_available = random.randint(38000, 52000)
        major_login.internal_storage_total = 110731
        major_login.internal_storage_available = random.randint(18000, 32000)
        major_login.game_disk_storage_total = 26628
        major_login.game_disk_storage_available = random.randint(18000, 25000)
        major_login.external_sdcard_total_storage = 119234
        major_login.external_sdcard_avail_storage = random.randint(25000, 60000)
        major_login.library_path = f"/data/app/~~{random.randint(100,999)}/base.apk"
        major_login.library_token = "hash|base.apk"
        major_login.client_using_version = "7428b253defc164018c604a1ebbfebdf"
        major_login.supported_astc_bitset = 16383
        major_login.analytics_detail = b"FwQVTgUPX1UaUllDDwcWCRBpWAUOUgsvA1snWlBaO1kFYg=="
        major_login.loading_time = random.randint(9000, 18000)
        major_login.release_channel = "android"
        major_login.channel_type = 3
        major_login.reg_avatar = 1
        major_login.if_push = 1
        major_login.is_vpn = 0
        major_login.android_engine_init_flag = 110009
        
        serialized = major_login.SerializeToString()
        encrypted = encrypt_proto(serialized)
        
        context = ssl._create_unverified_context()
        conn = http.client.HTTPSConnection("loginbp.ggpolarbear.com", context=context, timeout=20)
        headers = {
            'X-Unity-Version': '2018.4.11f1',
            'ReleaseVersion': 'OB54',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-GA': 'v1 1',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.1.2; ASUS_Z01QD Build/QKQ1.190825.002)',
            'Host': 'loginbp.ggpolarbear.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip'
        }
        conn.request("POST", "/MajorLogin", body=encrypted, headers=headers)
        response = conn.getresponse()
        raw_data = response.read()
        
        if response.getheader('Content-Encoding') == 'gzip':
            with gzip.GzipFile(fileobj=BytesIO(raw_data)) as f:
                raw_data = f.read()
        conn.close()
        
        if response.status in [200, 201]:
            return raw_data.hex()
        return None
    except Exception as e:
        return None

def decrypt_major_response(hex_data):
    try:
        proto = MajoRLoGinrEs_pb2.MajorLoginRes()
        proto.ParseFromString(bytes.fromhex(hex_data))
        return proto
    except:
        return None

def generate_jwt(uid, password):
    result = {
        "success": False,
        "uid": uid,
        "jwt_token": None,
        "account_uid": None,
        "region": None,
        "message": "",
        "timestamp": datetime.now().isoformat()
    }
    
    if not uid or not password:
        result["message"] = "UID and Password are required."
        return result
    
    if not uid.isdigit() or len(uid) < 8:
        result["message"] = "Invalid UID format."
        return result
    
    access_token, open_id = get_access_token(uid, password)
    if not access_token or not open_id:
        result["message"] = "Invalid UID or Password."
        return result
    
    response_hex = major_login_protobuf(access_token, open_id)
    if not response_hex:
        result["message"] = "Account may be banned or invalid."
        return result
    
    login_data = decrypt_major_response(response_hex)
    if not login_data:
        result["message"] = "Failed to decrypt response."
        return result
    
    jwt_token = login_data.token
    if not jwt_token:
        result["message"] = "No JWT token received."
        return result
    
    result["success"] = True
    result["jwt_token"] = jwt_token
    result["account_uid"] = str(login_data.account_uid)
    result["region"] = getattr(login_data, 'region', 'IND')
    result["message"] = "JWT generated successfully!"
    
    return result

def encrypt_payload(data):
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    return cipher.encrypt(pad(data, AES.block_size))

def send_follow(target_id, jwt, region_url):
    req = follow_pb2.CSFollowReq()
    req.target_id = target_id
    encrypted_data = encrypt_payload(req.SerializeToString())

    headers = {
        "User-Agent":     "UnityPlayer/2022.3.47f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)",
        "Accept":         "*/*",
        "Accept-Encoding":"deflate, gzip",
        "Authorization":  f"Bearer {jwt}",
        "X-Ga":           "v1 1",
        "Releaseversion": "OB54",
        "Content-Type":   "application/x-www-form-urlencoded",
        "X-Unity-Version":"2022.3.47f1",
    }

    try:
        response = requests.post(region_url, headers=headers, data=encrypted_data, timeout=20)

        if response.status_code == 200:
            try:
                res = follow_pb2.CSFollowRes()
                res.ParseFromString(response.content)
                res_dict = MessageToDict(res, preserving_proto_field_name=True)
                if 'msg' in res_dict:
                    return True, res_dict['msg']
                elif 'code' in res_dict and res_dict['code'] == 0:
                    return True, "Follow successful"
                else:
                    return True, "Follow sent"
            except:
                return True, "Success"
        elif response.status_code == 401:
            return False, "Token expired"
        elif response.status_code == 403:
            return False, "Need 3 Craftland matches"
        else:
            return False, f"HTTP {response.status_code}"

    except requests.exceptions.RequestException:
        return False, "Request failed"

def load_accounts_from_file():
    try:
        if not os.path.exists(ACCOUNTS_FILE):
            print_status(f"{ACCOUNTS_FILE} not found. Creating sample...", "warning")
            with open(ACCOUNTS_FILE, 'w') as f:
                f.write("# Format: uid:password\n")
                f.write("123456789:yourpassword\n")
            print_status(f"Add accounts to {BOLD}{ACCOUNTS_FILE}{RESET} and run again", "info")
            return None

        accounts = []
        with open(ACCOUNTS_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if line and ':' in line and not line.startswith('#'):
                    parts = line.split(':', 1)
                    if len(parts) == 2:
                        uid, password = parts
                        if uid.strip() and password.strip():
                            accounts.append({
                                'uid': uid.strip(),
                                'password': password.strip(),
                                'jwt': None,
                                'account_uid': None,
                                'region': None
                            })

        if not accounts:
            print_status("No valid accounts found in access.txt", "error")
            return None

        return accounts

    except Exception as e:
        print_status(f"Error loading accounts: {e}", "error")
        return None

def generate_all_jwts_fast(accounts):
    total = len(accounts)
    valid_accounts = []
    c = get_rainbow_colors(4)
    
    print(f"\n{PURPLE}{BOLD}╔══════════════════════════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{PURPLE}{BOLD}║{RESET}                     {CYAN}GENERATING JWT TOKENS{RESET}                           {PURPLE}{BOLD}║{RESET}")
    print(f"{PURPLE}{BOLD}╚══════════════════════════════════════════════════════════════════════════════════╝{RESET}\n")
    
    def process_account(account):
        uid = account['uid']
        password = account['password']
        result = generate_jwt(uid, password)
        return uid, result
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_account = {}
        for account in accounts:
            future = executor.submit(process_account, account)
            future_to_account[future] = account
        
        completed = 0
        for future in as_completed(future_to_account):
            account = future_to_account[future]
            uid, result = future.result()
            completed += 1
            prefix = f"  {c[completed % len(c)]}[{completed}/{total}]{RESET}"
            
            if result["success"]:
                account['jwt'] = result['jwt_token']
                account['account_uid'] = result['account_uid']
                account['region'] = result['region']
                valid_accounts.append(account)
                print(f"\r{prefix} {GREEN}[+]{RESET} {GOLD}{uid}{RESET}  ->  {MINT}JWT generated{RESET}           ")
            else:
                account['jwt'] = None
                print(f"\r{prefix} {RED}[X]{RESET} {DIM}{uid}{RESET}  ->  {CORAL}{result['message']}{RESET}           ")
    
    print()
    print_status(f"{GREEN}{len(valid_accounts)}{RESET} JWT(s) generated successfully", "success")
    print_status(f"{RED}{total - len(valid_accounts)}{RESET} JWT(s) failed", "error")
    return valid_accounts

def save_tokens_to_file(accounts, region_name):
    data = {
        'generated_at': datetime.now().isoformat(),
        'region': region_name,
        'total_accounts': len(accounts),
        'accounts': []
    }
    
    for acc in accounts:
        if acc.get('jwt'):
            data['accounts'].append({
                'uid': acc['uid'],
                'jwt': acc['jwt'],
                'account_uid': acc.get('account_uid', ''),
                'region': acc.get('region', ''),
                'status': 'valid'
            })
    
    with open(TOKENS_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    
    print_status(f"Tokens saved to {BOLD}{TOKENS_FILE}{RESET}", "success")

def print_region_menu():
    c = get_rainbow_colors(14)
    print(f"\n{c[0]}╔═══════════════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{c[0]}║{RESET}                  {GOLD}{BOLD}  SELECT  REGION{RESET}                         {c[0]}║{RESET}")
    print(f"{c[0]}╠═══════════════════════════════════════════════════════════════════════╣{RESET}")
    print(f"{c[0]}║{RESET}                                                               {c[0]}║{RESET}")
    print(f"{c[0]}║{RESET}     {c[2]}[{BOLD}1{RESET}{c[2]}]{RESET}  {CYAN}BD Server{RESET}         {c[3]}[{BOLD}7{RESET}{c[3]}]{RESET}  {CYAN}RU Server{RESET}          {c[0]}║{RESET}")
    print(f"{c[0]}║{RESET}     {c[4]}[{BOLD}2{RESET}{c[4]}]{RESET}  {CYAN}IND Server{RESET}        {c[5]}[{BOLD}8{RESET}{c[5]}]{RESET}  {CYAN}ID Server{RESET}          {c[0]}║{RESET}")
    print(f"{c[0]}║{RESET}     {c[6]}[{BOLD}3{RESET}{c[6]}]{RESET}  {CYAN}PK Server{RESET}         {c[7]}[{BOLD}9{RESET}{c[7]}]{RESET}  {CYAN}NA Server{RESET}          {c[0]}║{RESET}")
    print(f"{c[0]}║{RESET}     {c[8]}[{BOLD}4{RESET}{c[8]}]{RESET}  {CYAN}SG Server{RESET}         {c[9]}[{BOLD}10{RESET}{c[9]}]{RESET} {CYAN}BR Server{RESET}          {c[0]}║{RESET}")
    print(f"{c[0]}║{RESET}     {c[10]}[{BOLD}5{RESET}{c[10]}]{RESET} {CYAN}Taiwan Server{RESET}     {c[11]}[{BOLD}11{RESET}{c[11]}]{RESET} {CYAN}ME Server{RESET}          {c[0]}║{RESET}")
    print(f"{c[0]}║{RESET}     {c[12]}[{BOLD}6{RESET}{c[12]}]{RESET} {CYAN}TH Server{RESET}         {c[13]}[{BOLD}12{RESET}{c[13]}]{RESET} {CYAN}VN Server{RESET}          {c[0]}║{RESET}")
    print(f"{c[0]}║{RESET}                                                               {c[0]}║{RESET}")
    print(f"{c[0]}╚═══════════════════════════════════════════════════════════════════════╝{RESET}")

def select_region():
    print_region_menu()
    while True:
        choice = input(f"\n  {ORANGE}-> Select region {GOLD}(1-12){RESET}: ").strip()
        if choice in REGIONS:
            return REGIONS[choice]
        print_status("Invalid. Enter 1-12", "error")


HTML_PAGE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>XANAF FOLLOW - Premium Follow Bot</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: #0a0a0f;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'Rajdhani', sans-serif;
            padding: 20px;
            position: relative;
            overflow-x: hidden;
        }
        body::before {
            content: '';
            position: fixed;
            top: -50%;
            left: -50%;
            right: -50%;
            bottom: -50%;
            background: 
                radial-gradient(ellipse at 20% 50%, rgba(255,0,100,0.08), transparent 50%),
                radial-gradient(ellipse at 80% 50%, rgba(100,0,255,0.08), transparent 50%),
                radial-gradient(ellipse at 50% 100%, rgba(0,200,255,0.05), transparent 50%);
            animation: bgFloat 20s ease-in-out infinite alternate;
            z-index: 0;
            pointer-events: none;
        }
        @keyframes bgFloat {
            0% { transform: translate(0, 0) rotate(0deg); }
            100% { transform: translate(2%, -2%) rotate(3deg); }
        }
        .container {
            background: rgba(10, 10, 20, 0.92);
            border-radius: 28px;
            padding: 45px 40px;
            max-width: 750px;
            width: 100%;
            border: 1px solid rgba(255,255,255,0.06);
            box-shadow: 0 40px 100px rgba(0,0,0,0.8), 0 0 80px rgba(255,0,100,0.03);
            position: relative;
            z-index: 1;
            backdrop-filter: blur(30px);
        }
        .container::before {
            content: '';
            position: absolute;
            top: -1px;
            left: -1px;
            right: -1px;
            bottom: -1px;
            border-radius: 29px;
            background: linear-gradient(135deg, rgba(255,0,100,0.15), rgba(100,0,255,0.15), rgba(0,200,255,0.1));
            z-index: -1;
            opacity: 0.5;
        }
        .header {
            text-align: center;
            margin-bottom: 25px;
        }
        .header .logo {
            display: inline-block;
            margin-bottom: 6px;
        }
        .header .logo .icon {
            font-size: 32px;
            color: #ff0066;
            margin-right: 8px;
        }
        .header h1 {
            font-family: 'Orbitron', sans-serif;
            font-size: 28px;
            font-weight: 900;
            background: linear-gradient(135deg, #ff0066, #cc00ff, #6600ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: 3px;
            display: inline-block;
        }
        .header .subtitle {
            color: rgba(255,255,255,0.3);
            font-size: 13px;
            letter-spacing: 5px;
            margin-top: 4px;
            font-weight: 300;
        }
        .stats-bar {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
            margin-bottom: 22px;
            padding: 15px;
            background: rgba(255,255,255,0.02);
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.04);
        }
        .stats-bar .stat-item {
            text-align: center;
        }
        .stats-bar .stat-item .stat-number {
            font-size: 22px;
            font-weight: 700;
            font-family: 'Orbitron', sans-serif;
            color: #fff;
        }
        .stats-bar .stat-item .stat-label {
            font-size: 10px;
            color: rgba(255,255,255,0.25);
            letter-spacing: 1px;
            margin-top: 2px;
            text-transform: uppercase;
        }
        .stats-bar .stat-item .stat-number.green { color: #00e676; }
        .stats-bar .stat-item .stat-number.red { color: #ff1744; }
        .stats-bar .stat-item .stat-number.gold { color: #ffd700; }
        .stats-bar .stat-item .stat-number.blue { color: #448aff; }
        .form-group {
            margin-bottom: 14px;
        }
        .form-group label {
            display: block;
            color: rgba(255,255,255,0.5);
            font-size: 12px;
            font-weight: 600;
            letter-spacing: 2px;
            margin-bottom: 6px;
            text-transform: uppercase;
        }
        .form-group .input-wrap {
            position: relative;
            background: rgba(255,255,255,0.03);
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.06);
            transition: all 0.3s ease;
            overflow: hidden;
        }
        .form-group .input-wrap:focus-within {
            border-color: rgba(255,0,100,0.3);
            box-shadow: 0 0 30px rgba(255,0,100,0.04);
            background: rgba(255,255,255,0.05);
        }
        .form-group .input-wrap .icon-left {
            position: absolute;
            left: 14px;
            top: 50%;
            transform: translateY(-50%);
            color: rgba(255,255,255,0.15);
            font-size: 14px;
            pointer-events: none;
        }
        .form-group input, .form-group select {
            width: 100%;
            padding: 15px 16px 15px 44px;
            background: transparent;
            border: none;
            color: #e0e0e0;
            font-size: 15px;
            font-family: 'Rajdhani', sans-serif;
            font-weight: 500;
            letter-spacing: 0.5px;
            outline: none;
        }
        .form-group select option {
            background: #1a1a2e;
            color: #e0e0e0;
        }
        .form-group input::placeholder {
            color: rgba(255,255,255,0.15);
            font-weight: 300;
        }
        .form-row {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 12px;
        }
        .btn {
            width: 100%;
            padding: 16px;
            border: none;
            border-radius: 12px;
            font-family: 'Orbitron', sans-serif;
            font-size: 14px;
            font-weight: 700;
            letter-spacing: 3px;
            background: linear-gradient(135deg, #ff0066, #cc00ff);
            color: #fff;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            position: relative;
            overflow: hidden;
        }
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 40px rgba(255,0,100,0.25);
        }
        .btn:active { transform: scale(0.97); }
        .btn:disabled {
            opacity: 0.4;
            cursor: not-allowed;
            transform: none !important;
            box-shadow: none !important;
        }
        .btn .btn-text { position: relative; z-index: 1; }
        .result-box {
            margin-top: 22px;
            border-radius: 16px;
            background: rgba(255,255,255,0.02);
            border: 1px solid rgba(255,255,255,0.05);
            padding: 20px;
            display: none;
            animation: fadeSlide 0.4s ease;
        }
        .result-box.show { display: block; }
        @keyframes fadeSlide {
            from { opacity: 0; transform: translateY(12px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .result-box .result-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 12px;
            padding-bottom: 10px;
            border-bottom: 1px solid rgba(255,255,255,0.04);
        }
        .result-box .result-header .status-icon { font-size: 20px; }
        .result-box .result-header .status-text {
            font-size: 15px;
            font-weight: 600;
            letter-spacing: 0.5px;
        }
        .result-box .result-header .status-text.success { color: #00e676; }
        .result-box .result-header .status-text.error { color: #ff1744; }
        .result-box .result-header .status-text.partial { color: #ffd700; }
        .result-box .result-stats {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            margin-bottom: 12px;
            padding: 12px;
            background: rgba(255,255,255,0.02);
            border-radius: 10px;
        }
        .result-box .result-stats .rstat {
            text-align: center;
        }
        .result-box .result-stats .rstat .rnum {
            font-size: 20px;
            font-weight: 700;
            font-family: 'Orbitron', sans-serif;
        }
        .result-box .result-stats .rstat .rlabel {
            font-size: 10px;
            color: rgba(255,255,255,0.25);
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .result-box .result-stats .rstat .rnum.green { color: #00e676; }
        .result-box .result-stats .rstat .rnum.red { color: #ff1744; }
        .result-box .result-stats .rstat .rnum.gold { color: #ffd700; }
        .result-details {
            max-height: 200px;
            overflow-y: auto;
            margin-top: 10px;
        }
        .result-details::-webkit-scrollbar {
            width: 4px;
        }
        .result-details::-webkit-scrollbar-track {
            background: rgba(255,255,255,0.02);
            border-radius: 2px;
        }
        .result-details::-webkit-scrollbar-thumb {
            background: rgba(255,0,100,0.3);
            border-radius: 2px;
        }
        .result-item {
            display: flex;
            justify-content: space-between;
            padding: 5px 10px;
            border-radius: 6px;
            margin-bottom: 2px;
            font-size: 13px;
            background: rgba(255,255,255,0.02);
            font-family: 'Rajdhani', sans-serif;
        }
        .result-item .ruid { color: #aaa; font-weight: 500; }
        .result-item .rmsg { font-size: 12px; }
        .result-item .rmsg.success { color: #00e676; }
        .result-item .rmsg.error { color: #ff1744; }
        .footer {
            text-align: center;
            margin-top: 20px;
            color: rgba(255,255,255,0.08);
            font-size: 11px;
            letter-spacing: 3px;
            font-weight: 300;
        }
        .footer .brand {
            background: linear-gradient(135deg, #ff0066, #cc00ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
        }
        .loader {
            display: none;
            width: 28px;
            height: 28px;
            border: 2px solid rgba(255,255,255,0.05);
            border-top-color: #ff0066;
            border-radius: 50%;
            animation: spin 0.7s linear infinite;
            margin: 0 auto 4px;
        }
        .loader.show { display: block; }
        @keyframes spin { to { transform: rotate(360deg); } }
        .status-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 600;
            letter-spacing: 1px;
            text-transform: uppercase;
        }
        .status-badge.online {
            background: rgba(0,230,118,0.1);
            color: #00e676;
            border: 1px solid rgba(0,230,118,0.2);
        }
        .status-badge.offline {
            background: rgba(255,23,68,0.1);
            color: #ff1744;
            border: 1px solid rgba(255,23,68,0.2);
        }
        .status-badge.partial {
            background: rgba(255,215,0,0.1);
            color: #ffd700;
            border: 1px solid rgba(255,215,0,0.2);
        }
        @media (max-width: 600px) {
            .container { padding: 28px 18px; }
            .header h1 { font-size: 22px; letter-spacing: 2px; }
            .form-row { grid-template-columns: 1fr; }
            .stats-bar { grid-template-columns: repeat(2, 1fr); }
            .result-box .result-stats { grid-template-columns: repeat(3, 1fr); }
            .btn { font-size: 13px; padding: 14px; }
        }
    </style>
</head>
<body>

<div class="container">
    <div class="header">
        <div class="logo">
            <span class="icon"><i class="fas fa-crown"></i></span>
            <h1>XANAF FOLLOW</h1>
        </div>
        <div class="subtitle">PREMIUM FOLLOW BOT</div>
    </div>

    <div class="stats-bar">
        <div class="stat-item">
            <div class="stat-number gold" id="totalBots">0</div>
            <div class="stat-label">Total Bots</div>
        </div>
        <div class="stat-item">
            <div class="stat-number green" id="onlineBots">0</div>
            <div class="stat-label">Online</div>
        </div>
        <div class="stat-item">
            <div class="stat-number blue" id="sentCount">0</div>
            <div class="stat-label">Sent</div>
        </div>
        <div class="stat-item">
            <div class="stat-number red" id="failedCount">0</div>
            <div class="stat-label">Failed</div>
        </div>
    </div>

    <form id="followForm" onsubmit="sendFollow(event)">
        <div class="form-row">
            <div class="form-group">
                <label><i class="fas fa-user"></i> Target UID</label>
                <div class="input-wrap">
                    <span class="icon-left"><i class="fas fa-id-card"></i></span>
                    <input type="text" id="targetUid" placeholder="Enter target UID" required>
                </div>
            </div>
            <div class="form-group">
                <label><i class="fas fa-globe"></i> Region</label>
                <div class="input-wrap">
                    <span class="icon-left"><i class="fas fa-server"></i></span>
                    <select id="regionSelect">
                        <option value="1">BD</option>
                        <option value="2">IND</option>
                        <option value="3">PK</option>
                        <option value="4">SG</option>
                        <option value="5">Taiwan</option>
                        <option value="6">TH</option>
                        <option value="7">RU</option>
                        <option value="8">ID</option>
                        <option value="9">NA</option>
                        <option value="10">BR</option>
                        <option value="11">ME</option>
                        <option value="12">VN</option>
                    </select>
                </div>
            </div>
        </div>
        <button type="submit" class="btn" id="submitBtn">
            <span class="btn-text"><i class="fas fa-bolt"></i> SEND FOLLOWS</span>
        </button>
    </form>

    <div class="loader" id="loader"></div>

    <div class="result-box" id="resultBox">
        <div class="result-header">
            <span class="status-icon" id="statusIcon"><i class="fas fa-check-circle"></i></span>
            <span class="status-text" id="statusText">Success</span>
            <span class="status-badge online" id="statusBadge">Online</span>
        </div>
        <div class="result-stats">
            <div class="rstat">
                <div class="rnum gold" id="resTotal">0</div>
                <div class="rlabel">Total</div>
            </div>
            <div class="rstat">
                <div class="rnum green" id="resSuccess">0</div>
                <div class="rlabel">Success</div>
            </div>
            <div class="rstat">
                <div class="rnum red" id="resFailed">0</div>
                <div class="rlabel">Failed</div>
            </div>
        </div>
        <div class="result-details" id="resultDetails"></div>
    </div>

    <div class="footer">
        <span class="brand">XANAF</span> &bull; PREMIUM FOLLOW BOT &bull; v5.0
    </div>
</div>

<script>
    let isProcessing = false;

    async function sendFollow(event) {
        event.preventDefault();
        if (isProcessing) return;

        const targetUid = document.getElementById('targetUid').value.trim();
        const region = document.getElementById('regionSelect').value;
        const submitBtn = document.getElementById('submitBtn');
        const loader = document.getElementById('loader');
        const resultBox = document.getElementById('resultBox');

        if (!targetUid) {
            alert('Please enter target UID');
            return;
        }

        isProcessing = true;
        submitBtn.disabled = true;
        submitBtn.querySelector('.btn-text').textContent = 'SENDING...';
        loader.classList.add('show');
        resultBox.classList.remove('show');

        try {
            const response = await fetch('/send', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ uid: targetUid, region: region })
            });
            const data = await response.json();
            displayResults(data);
        } catch (error) {
            displayResults({
                success: false,
                message: 'Network error. Please try again.',
                total: 0,
                success_count: 0,
                failed_count: 0,
                details: []
            });
        } finally {
            isProcessing = false;
            submitBtn.disabled = false;
            submitBtn.querySelector('.btn-text').textContent = 'SEND FOLLOWS';
            loader.classList.remove('show');
        }
    }

    function displayResults(data) {
        const resultBox = document.getElementById('resultBox');
        const statusIcon = document.getElementById('statusIcon');
        const statusText = document.getElementById('statusText');
        const statusBadge = document.getElementById('statusBadge');

        document.getElementById('resTotal').textContent = data.total || 0;
        document.getElementById('resSuccess').textContent = data.success_count || 0;
        document.getElementById('resFailed').textContent = data.failed_count || 0;

        document.getElementById('sentCount').textContent = data.success_count || 0;
        document.getElementById('failedCount').textContent = data.failed_count || 0;

        if (data.success && data.success_count > 0) {
            statusIcon.innerHTML = '<i class="fas fa-check-circle"></i>';
            statusText.textContent = data.message || 'Follow process completed';
            statusText.className = 'status-text success';
            statusBadge.textContent = 'Completed';
            statusBadge.className = 'status-badge online';
        } else if (data.success_count > 0 && data.failed_count > 0) {
            statusIcon.innerHTML = '<i class="fas fa-exclamation-triangle"></i>';
            statusText.textContent = data.message || 'Partial success';
            statusText.className = 'status-text partial';
            statusBadge.textContent = 'Partial';
            statusBadge.className = 'status-badge partial';
        } else {
            statusIcon.innerHTML = '<i class="fas fa-times-circle"></i>';
            statusText.textContent = data.message || 'Process failed';
            statusText.className = 'status-text error';
            statusBadge.textContent = 'Failed';
            statusBadge.className = 'status-badge offline';
        }

        const detailsDiv = document.getElementById('resultDetails');
        detailsDiv.innerHTML = '';
        if (data.details && data.details.length > 0) {
            data.details.forEach(item => {
                const div = document.createElement('div');
                div.className = 'result-item';
                const statusClass = item.success ? 'success' : 'error';
                const statusIcon = item.success ? '✓' : '✗';
                div.innerHTML = `
                    <span class="ruid">${item.uid}</span>
                    <span class="rmsg ${statusClass}">${statusIcon} ${item.message}</span>
                `;
                detailsDiv.appendChild(div);
            });
        }

        resultBox.classList.add('show');
        resultBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    async function loadStatus() {
        try {
            const response = await fetch('/status');
            const data = await response.json();
            document.getElementById('totalBots').textContent = data.total_bots || 0;
            document.getElementById('onlineBots').textContent = data.online_bots || 0;
        } catch (error) {
            console.error('Error loading status:', error);
        }
    }

    setInterval(loadStatus, 5000);
    loadStatus();
</script>

</body>
</html>'''


class FollowRequestHandler(BaseHTTPRequestHandler):
    jwt_accounts = []

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode('utf-8'))
        elif self.path == '/status':
            response = {
                'total_bots': len(FollowRequestHandler.jwt_accounts),
                'online_bots': len([a for a in FollowRequestHandler.jwt_accounts if a.get('jwt')])
            }
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/send':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                target_uid = data.get('uid', '').strip()
                region_key = data.get('region', '1')
                
                if not target_uid:
                    response = {'success': False, 'message': 'UID required', 'total': 0, 'success_count': 0, 'failed_count': 0, 'details': []}
                else:
                    try:
                        target_id = int(target_uid)
                        region = REGIONS.get(region_key, REGIONS['1'])
                        region_url = region['url']
                        region_name = region['name']
                        
                        accounts = FollowRequestHandler.jwt_accounts
                        if not accounts:
                            response = {'success': False, 'message': 'No bot accounts available', 'total': 0, 'success_count': 0, 'failed_count': 0, 'details': []}
                        else:
                            success_list = []
                            failed_list = []
                            
                            print_status(f"Sending follows to UID: {GOLD}{target_id}{RESET} on {region_name}", "loading")
                            
                            for idx, acc in enumerate(accounts, 1):
                                if not acc.get('jwt'):
                                    failed_list.append({'uid': acc['uid'], 'message': 'No JWT token', 'success': False})
                                    continue
                                
                                success, msg = send_follow(target_id, acc['jwt'], region_url)
                                if success:
                                    success_list.append({'uid': acc['uid'], 'message': msg, 'success': True})
                                    print_status(f"{GREEN}[+]{RESET} {acc['uid']} -> {msg}", "success")
                                else:
                                    failed_list.append({'uid': acc['uid'], 'message': msg, 'success': False})
                                    print_status(f"{RED}[X]{RESET} {acc['uid']} -> {msg}", "error")
                                
                                time.sleep(0.05)
                            
                            details = success_list + failed_list
                            response = {
                                'success': len(success_list) > 0,
                                'message': f'Follow process completed. {len(success_list)} successful, {len(failed_list)} failed',
                                'total': len(accounts),
                                'success_count': len(success_list),
                                'failed_count': len(failed_list),
                                'details': details
                            }
                    except ValueError:
                        response = {'success': False, 'message': 'Invalid UID format', 'total': 0, 'success_count': 0, 'failed_count': 0, 'details': []}
                        
            except Exception as e:
                response = {'success': False, 'message': f'Error: {str(e)}', 'total': 0, 'success_count': 0, 'failed_count': 0, 'details': []}
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass


def run_server():
    server = HTTPServer(('0.0.0.0', PORT), FollowRequestHandler)
    print(f"""
{GREEN}╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║   {GOLD}XANAF FOLLOW BOT - PREMIUM EDITION{RESET}                                   {GREEN}║
║                                                                      ║
║   {CYAN}Server:{RESET} http://localhost:{PORT}                                 {GREEN}║
║   {CYAN}Status:{RESET} {GREEN}Running{RESET}                                       {GREEN}║
║   {CYAN}Bots:{RESET} {WHITE}{len(FollowRequestHandler.jwt_accounts)}{RESET} loaded                              {GREEN}║
║                                                                      ║
║   {YELLOW}Press Ctrl+C to stop{RESET}                                         {GREEN}║
║                                                                      ║
{GREEN}╚══════════════════════════════════════════════════════════════════════╝{RESET}
    """)
    print(f"\n{GREEN}[+]{RESET} Web interface: {CYAN}http://localhost:{PORT}{RESET}\n")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n{YELLOW}[!]{RESET} Server stopped.")


def main():
    print_banner()
    
    region = select_region()
    region_name = region['name']
    region_url = region['url']
    
    print_status(f"Region selected: {GOLD}{region_name}{RESET}", "success")
    print_status(f"Server URL: {DIM}{region_url}{RESET}", "info")
    
    accounts = load_accounts_from_file()
    if accounts is None:
        print_status("Please add accounts to access.txt file", "error")
        print_status("Format: uid:password", "info")
        sys.exit(1)
    
    print_status(f"{GOLD}{len(accounts)}{RESET} account(s) loaded from access.txt", "success")
    
    print_status("Generating JWT tokens (Fast Mode)...", "loading")
    valid_accounts = generate_all_jwts_fast(accounts)
    
    if not valid_accounts:
        print_status("No valid JWT tokens generated. Exiting...", "error")
        sys.exit(1)
    
    save_tokens_to_file(valid_accounts, region_name)
    
    FollowRequestHandler.jwt_accounts = valid_accounts
    
    print_status(f"{GOLD}{len(valid_accounts)}{RESET} bot accounts ready", "success")
    print_status(f"Starting web server on port {GOLD}{PORT}{RESET}...", "loading")
    
    run_server()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n  {RED}[X]{RESET} Interrupted. Shutting down...")
    except Exception as e:
        print_status(f"Unexpected error: {e}", "error")