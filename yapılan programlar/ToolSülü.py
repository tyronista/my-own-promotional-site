#!/usr/bin/env python3
import socket
import hashlib
import requests

def port_scanner(ip, ports=[21, 22, 80, 443, 8080]):
    print(f"[+] Port taramasý baþlatýldý: {ip}")
    for port in ports:
        try:
            sock = socket.socket()
            sock.settimeout(1)
            sock.connect((ip, port))
            print(f"    - Port {port} açýk")
            sock.close()
        except:
            print(f"    - Port {port} kapalý")

def hash_generator(text):
    print("[+] Hash çýktýlarý:")
    print(f"    - MD5   : {hashlib.md5(text.encode()).hexdigest()}")
    print(f"    - SHA1  : {hashlib.sha1(text.encode()).hexdigest()}")
    print(f"    - SHA256: {hashlib.sha256(text.encode()).hexdigest()}")

def simple_bruteforce(hash_to_crack, wordlist_path):
    print(f"[+] Þifre kýrma baþlatýldý: {hash_to_crack}")
    try:
        with open(wordlist_path, 'r') as file:
            for line in file:
                word = line.strip()
                if hashlib.md5(word.encode()).hexdigest() == hash_to_crack:
                    print(f"    - Þifre bulundu: {word}")
                    return
        print("    - Þifre bulunamadý.")
    except FileNotFoundError:
        print("    - Wordlist dosyasý bulunamadý.")

def ip_info(ip):
    print(f"[+] IP bilgisi sorgulanýyor: {ip}")
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        data = response.json()
        for key, value in data.items():
            print(f"    - {key}: {value}")
    except:
        print("    - IP bilgisi alýnamadý.")

def menu():
    print("""
    === toolSülü ===
    1. Port Tarayýcý
    2. Hash Üreteci
    3. Basit Þifre Kýrýcý
    4. IP Bilgi Sorgulayýcý
    0. Çýkýþ
    """)
    choice = input("Seçiminiz: ")
    if choice == "1":
        ip = input("IP adresi: ")
        port_scanner(ip)
    elif choice == "2":
        text = input("Metin: ")
        hash_generator(text)
    elif choice == "3":
        hash_val = input("MD5 hash: ")
        wordlist = input("Wordlist dosya yolu: ")
        simple_bruteforce(hash_val, wordlist)
    elif choice == "4":
        ip = input("IP adresi: ")
        ip_info(ip)
    elif choice == "0":
        print("Çýkýlýyor...")
    else:
        print("Geçersiz seçim.")

if __name__ == "__main__":
    menu()
