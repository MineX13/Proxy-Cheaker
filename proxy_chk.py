import requests
import concurrent.futures
import os

LOGO = r"""
███╗   ███╗██╗███╗   ██╗███████╗██╗  ██╗
████╗ ████║██║████╗  ██║██╔════╝╚██╗██╔╝
██╔████╔██║██║██╔██╗ ██║█████╗   ╚███╔╝
██║╚██╔╝██║██║██║╚██╗██║██╔══╝   ██╔██╗
██║ ╚═╝ ██║██║██║ ╚████║███████╗██╔╝ ██╗
╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
              P  R  O  X  Y   •   C H E C K E R
"""

TEST_URL = "http://httpbin.org/ip"
TIMEOUT = 7
MAX_THREADS = 100

proxy_types = ["http", "socks4", "socks5"]

# Store classified proxies
results = {
    'http': {'working': [], 'dead': []},
    'socks4': {'working': [], 'dead': []},
    'socks5': {'working': [], 'dead': []}
}

def try_proxy(proxy, ptype):
    try:
        proxies = {
            "http": f"{ptype}://{proxy}",
            "https": f"{ptype}://{proxy}"
        }
        response = requests.get(TEST_URL, proxies=proxies, timeout=TIMEOUT)
        if response.status_code == 200:
            return True
    except:
        pass
    return False

def identify_and_check(proxy):
    for ptype in proxy_types:
        if try_proxy(proxy, ptype):
            print(f"[LIVE] ({ptype.upper()}) {proxy}")
            results[ptype]['working'].append(proxy)
            return
    print(f"[DEAD] {proxy}")
    for ptype in proxy_types:
        results[ptype]['dead'].append(proxy)

def load_proxies(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        return list(set([line.strip() for line in f if line.strip()]))

def save_all_results():
    os.makedirs("results", exist_ok=True)
    for ptype in proxy_types:
        with open(f"results/{ptype}_working.txt", 'w') as f:
            f.writelines(p + '\n' for p in results[ptype]['working'])
        with open(f"results/{ptype}_dead.txt", 'w') as f:
            f.writelines(p + '\n' for p in results[ptype]['dead'])

def main():
    print(LOGO)
    print("=== Smart Proxy Type Detector & Checker ===\n")
    
    filepath = input("Enter the path to your mixed proxy file: ").strip()
    if not os.path.isfile(filepath):
        print("❌ File not found.")
        return

    proxy_list = load_proxies(filepath)
    print(f"\n📦 Loaded {len(proxy_list)} unique proxies.")
    print("⏳ Checking...\n")

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        executor.map(identify_and_check, proxy_list)

    save_all_results()
    print("\n✅ Done! Results saved in the 'results/' folder.")

if __name__ == "__main__":
    main()
