#!/usr/bin/env python3
"""
Full Portfolio Generator and Inserter for README.md and README-ID.md.
Hierarchical 3-Tier Architecture:
- Priority 1: Milik Saya Murni / Original Core Projects (66 Repos)
- Priority 2: Fork yang Mana Saya Juga Ikut Andil (69 Contributed Forks)
- Priority 3: Selebihnya - Koleksi Cermin & Fork Terpilih (99 Starred Forks)
- Strictly Excludes All Archived Repositories (0% Archive).
"""
import json
import re

def escape_markdown(text):
    if not text:
        return ""
    # Convert github URLs to project name before stripping
    text = re.sub(r'https?://github\.com/([^/\s]+)/([^/\s]+)', r'\2', text)
    # Strip remaining bare URLs cleanly
    text = re.sub(r'https?://\S+', '', text)
    # Fix trailing conjunctions like 'and', 'with', 'based on'
    text = re.sub(r'\s+(and|with|based on)\s*$', '', text)
    # Replace pipes and newlines
    text = text.replace("|", "/").replace("\n", " ").strip()
    # Normalize multiple spaces
    text = re.sub(r'\s+', ' ', text)
    if len(text) > 85:
        text = text[:82].strip()
        text = re.sub(r'\s+(and|with|based on)\s*$', '', text)
        text += "..."
    return text.strip()

def build_tables():
    with open('/tmp/source_repos.json') as f:
        sources = json.load(f)
    with open('/tmp/contributed_forks.json') as f:
        contributed = json.load(f)
    with open('/tmp/forks.json') as f:
        all_forks = json.load(f)

    # Exclude archived
    sources = [s for s in sources if not s.get('isArchived') and s['name'] != 'MIKROTIK-SCRIPT']
    contributed = [c for c in contributed if not c.get('isArchived')]
    contributed_names = set(c['name'] for c in contributed)

    other_forks = [
        f for f in all_forks
        if f['name'] not in contributed_names and not f.get('isArchived') and f.get('stargazerCount', 0) > 0
    ]
    other_forks.sort(key=lambda x: (x.get('stargazerCount', 0), x.get('pushedAt', '')), reverse=True)

    # Generate Other Forks Table (EN)
    en_table_rows = [
        "| Repository / Mirror | Stars | Language | Focus & Upstream Reference |",
        "| :--- | :---: | :---: | :--- |"
    ]
    for f in other_forks:
        name = f['name']
        stars = f.get('stargazerCount', 0)
        lang = (f.get('primaryLanguage') or {}).get('name', 'Misc')
        desc = escape_markdown(f.get('description') or 'Upstream repository mirror and reference tool.')
        en_table_rows.append(f"| [**{name}**](https://github.com/alsyundawy/{name}) | ★ {stars} | `{lang}` | {desc} |")
    en_table_str = "\n".join(en_table_rows)

    # Generate Other Forks Table (ID)
    id_table_rows = [
        "| Repositori / Cermin | Stars | Bahasa | Fokus & Referensi Proyek |",
        "| :--- | :---: | :---: | :--- |"
    ]
    for f in other_forks:
        name = f['name']
        stars = f.get('stargazerCount', 0)
        lang = (f.get('primaryLanguage') or {}).get('name', 'Misc')
        desc = escape_markdown(f.get('description') or 'Cermin repositori hulu dan perkakas referensi.')
        id_table_rows.append(f"| [**{name}**](https://github.com/alsyundawy/{name}) | ★ {stars} | `{lang}` | {desc} |")
    id_table_str = "\n".join(id_table_rows)

    return en_table_str, id_table_str, len(sources), len(contributed), len(other_forks)

def build_portfolio_markdown_en(en_table_str):
    md = """### 🚀 Curated Repository Portfolio (680+ Public Repositories)

> 📊 **Portfolio Matrix:** **66** Original Source Repositories • **69** Actively Contributed Forks • **99+** Curated Upstream Forks • **0** Archived (Strictly Filtered)

---

#### 🌟 Priority 1: Original Core Projects (Murni Buatan Sendiri)

*High-impact production systems, authoritative DNS control planes, cross-platform utilities, and mail automation engines engineered from scratch by Harry DS Alsyundawy.*

##### 🛡️ DNS Infrastructure, RPZ & Threat Intelligence

- 📦 **[PowerDNS-Admin-PHP](https://github.com/alsyundawy/PowerDNS-Admin-PHP)** [![Stars](https://img.shields.io/github/stars/alsyundawy/PowerDNS-Admin-PHP?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/PowerDNS-Admin-PHP)<br>
  *Enterprise Authoritative PowerDNS Web Control Plane in Native PHP & PDO — Zero external runtime frameworks, <1ms sub-millisecond bootstrap, 100% offline air-gapped Zero-CDN architecture, RFC 6238 TOTP 2FA, multi-server node clustering, APCu caching, and direct PowerDNS HTTP API v1 integration.*<br>
  `PHP` `PowerDNS` `DNS` `Control-Plane` `Security` `REST-API`
- 📦 **[PHP-PDNSManager](https://github.com/alsyundawy/PHP-PDNSManager)** [![Stars](https://img.shields.io/github/stars/alsyundawy/PHP-PDNSManager?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/PHP-PDNSManager)<br>
  *Enterprise DNS Management Web GUI & REST API Gateway for PowerDNS Authoritative Server — PHP 8.1+, PSR-compliant architecture, RBAC, and high-performance zone automation.*<br>
  `PHP` `PowerDNS` `DNS` `REST-API` `Enterprise`
- 📦 **[PHP-BindManager](https://github.com/alsyundawy/PHP-BindManager)** [![Stars](https://img.shields.io/github/stars/alsyundawy/PHP-BindManager?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/PHP-BindManager)<br>
  *Enterprise-grade Web GUI for BIND9 DNS Server Management — PHP 8.4+, Bootstrap 5, Tailwind CSS, SQLite3, RBAC, DNSSEC, REST API.*<br>
  `PHP` `BIND9` `DNS` `DNSSEC` `REST-API`
- 📦 **[TrustPositif-To-RPZ-Binary](https://github.com/alsyundawy/TrustPositif-To-RPZ-Binary)** [![Stars](https://img.shields.io/github/stars/alsyundawy/TrustPositif-To-RPZ-Binary?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/TrustPositif-To-RPZ-Binary)<br>
  *Converts Kominfo TrustPositif domains into DNS RPZ format. Features whitelist & Google SafeSearch helper.*<br>
  `Go` `Shell` `DNS` `RPZ` `Blocklist`
- 📦 **[TrustPositif](https://github.com/alsyundawy/TrustPositif)** [![Stars](https://img.shields.io/github/stars/alsyundawy/TrustPositif?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/TrustPositif)<br>
  *Comprehensive raw TrustPositif domain database with daily automated updates.*<br>
  `Database` `Kominfo` `Blocklist`
- 📦 **[TrustPositif-Validator](https://github.com/alsyundawy/TrustPositif-Validator)** [![Stars](https://img.shields.io/github/stars/alsyundawy/TrustPositif-Validator?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/TrustPositif-Validator)<br>
  *High-performance domain validation, IDN Punycode normalization & blocklist aggregation pipeline for TrustPositif/Komdigi. ShellCheck Certified.*<br>
  `Shell` `Validator` `RFC-Compliant` `Punycode`
- 📦 **[sunat-trustpositif](https://github.com/alsyundawy/sunat-trustpositif)** [![Stars](https://img.shields.io/github/stars/alsyundawy/sunat-trustpositif?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/sunat-trustpositif)<br>
  *Shell script that validates domain lists against official IANA TLDs and cleanses database records.*<br>
  `Shell` `TLD` `Data-Cleansing`
- 📦 **[StevenBlack-Host-RPZ](https://github.com/alsyundawy/StevenBlack-Host-RPZ)** [![Stars](https://img.shields.io/github/stars/alsyundawy/StevenBlack-Host-RPZ?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/StevenBlack-Host-RPZ)<br>
  *Converts the StevenBlack host lists to DNS RPZ format.*<br>
  `DNS` `RPZ` `StevenBlack`
- 📦 **[PowerDNS-Zone-Backups](https://github.com/alsyundawy/PowerDNS-Zone-Backups)** [![Stars](https://img.shields.io/github/stars/alsyundawy/PowerDNS-Zone-Backups?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/PowerDNS-Zone-Backups)<br>
  *Automated PowerDNS zone backup solution with incremental backups and retention rotation.*<br>
  `PowerDNS` `Backup` `Database`
- 📦 **[bind-acl-indonesia-openixp](https://github.com/alsyundawy/bind-acl-indonesia-openixp)** [![Stars](https://img.shields.io/github/stars/alsyundawy/bind-acl-indonesia-openixp?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/bind-acl-indonesia-openixp)<br>
  *Automatically generates Indonesian IP ACL files for BIND9 DNS using Nice.rsc and APNIC data.*<br>
  `BIND9` `ACL` `OpenIXP` `APNIC`
- 📦 **[IP2RPZ](https://github.com/alsyundawy/IP2RPZ)** [![Stars](https://img.shields.io/github/stars/alsyundawy/IP2RPZ?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/IP2RPZ)<br>
  *High-speed C utility to convert IP threat feeds into DNS RPZ format.*<br>
  `C` `DNS` `RPZ` `Firewall`
- 📦 **[dnstrust-apjii](https://github.com/alsyundawy/dnstrust-apjii)** [![Stars](https://img.shields.io/github/stars/alsyundawy/dnstrust-apjii?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/dnstrust-apjii)<br>
  *DNS-Trust Database BIND9 || DNS Bersih TrustPositif APJII.*<br>
  `DNS` `BIND9` `APJII` `TrustPositif`

##### 🖥️ Diagnostics, Telemetry, Subnetting & IPAM

- 📦 **[php-looking-glass](https://github.com/alsyundawy/php-looking-glass)** [![Stars](https://img.shields.io/github/stars/alsyundawy/php-looking-glass?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/php-looking-glass)<br>
  *A professional, secure, single-file PHP Looking Glass for network diagnostics (Ping, Traceroute, MTR, WHOIS, DNS Lookup, Iperf3).*<br>
  `PHP` `Network` `Looking-Glass` `MTR`
- 📦 **[SubNetCalc-Electron](https://github.com/alsyundawy/SubNetCalc-Electron)** [![Stars](https://img.shields.io/github/stars/alsyundawy/SubNetCalc-Electron?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/SubNetCalc-Electron)<br>
  *High-Precision, Low-Footprint IPv4 & IPv6 Subnet Calculator with 14 Multi-Themes for macOS & Cross-Platform desktop. Powered by Electron 44, React 19, and TypeScript with real-time RFC classification and binary bit visualization.*<br>
  `TypeScript` `Electron` `React` `Networking` `Subnetting` `Cross-Platform`
- 📦 **[SubnetCalc-Windows](https://github.com/alsyundawy/SubnetCalc-Windows)** [![Stars](https://img.shields.io/github/stars/alsyundawy/SubnetCalc-Windows?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/SubnetCalc-Windows)<br>
  *High-Performance, Native C11 & Win32 IPv4 & IPv6 Subnet Calculator for Windows (x86/x64) with instant memory rendering and themes.*<br>
  `C` `Win32` `Subnetting` `Networking` `Windows`
- 📦 **[dnsperftest](https://github.com/alsyundawy/dnsperftest)** [![Stars](https://img.shields.io/github/stars/alsyundawy/dnsperftest?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/dnsperftest)<br>
  *Comprehensive DNS benchmark, latency evaluation, and public resolver performance tester.*<br>
  `Shell` `DNS` `Benchmark` `Latency`
- 📦 **[File-Directory-Browser](https://github.com/alsyundawy/File-Directory-Browser)** [![Stars](https://img.shields.io/github/stars/alsyundawy/File-Directory-Browser?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/File-Directory-Browser)<br>
  *Lightweight, security-hardened single-file PHP directory browser featuring CSRF protection, output sanitization, and SHA-256 hash checks.*<br>
  `PHP` `Security` `File-Manager`
- 📦 **[bailu-kilo-agent](https://github.com/alsyundawy/bailu-kilo-agent)** [![Stars](https://img.shields.io/github/stars/alsyundawy/bailu-kilo-agent?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/bailu-kilo-agent)<br>
  *Agentic coding sidebar for BAILU AI — Kilo-style panel, model picker, Auto, thinking mode, and API token integration for VS Code & Code-OSS forks.*<br>
  `TypeScript` `VSCode` `AI-Agent` `Agentic-Coding` `Extension`

##### ✉️ Mail Systems & Zimbra Collaboration Suite

- 📦 **[eradicate-zimbra-malware](https://github.com/alsyundawy/eradicate-zimbra-malware)** [![Stars](https://img.shields.io/github/stars/alsyundawy/eradicate-zimbra-malware?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/eradicate-zimbra-malware)<br>
  *Enterprise Forensic Incident Response, Anti-Ransomware, Polyglot Webshell Quarantine & Zimbra Permission Healing Suite.*<br>
  `Shell` `Security` `Forensics` `Zimbra` `Incident-Response`
- 📦 **[Zimbra-Link-Installer](https://github.com/alsyundawy/Zimbra-Link-Installer)** [![Stars](https://img.shields.io/github/stars/alsyundawy/Zimbra-Link-Installer?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/Zimbra-Link-Installer)<br>
  *The Complete Zimbra Collaboration Archive & Installer Suite. Direct binary downloads, official & community builds, cryptographic checksums, and automated CLI installer (ZCS 4.5.x – 10.1.x).*<br>
  `Shell` `HTML` `Zimbra` `Installer` `Mail-Server`
- 📦 **[Z2C (Zimbra to Carbonio Migration)](https://github.com/alsyundawy/Z2C)** [![Stars](https://img.shields.io/github/stars/alsyundawy/Z2C?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/Z2C)<br>
  *Zimbra to Carbonio Migration tool. A set of scripts to export domains, accounts, aliases, and mailboxes, supporting parallel migration.*<br>
  `Shell` `Zimbra` `Carbonio` `Migration`
- 📦 **[cmbackup](https://github.com/alsyundawy/cmbackup)** [![Stars](https://img.shields.io/github/stars/alsyundawy/cmbackup?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/cmbackup)<br>
  *Next-generation hot backup, restore, and migration engine from Zimbra to Carbonio.*<br>
  `Shell` `Carbonio` `Zimbra` `Backup`
- 📦 **[uninstall-zimbra](https://github.com/alsyundawy/uninstall-zimbra)** [![Stars](https://img.shields.io/github/stars/alsyundawy/uninstall-zimbra?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/uninstall-zimbra)<br>
  *Complete Bash utility to clean-uninstall Zimbra instances from Linux.*<br>
  `Zimbra` `Uninstaller` `Bash`
- 📦 **[Zimbra-Clean-Spam](https://github.com/alsyundawy/Zimbra-Clean-Spam)** [![Stars](https://img.shields.io/github/stars/alsyundawy/Zimbra-Clean-Spam?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/Zimbra-Clean-Spam)<br>
  *Scan and purge spam email queues caused by compromised accounts.*<br>
  `Zimbra` `Mail-Server` `Spam-Cleaner`

##### ☁️ Desktop Apps, macOS, Hypervisors & System Engineering

- 📦 **[Microsoft-Office-For-MacOS](https://github.com/alsyundawy/Microsoft-Office-For-MacOS)** [![Stars](https://img.shields.io/github/stars/alsyundawy/Microsoft-Office-For-MacOS?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/Microsoft-Office-For-MacOS)<br>
  *Complete Mac installer bundle for Microsoft Office (Intel/Apple Silicon) with LTSC volume serializer.*<br>
  `Shell` `macOS` `Installer` `Office` `Apple-Silicon`
- 📦 **[SparkNotePad](https://github.com/alsyundawy/SparkNotePad)** [![Stars](https://img.shields.io/github/stars/alsyundawy/SparkNotePad?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/SparkNotePad)<br>
  *Lightweight, blazing-fast native Scintilla & Qt text and source code editor for Linux and macOS. Engineered with ISO C++20, Qt 6, and Scintilla 5.6.7 / Lexilla 5.5.4 core for minimal memory footprint (<35MB), instant rendering, AES-256 encryption, and 75 developer themes.*<br>
  `C++20` `Qt6` `Scintilla` `macOS` `Linux` `FreeBSD` `Code-Editor`
- 📦 **[XiaomiADBFastbootTools-Win32](https://github.com/alsyundawy/XiaomiADBFastbootTools-Win32)** [![Stars](https://img.shields.io/github/stars/alsyundawy/XiaomiADBFastbootTools-Win32?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/XiaomiADBFastbootTools-Win32)<br>
  *ADB and fastboot tools optimized for Xiaomi devices on Windows.*<br>
  `C#` `Windows` `ADB` `Fastboot` `Xiaomi`
- 📦 **[PnetLab-v8](https://github.com/alsyundawy/PnetLab-v8)** [![Stars](https://img.shields.io/github/stars/alsyundawy/PnetLab-v8?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/PnetLab-v8)<br>
  *Enterprise network virtualization & emulation platform on Ubuntu 26.04 LTS (Resolute). Turn-key OVA, ISO, and Proxmox VE 8+ deployment guide.*<br>
  `Ubuntu` `Proxmox` `Virtualization` `Network-Emulation` `PNETLab` `KVM`
- 📦 **[NotepadNext-MacOS](https://github.com/alsyundawy/NotepadNext-MacOS)** [![Stars](https://img.shields.io/github/stars/alsyundawy/NotepadNext-MacOS?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/NotepadNext-MacOS)<br>
  *Native macOS reimplementation of Notepad++ built with Qt 6. Fast, lightweight, and modern.*<br>
  `C++` `macOS` `NotepadNext` `Editor` `Qt6`
- 📦 **[openssl-1.0.2](https://github.com/alsyundawy/openssl-1.0.2)** [![Stars](https://img.shields.io/github/stars/alsyundawy/openssl-1.0.2?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/openssl-1.0.2)<br>
  *Production-grade security hardened fork and backported CVE mitigations for legacy OpenSSL 1.0.2 (up to 1.0.2zr).*<br>
  `C` `OpenSSL` `Security` `Hardening` `CVE-Mitigation` `Backport`
- 📦 **[Disable-MacOS-Updates](https://github.com/alsyundawy/Disable-MacOS-Updates)** [![Stars](https://img.shields.io/github/stars/alsyundawy/Disable-MacOS-Updates?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/Disable-MacOS-Updates)<br>
  *Reversible Bash scripts to disable automatic software updates on macOS (Monterey to Golden Gate).*<br>
  `macOS` `Bash` `Apple-Silicon` `DAW` `Sysadmin`
- 📦 **[mikrotik-blacklist](https://github.com/alsyundawy/mikrotik-blacklist)** [![Stars](https://img.shields.io/github/stars/alsyundawy/mikrotik-blacklist?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/mikrotik-blacklist)<br>
  *RouterOS automated threat intelligence blacklist updates and firewall address-lists.*<br>
  `RouterOS` `Blacklist` `Security`

---

#### 🛠️ Priority 2: Actively Contributed & Patched Forks (Fork dengan Kontribusi Nyata)

*Upstream open-source repositories where Harry DS Alsyundawy authored direct commits, security hardening, or maintained mission-critical forks.*

- 📦 **[PowerDNS-Admin](https://github.com/alsyundawy/PowerDNS-Admin)** [![Stars](https://img.shields.io/github/stars/alsyundawy/PowerDNS-Admin?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/PowerDNS-Admin) `[136 Commits]`<br>
  *Enterprise web control panel for PowerDNS Authoritative Server with custom MariaDB pooling, LDAP optimizations, and UI enhancements.*<br>
  `Python` `PowerDNS` `DNS` `Web-GUI` `Enterprise`
- 📦 **[shc](https://github.com/alsyundawy/shc)** [![Stars](https://img.shields.io/github/stars/alsyundawy/shc?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/shc) `[54 Commits]`<br>
  *Generic Shell Script Compiler with Enhanced Security & Auditing. Encrypts and compiles shell scripts into stripped binary executables.*<br>
  `C` `Shell` `Security` `Auditing` `Hardening`
- 📦 **[visualsubnetcalc](https://github.com/alsyundawy/visualsubnetcalc)** [![Stars](https://img.shields.io/github/stars/alsyundawy/visualsubnetcalc?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/visualsubnetcalc) `[49 Commits]`<br>
  *Visual Subnet Calculator — Modernized & Hardened Edition. Visual, interactive IPv4/IPv6 CIDR subnet planner with real-time bit splitting and zero server-side storage.*<br>
  `TypeScript` `Networking` `Subnetting` `IPv4` `CIDR`
- 📦 **[zmbackup](https://github.com/alsyundawy/zmbackup)** [![Stars](https://img.shields.io/github/stars/alsyundawy/zmbackup?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/zmbackup) `[47 Commits]`<br>
  *Enterprise Multi-Threaded Hot Backup, Zero-Timeout Restore, Cross-OS Migration Engine & Security Hardening for Zimbra Collaboration Suite & Carbonio.*<br>
  `Shell` `Zimbra` `Backup` `Disaster-Recovery` `Migration`
- 📦 **[pear-desktop-mac](https://github.com/alsyundawy/pear-desktop-mac)** [![Stars](https://img.shields.io/github/stars/alsyundawy/pear-desktop-mac?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/pear-desktop-mac) `[44 Commits]`<br>
  *High-performance, privacy-hardened macOS desktop client for YouTube Music with built-in ad blocker (27+ vendor filters), SponsorBlock, and synced lyrics.*<br>
  `macOS` `Apple-Silicon` `YouTube-Music` `Electron` `TypeScript`
- 📦 **[SmartDNS](https://github.com/alsyundawy/SmartDNS)** [![Stars](https://img.shields.io/github/stars/alsyundawy/SmartDNS?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/SmartDNS) `[43 Commits]`<br>
  *Automated DNS resolver platform for ISP & enterprise networks with multi-upstream routing and latency-based failover.*<br>
  `HTML` `JavaScript` `DNS` `Resolver` `Routing`
- 📦 **[SubnetCalc-MacOS](https://github.com/alsyundawy/SubnetCalc-MacOS)** [![Stars](https://img.shields.io/github/stars/alsyundawy/SubnetCalc-MacOS?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/SubnetCalc-MacOS) `[32 Commits]`<br>
  *High-Performance, Native Swift & Cocoa IPv4 & IPv6 Subnet Calculator for macOS (Universal 2: Apple Silicon M1-M4 & Intel x64) with 25 developer theme suites.*<br>
  `Swift` `macOS` `Apple-Silicon` `AppKit` `Cocoa` `Subnetting` `IPAM`
- 📦 **[ufw-ipset-blocklist-autoupdate](https://github.com/alsyundawy/ufw-ipset-blocklist-autoupdate)** [![Stars](https://img.shields.io/github/stars/alsyundawy/ufw-ipset-blocklist-autoupdate?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/ufw-ipset-blocklist-autoupdate) `[27 Commits]`<br>
  *Automatically updates IP blocking lists via ipset and UFW firewalls with threat intelligence feeds.*<br>
  `Shell` `UFW` `Ipset` `Security` `Firewall`
- 📦 **[OpenVPN-Install](https://github.com/alsyundawy/OpenVPN-Install)** [![Stars](https://img.shields.io/github/stars/alsyundawy/OpenVPN-Install?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/OpenVPN-Install) `[24 Commits]`<br>
  *OpenVPN road warrior installer for Debian, Ubuntu, and CentOS with dual-stack IPv4/IPv6 and Unbound DNS integration.*<br>
  `Shell` `OpenVPN` `VPN` `Security` `Networking`
- 📦 **[cyberpanel](https://github.com/alsyundawy/cyberpanel)** [![Stars](https://img.shields.io/github/stars/alsyundawy/cyberpanel?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/cyberpanel) `[21 Commits]`<br>
  *Hosting control panel for OpenLiteSpeed with custom security patches and environment optimizations.*<br>
  `JavaScript` `Python` `Hosting` `LiteSpeed` `Control-Panel`
- 📦 **[esxi-unlocker-v4](https://github.com/alsyundawy/esxi-unlocker-v4)** [![Stars](https://img.shields.io/github/stars/alsyundawy/esxi-unlocker-v4?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/esxi-unlocker-v4) `[11 Commits]`<br>
  *macOS Unlocker V4 for VMware ESXi. Enables Apple macOS guest support on VMware ESXi hypervisors with maintained shell/Python patching workflow.*<br>
  `Python` `VMware` `ESXi` `macOS` `Hypervisor`
- 📦 **[Zimbra2Zimbra-Migration-Tool](https://github.com/alsyundawy/Zimbra2Zimbra-Migration-Tool)** [![Stars](https://img.shields.io/github/stars/alsyundawy/Zimbra2Zimbra-Migration-Tool?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/Zimbra2Zimbra-Migration-Tool) `[11 Commits]`<br>
  *Z2Z — Zimbra to Zimbra Migration Suite. Enterprise zero-timeout, cross-version, and zero-data-loss migration engine for ZCS 7.x – 10.1.x.*<br>
  `Shell` `Zimbra` `Migration` `Backup` `Mail-Server`
- 📦 **[Windows10Debloater](https://github.com/alsyundawy/Windows10Debloater)** [![Stars](https://img.shields.io/github/stars/alsyundawy/Windows10Debloater?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/Windows10Debloater) `[6 Commits]`<br>
  *PowerShell script to remove Windows 10/11 bloatware, disable telemetry, and stop unwanted background tasks.*<br>
  `PowerShell` `Windows` `Debloat` `System-Tuning`
- 📦 **[OpenSID](https://github.com/alsyundawy/OpenSID)** [![Stars](https://img.shields.io/github/stars/alsyundawy/OpenSID?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/OpenSID) `[5 Commits]`<br>
  *Sistem Informasi Desa (SID) open-source with PHP 8+ tuning and server security enhancements.*<br>
  `PHP` `OpenSID` `Government` `Indonesia`
- 📦 **[Linux-System-Management-Scripts-Tricks](https://github.com/alsyundawy/Linux-System-Management-Scripts-Tricks)** [![Stars](https://img.shields.io/github/stars/alsyundawy/Linux-System-Management-Scripts-Tricks?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/Linux-System-Management-Scripts-Tricks) `[4 Commits]`<br>
  *Linux System Administrator & Engineer automation scripts, monitoring snippets, and certification tricks.*<br>
  `Shell` `Linux` `Sysadmin` `DevOps`
- 📦 **[wireguard-install](https://github.com/alsyundawy/wireguard-install)** [![Stars](https://img.shields.io/github/stars/alsyundawy/wireguard-install?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/wireguard-install) `[2 Commits]`<br>
  *WireGuard road warrior installer for Ubuntu, Debian, CentOS, and Fedora with QR-code profile generator.*<br>
  `Shell` `WireGuard` `VPN` `Security`
- 📦 **[AutoInstallGenieACS](https://github.com/alsyundawy/AutoInstallGenieACS)** [![Stars](https://img.shields.io/github/stars/alsyundawy/AutoInstallGenieACS?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/AutoInstallGenieACS) `[1 Commit]`<br>
  *Automated installation and service provisioning script for GenieACS TR-069 server on Debian/Ubuntu.*<br>
  `Shell` `GenieACS` `TR-069` `ISP`
- 📦 **[dnsdist-one-click](https://github.com/alsyundawy/dnsdist-one-click)** [![Stars](https://img.shields.io/github/stars/alsyundawy/dnsdist-one-click?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/dnsdist-one-click) `[1 Commit]`<br>
  *One-click installer for DNSDist load balancer with automated Komdigi TrustPositif filtering rules.*<br>
  `Shell` `DNSDist` `DNS` `TrustPositif` `Load-Balancer`
- 📦 **[SlimBrave-Neo](https://github.com/alsyundawy/SlimBrave-Neo)** [![Stars](https://img.shields.io/github/stars/alsyundawy/SlimBrave-Neo)](https://github.com/alsyundawy/SlimBrave-Neo) `[1 Commit]`<br>
  *Debloat and harden Brave Browser on Linux and macOS for privacy and performance.*<br>
  `Python` `Brave` `Privacy` `Debloat`

---

#### 📚 Priority 3: Curated Upstream Forks & Reference Mirrors (Non-Archived)

*Carefully maintained upstream mirrors, network security toolkits, and curated development resources. Strictly excludes all archived repositories.*

<details>
<summary><b>📂 Expand Complete Directory of 99+ Active Starred Upstream Forks & Mirrors</b> (Click to view table)</summary>

""" + en_table_str + """

</details>"""
    return md

def build_portfolio_markdown_id(id_table_str):
    md = """### 🚀 Portofolio Repositori Terkurasi (680+ Repositori Publik)

> 📊 **Matriks Portofolio:** **66** Repositori Murni / Original • **69** Fork dengan Kontribusi Nyata • **99+** Fork & Cermin Referensi Terpilih • **0** Arsip (Bebas dari Repositori Terarsip)

---

#### 🌟 Prioritas 1: Repositori Murni / Original (Karya Mandiri)

*Sistem produksi enterprise, control plane DNS authoritative, utilitas lintas platform, dan otomatisasi mail server yang dibangun langsung dari nol oleh Harry DS Alsyundawy.*

##### 🛡️ Infrastruktur DNS, RPZ & Intelijen Ancaman

- 📦 **[PowerDNS-Admin-PHP](https://github.com/alsyundawy/PowerDNS-Admin-PHP)** [![Stars](https://img.shields.io/github/stars/alsyundawy/PowerDNS-Admin-PHP?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/PowerDNS-Admin-PHP)<br>
  *Control plane web PowerDNS Authoritative mandiri berbasis Native PHP & PDO — Tanpa framework eksternal, bootstrap sub-milidetik (<1ms), arsitektur Zero-CDN 100% offline, 2FA TOTP RFC 6238, kluster multi-server, cache APCu, dan integrasi langsung PowerDNS HTTP API v1.*<br>
  `PHP` `PowerDNS` `DNS` `Control-Plane` `Security` `REST-API`
- 📦 **[PHP-PDNSManager](https://github.com/alsyundawy/PHP-PDNSManager)** [![Stars](https://img.shields.io/github/stars/alsyundawy/PHP-PDNSManager?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/PHP-PDNSManager)<br>
  *Web GUI Manajemen DNS Enterprise & REST API Gateway untuk PowerDNS Authoritative Server — PHP 8.1+, arsitektur sesuai PSR, RBAC, dan otomatisasi zona performa tinggi.*<br>
  `PHP` `PowerDNS` `DNS` `REST-API` `Enterprise`
- 📦 **[PHP-BindManager](https://github.com/alsyundawy/PHP-BindManager)** [![Stars](https://img.shields.io/github/stars/alsyundawy/PHP-BindManager?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/PHP-BindManager)<br>
  *Web GUI modern pengelolaan server DNS BIND9 — PHP 8.4+, Bootstrap 5, Tailwind CSS, SQLite3, RBAC, DNSSEC, REST API.*<br>
  `PHP` `BIND9` `DNS` `DNSSEC` `REST-API`
- 📦 **[TrustPositif-To-RPZ-Binary](https://github.com/alsyundawy/TrustPositif-To-RPZ-Binary)** [![Stars](https://img.shields.io/github/stars/alsyundawy/TrustPositif-To-RPZ-Binary?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/TrustPositif-To-RPZ-Binary)<br>
  *Generator konversi domain TrustPositif Kominfo ke format DNS RPZ biner berkecepatan tinggi dengan whitelist & Google SafeSearch.*<br>
  `Go` `Shell` `DNS` `RPZ` `Blocklist`
- 📦 **[TrustPositif](https://github.com/alsyundawy/TrustPositif)** [![Stars](https://img.shields.io/github/stars/alsyundawy/TrustPositif?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/TrustPositif)<br>
  *Database domain TrustPositif Kominfo terstandarisasi dengan pembaruan otomatis harian.*<br>
  `Database` `Kominfo` `Blocklist`
- 📦 **[TrustPositif-Validator](https://github.com/alsyundawy/TrustPositif-Validator)** [![Stars](https://img.shields.io/github/stars/alsyundawy/TrustPositif-Validator?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/TrustPositif-Validator)<br>
  *Pipeline validasi dan agregasi domain berkinerja tinggi untuk TrustPositif/Komdigi dan daftar blokir publik. Tersertifikasi ShellCheck.*<br>
  `Shell` `Validator` `RFC-Compliant` `Punycode`
- 📦 **[sunat-trustpositif](https://github.com/alsyundawy/sunat-trustpositif)** [![Stars](https://img.shields.io/github/stars/alsyundawy/sunat-trustpositif?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/sunat-trustpositif)<br>
  *Skrip shell pembersih dan validasi daftar domain terhadap TLD resmi IANA untuk integritas database.*<br>
  `Shell` `TLD` `Data-Cleansing`
- 📦 **[StevenBlack-Host-RPZ](https://github.com/alsyundawy/StevenBlack-Host-RPZ)** [![Stars](https://img.shields.io/github/stars/alsyundawy/StevenBlack-Host-RPZ?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/StevenBlack-Host-RPZ)<br>
  *Konverter daftar host StevenBlack ke format DNS RPZ.*<br>
  `DNS` `RPZ` `StevenBlack`
- 📦 **[PowerDNS-Zone-Backups](https://github.com/alsyundawy/PowerDNS-Zone-Backups)** [![Stars](https://img.shields.io/github/stars/alsyundawy/PowerDNS-Zone-Backups?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/PowerDNS-Zone-Backups)<br>
  *Solusi backup zona PowerDNS otomatis dengan rotasi backup inkremental.*<br>
  `PowerDNS` `Backup` `Database`
- 📦 **[bind-acl-indonesia-openixp](https://github.com/alsyundawy/bind-acl-indonesia-openixp)** [![Stars](https://img.shields.io/github/stars/alsyundawy/bind-acl-indonesia-openixp?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/bind-acl-indonesia-openixp)<br>
  *Pembuat otomatis berkas ACL IP alokasi Indonesia dan OpenIXP untuk mengamankan rekursi DNS BIND9.*<br>
  `BIND9` `ACL` `OpenIXP` `APNIC`
- 📦 **[IP2RPZ](https://github.com/alsyundawy/IP2RPZ)** [![Stars](https://img.shields.io/github/stars/alsyundawy/IP2RPZ?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/IP2RPZ)<br>
  *Utilitas C berkecepatan tinggi untuk mengonversi daftar feed ancaman IP menjadi aturan firewall DNS RPZ.*<br>
  `C` `DNS` `RPZ` `Firewall`
- 📦 **[dnstrust-apjii](https://github.com/alsyundawy/dnstrust-apjii)** [![Stars](https://img.shields.io/github/stars/alsyundawy/dnstrust-apjii?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/dnstrust-apjii)<br>
  *Database DNS-Trust BIND9 || DNS Bersih TrustPositif APJII.*<br>
  `DNS` `BIND9` `APJII` `TrustPositif`

##### 🖥️ Diagnostik, Telemetri, Subnetting & IPAM

- 📦 **[php-looking-glass](https://github.com/alsyundawy/php-looking-glass)** [![Stars](https://img.shields.io/github/stars/alsyundawy/php-looking-glass?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/php-looking-glass)<br>
  *Looking Glass PHP single-file profesional dan aman untuk diagnostik jaringan (Ping, Traceroute, MTR, WHOIS, DNS, Iperf3).*<br>
  `PHP` `Network` `Looking-Glass` `MTR`
- 📦 **[SubNetCalc-Electron](https://github.com/alsyundawy/SubNetCalc-Electron)** [![Stars](https://img.shields.io/github/stars/alsyundawy/SubNetCalc-Electron?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/SubNetCalc-Electron)<br>
  *Kalkulator subnet desktop presisi tinggi dengan 14 multi-tema untuk macOS dan lintas platform. Ditenagai Electron 44, React 19, dan TypeScript dengan klasifikasi RFC real-time.*<br>
  `TypeScript` `Electron` `React` `Networking` `Subnetting` `Cross-Platform`
- 📦 **[SubnetCalc-Windows](https://github.com/alsyundawy/SubnetCalc-Windows)** [![Stars](https://img.shields.io/github/stars/alsyundawy/SubnetCalc-Windows?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/SubnetCalc-Windows)<br>
  *Kalkulator subnet IPv4 & IPv6 native C11 & Win32 berkinerja tinggi untuk Windows (x86/x64) dengan perenderan memori instan dan ragam tema.*<br>
  `C` `Win32` `Subnetting` `Networking` `Windows`
- 📦 **[dnsperftest](https://github.com/alsyundawy/dnsperftest)** [![Stars](https://img.shields.io/github/stars/alsyundawy/dnsperftest?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/dnsperftest)<br>
  *Alat tolok ukur komprehensif performa dan latensi resolver DNS publik.*<br>
  `Shell` `DNS` `Benchmark` `Latency`
- 📦 **[File-Directory-Browser](https://github.com/alsyundawy/File-Directory-Browser)** [![Stars](https://img.shields.io/github/stars/alsyundawy/File-Directory-Browser?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/File-Directory-Browser)<br>
  *File browser PHP ringan dan diperkeras dengan proteksi CSRF, sanitasi output, dan verifikasi hash SHA-256.*<br>
  `PHP` `Security` `File-Manager`
- 📦 **[bailu-kilo-agent](https://github.com/alsyundawy/bailu-kilo-agent)** [![Stars](https://img.shields.io/github/stars/alsyundawy/bailu-kilo-agent?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/bailu-kilo-agent)<br>
  *Panel bilah sisi agentic coding untuk BAILU AI — panel gaya Kilo, pemilih model, mode pemikiran, dan token API untuk VS Code.*<br>
  `TypeScript` `VSCode` `AI-Agent` `Agentic-Coding` `Extension`

##### ✉️ Sistem Email & Zimbra Collaboration Suite

- 📦 **[eradicate-zimbra-malware](https://github.com/alsyundawy/eradicate-zimbra-malware)** [![Stars](https://img.shields.io/github/stars/alsyundawy/eradicate-zimbra-malware?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/eradicate-zimbra-malware)<br>
  *Suite respons insiden forensik enterprise, anti-ransomware, karantina webshell poliglota & perbaikan hak akses Zimbra.*<br>
  `Shell` `Security` `Forensics` `Zimbra` `Incident-Response`
- 📦 **[Zimbra-Link-Installer](https://github.com/alsyundawy/Zimbra-Link-Installer)** [![Stars](https://img.shields.io/github/stars/alsyundawy/Zimbra-Link-Installer?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/Zimbra-Link-Installer)<br>
  *Arsip lengkap binary dan installer Zimbra Collaboration Suite (ZCS 4.5.x – 10.1.x) resmi dan komunitas dengan verifikasi checksum kriptografis.*<br>
  `Shell` `HTML` `Zimbra` `Installer` `Mail-Server`
- 📦 **[Z2C (Zimbra to Carbonio Migration)](https://github.com/alsyundawy/Z2C)** [![Stars](https://img.shields.io/github/stars/alsyundawy/Z2C?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/Z2C)<br>
  *Alat migrasi Zimbra ke Carbonio untuk ekspor domain, akun, alias, dan mailbox secara paralel.*<br>
  `Shell` `Zimbra` `Carbonio` `Migration`
- 📦 **[cmbackup](https://github.com/alsyundawy/cmbackup)** [![Stars](https://img.shields.io/github/stars/alsyundawy/cmbackup?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/cmbackup)<br>
  *Mesin hot backup, restore, dan migrasi generasi terbaru dari Zimbra ke Carbonio.*<br>
  `Shell` `Carbonio` `Zimbra` `Backup`
- 📦 **[uninstall-zimbra](https://github.com/alsyundawy/uninstall-zimbra)** [![Stars](https://img.shields.io/github/stars/alsyundawy/uninstall-zimbra?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/uninstall-zimbra)<br>
  *Utilitas Bash lengkap untuk mencopot pemasangan Zimbra secara bersih dari server Linux.*<br>
  `Zimbra` `Uninstaller` `Bash`
- 📦 **[Zimbra-Clean-Spam](https://github.com/alsyundawy/Zimbra-Clean-Spam)** [![Stars](https://img.shields.io/github/stars/alsyundawy/Zimbra-Clean-Spam?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/Zimbra-Clean-Spam)<br>
  *Pindai dan bersihkan antrian email spam yang disebabkan oleh akun terkompromi.*<br>
  `Zimbra` `Mail-Server` `Spam-Cleaner`

##### ☁️ Aplikasi Desktop, macOS, Hypervisor & Utilitas Sistem

- 📦 **[Microsoft-Office-For-MacOS](https://github.com/alsyundawy/Microsoft-Office-For-MacOS)** [![Stars](https://img.shields.io/github/stars/alsyundawy/Microsoft-Office-For-MacOS?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/Microsoft-Office-For-MacOS)<br>
  *Paket installer lengkap Microsoft Office untuk Mac (Intel & Apple Silicon) dengan serializer volume LTSC.*<br>
  `Shell` `macOS` `Installer` `Office` `Apple-Silicon`
- 📦 **[SparkNotePad](https://github.com/alsyundawy/SparkNotePad)** [![Stars](https://img.shields.io/github/stars/alsyundawy/SparkNotePad?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/SparkNotePad)<br>
  *Editor teks dan kode sumber native berkinerja tinggi berbasis Scintilla & Qt untuk Linux dan macOS. Diprogram dengan C++20, Qt 6, dan engine Scintilla 5.6.7 / Lexilla 5.5.4 untuk efisiensi memori (<35MB), perenderan baris instan, enkripsi dokumen AES-256, serta 75 tema pengembang.*<br>
  `C++20` `Qt6` `Scintilla` `macOS` `Linux` `FreeBSD` `Code-Editor`
- 📦 **[XiaomiADBFastbootTools-Win32](https://github.com/alsyundawy/XiaomiADBFastbootTools-Win32)** [![Stars](https://img.shields.io/github/stars/alsyundawy/XiaomiADBFastbootTools-Win32?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/XiaomiADBFastbootTools-Win32)<br>
  *Alat bantu ADB dan Fastboot yang dioptimalkan untuk perangkat Xiaomi Android pada lingkungan Windows.*<br>
  `C#` `Windows` `ADB` `Fastboot` `Xiaomi`
- 📦 **[PnetLab-v8](https://github.com/alsyundawy/PnetLab-v8)** [![Stars](https://img.shields.io/github/stars/alsyundawy/PnetLab-v8?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/PnetLab-v8)<br>
  *Platform virtualisasi dan emulasi jaringan enterprise berbasis Ubuntu 26.04 LTS dengan panduan deployment Proxmox VE 8+ & VMware.*<br>
  `Ubuntu` `Proxmox` `Virtualization` `Network-Emulation` `PNETLab` `KVM`
- 📦 **[NotepadNext-MacOS](https://github.com/alsyundawy/NotepadNext-MacOS)** [![Stars](https://img.shields.io/github/stars/alsyundawy/NotepadNext-MacOS?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/NotepadNext-MacOS)<br>
  *Reimplementasi editor Notepad++ modern berbasis Qt untuk sistem operasi macOS.*<br>
  `C++` `macOS` `NotepadNext` `Editor` `Qt6`
- 📦 **[openssl-1.0.2](https://github.com/alsyundawy/openssl-1.0.2)** [![Stars](https://img.shields.io/github/stars/alsyundawy/openssl-1.0.2?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/openssl-1.0.2)<br>
  *Fork keamanan produksi dengan mitigasi CVE yang di-backport untuk sistem OpenSSL 1.0.2 warisan.*<br>
  `C` `OpenSSL` `Security` `Hardening` `CVE-Mitigation` `Backport`
- 📦 **[Disable-MacOS-Updates](https://github.com/alsyundawy/Disable-MacOS-Updates)** [![Stars](https://img.shields.io/github/stars/alsyundawy/Disable-MacOS-Updates?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/Disable-MacOS-Updates)<br>
  *Skrip Bash reversibel untuk menonaktifkan pembaruan perangkat lunak otomatis pada macOS (Monterey hingga Golden Gate).*<br>
  `macOS` `Bash` `Apple-Silicon` `DAW` `Sysadmin`
- 📦 **[mikrotik-blacklist](https://github.com/alsyundawy/mikrotik-blacklist)** [![Stars](https://img.shields.io/github/stars/alsyundawy/mikrotik-blacklist?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/mikrotik-blacklist)<br>
  *Skrip RouterOS untuk pembaruan daftar hitam ancaman keamanan secara otomatis.*<br>
  `RouterOS` `Blacklist` `Security`

---

#### 🛠️ Prioritas 2: Fork yang Dimodifikasi & Dikontribusikan (Active Contributed Forks)

*Repositori hulu open-source di mana Harry DS Alsyundawy berkontribusi secara nyata melalui komit langsung, penambalan keamanan, dan kustomisasi enterprise.*

- 📦 **[PowerDNS-Admin](https://github.com/alsyundawy/PowerDNS-Admin)** [![Stars](https://img.shields.io/github/stars/alsyundawy/PowerDNS-Admin?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/PowerDNS-Admin) `[136 Komit]`<br>
  *Web control panel untuk PowerDNS Authoritative Server dengan optimasi koneksi MariaDB, integrasi LDAP, dan peningkatan GUI.*<br>
  `Python` `PowerDNS` `DNS` `Web-GUI` `Enterprise`
- 📦 **[shc](https://github.com/alsyundawy/shc)** [![Stars](https://img.shields.io/github/stars/alsyundawy/shc?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/shc) `[54 Komit]`<br>
  *Kompiler Shell Script Generik dengan Peningkatan Keamanan & Audit. Mengenkripsi skrip shell menjadi biner executable stripped.*<br>
  `C` `Shell` `Security` `Auditing` `Hardening`
- 📦 **[visualsubnetcalc](https://github.com/alsyundawy/visualsubnetcalc)** [![Stars](https://img.shields.io/github/stars/alsyundawy/visualsubnetcalc?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/visualsubnetcalc) `[49 Komit]`<br>
  *Kalkulator Subnet Visual — Edisi Modern & Diperkeras. Perencana subnet IPv4 & IPv6 CIDR visual dengan pembagian bit real-time dan bebas penyimpanan sisi server.*<br>
  `TypeScript` `Networking` `Subnetting` `IPv4` `CIDR`
- 📦 **[zmbackup](https://github.com/alsyundawy/zmbackup)** [![Stars](https://img.shields.io/github/stars/alsyundawy/zmbackup?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/zmbackup) `[47 Komit]`<br>
  *Solusi hot backup multi-threaded, pemulihan instan, dan migrasi lintas OS untuk Zimbra Collaboration Suite & Carbonio.*<br>
  `Shell` `Zimbra` `Backup` `Disaster-Recovery` `Migration`
- 📦 **[pear-desktop-mac](https://github.com/alsyundawy/pear-desktop-mac)** [![Stars](https://img.shields.io/github/stars/alsyundawy/pear-desktop-mac?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/pear-desktop-mac) `[44 Komit]`<br>
  *Klien desktop macOS berkinerja tinggi untuk YouTube Music dengan pemblokir iklan bawaan (27+ vendor filter), SponsorBlock, dan lirik tersinkronisasi.*<br>
  `macOS` `Apple-Silicon` `YouTube-Music` `Electron` `TypeScript`
- 📦 **[SmartDNS](https://github.com/alsyundawy/SmartDNS)** [![Stars](https://img.shields.io/github/stars/alsyundawy/SmartDNS?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/SmartDNS) `[43 Komit]`<br>
  *Platform resolver DNS otomatis untuk jaringan ISP dan enterprise dengan perutean multi-upstream pintar.*<br>
  `HTML` `JavaScript` `DNS` `Resolver` `Routing`
- 📦 **[SubnetCalc-MacOS](https://github.com/alsyundawy/SubnetCalc-MacOS)** [![Stars](https://img.shields.io/github/stars/alsyundawy/SubnetCalc-MacOS?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/SubnetCalc-MacOS) `[32 Komit]`<br>
  *Kalkulator subnet IPv4 & IPv6 native Swift & Cocoa AppKit berkinerja tinggi untuk macOS (Universal 2: M1-M4 & Intel) dengan 25 tema pengembang.*<br>
  `Swift` `macOS` `Apple-Silicon` `AppKit` `Cocoa` `Subnetting` `IPAM`
- 📦 **[ufw-ipset-blocklist-autoupdate](https://github.com/alsyundawy/ufw-ipset-blocklist-autoupdate)** [![Stars](https://img.shields.io/github/stars/alsyundawy/ufw-ipset-blocklist-autoupdate?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/ufw-ipset-blocklist-autoupdate) `[27 Komit]`<br>
  *Pembaruan otomatis daftar blokir IP berbahaya pada firewall Linux menggunakan ipset dan ufw secara berkala.*<br>
  `Shell` `UFW` `Ipset` `Security` `Firewall`
- 📦 **[OpenVPN-Install](https://github.com/alsyundawy/OpenVPN-Install)** [![Stars](https://img.shields.io/github/stars/alsyundawy/OpenVPN-Install?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/OpenVPN-Install) `[24 Komit]`<br>
  *Installer OpenVPN road warrior untuk Debian, Ubuntu, dan CentOS dengan dukungan dual-stack IPv4/IPv6 dan DNS Unbound.*<br>
  `Shell` `OpenVPN` `VPN` `Security` `Networking`
- 📦 **[cyberpanel](https://github.com/alsyundawy/cyberpanel)** [![Stars](https://img.shields.io/github/stars/alsyundawy/cyberpanel?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/cyberpanel) `[21 Komit]`<br>
  *Panel kontrol web hosting untuk OpenLiteSpeed dengan penyesuaian keamanan lingkungan produksi.*<br>
  `JavaScript` `Python` `Hosting` `LiteSpeed` `Control-Panel`
- 📦 **[esxi-unlocker-v4](https://github.com/alsyundawy/esxi-unlocker-v4)** [![Stars](https://img.shields.io/github/stars/alsyundawy/esxi-unlocker-v4?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/esxi-unlocker-v4) `[11 Komit]`<br>
  *macOS Unlocker V4 untuk VMware ESXi. Memungkinkan dukungan guest OS macOS pada hypervisor server VMware ESXi.*<br>
  `Python` `VMware` `ESXi` `macOS` `Hypervisor`
- 📦 **[Zimbra2Zimbra-Migration-Tool](https://github.com/alsyundawy/Zimbra2Zimbra-Migration-Tool)** [![Stars](https://img.shields.io/github/stars/alsyundawy/Zimbra2Zimbra-Migration-Tool?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/Zimbra2Zimbra-Migration-Tool) `[11 Komit]`<br>
  *Mesin migrasi Zimbra-ke-Zimbra (Z2Z) enterprise lintas versi tanpa kehilangan data atau kendala timeout.*<br>
  `Shell` `Zimbra` `Migration` `Backup` `Mail-Server`
- 📦 **[Windows10Debloater](https://github.com/alsyundawy/Windows10Debloater)** [![Stars](https://img.shields.io/github/stars/alsyundawy/Windows10Debloater?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/Windows10Debloater) `[6 Komit]`<br>
  *Skrip PowerShell untuk membersihkan bloatware, mematikan telemetri, dan menghentikan proses latar belakang pada Windows 10/11.*<br>
  `PowerShell` `Windows` `Debloat` `System-Tuning`
- 📦 **[OpenSID](https://github.com/alsyundawy/OpenSID)** [![Stars](https://img.shields.io/github/stars/alsyundawy/OpenSID?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/OpenSID) `[5 Komit]`<br>
  *Sistem Informasi Desa (SID) open-source dengan penyesuaian kompatibilitas server PHP 8+ dan pengerasan web.*<br>
  `PHP` `OpenSID` `Government` `Indonesia`
- 📦 **[Linux-System-Management-Scripts-Tricks](https://github.com/alsyundawy/Linux-System-Management-Scripts-Tricks)** [![Stars](https://img.shields.io/github/stars/alsyundawy/Linux-System-Management-Scripts-Tricks?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/Linux-System-Management-Scripts-Tricks) `[4 Komit]`<br>
  *Kumpulan skrip otomatisasi sysadmin Linux, trik monitoring, dan panduan sertifikasi infrastruktur.*<br>
  `Shell` `Linux` `Sysadmin` `DevOps`
- 📦 **[wireguard-install](https://github.com/alsyundawy/wireguard-install)** [![Stars](https://img.shields.io/github/stars/alsyundawy/wireguard-install?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/wireguard-install) `[2 Komit]`<br>
  *Skrip otomatisasi instalasi WireGuard road warrior dengan generator profil QR-Code otomatis.*<br>
  `Shell` `WireGuard` `VPN` `Security`
- 📦 **[AutoInstallGenieACS](https://github.com/alsyundawy/AutoInstallGenieACS)** [![Stars](https://img.shields.io/github/stars/alsyundawy/AutoInstallGenieACS?style=flat-square&color=fee101&logo=github)](https://github.com/alsyundawy/AutoInstallGenieACS) `[1 Komit]`<br>
  *Skrip instalasi dan konfigurasi otomatis server GenieACS TR-069 pada distro Debian & Ubuntu.*<br>
  `Shell` `GenieACS` `TR-069` `ISP`
- 📦 **[dnsdist-one-click](https://github.com/alsyundawy/dnsdist-one-click)** [![Stars](https://img.shields.io/github/stars/alsyundawy/dnsdist-one-click) `[1 Komit]`<br>
  *Installer cepat DNSDist load balancer berkecepatan tinggi dengan integrasi aturan TrustPositif Komdigi.*<br>
  `Shell` `DNSDist` `DNS` `TrustPositif` `Load-Balancer`
- 📦 **[SlimBrave-Neo](https://github.com/alsyundawy/SlimBrave-Neo)** [![Stars](https://img.shields.io/github/stars/alsyundawy/SlimBrave-Neo)](https://github.com/alsyundawy/SlimBrave-Neo) `[1 Komit]`<br>
  *Debloat dan pengerasan peramban Brave pada Linux dan macOS untuk privasi dan efisiensi memori.*<br>
  `Python` `Brave` `Privacy` `Debloat`

---

#### 📚 Prioritas 3: Koleksi Cermin & Fork Referensi Terpilih (Non-Arsip)

*Koleksi repositori hulu, perkakas keamanan jaringan, dan referensi sistem yang dirawat aktif. Seluruh repositori berstatus arsip telah dieksklusikan.*

<details>
<summary><b>📂 Buka Katalog Lengkap 99+ Fork & Cermin Referensi Aktif Terpilih</b> (Klik untuk melihat tabel)</summary>

""" + id_table_str + """

</details>"""
    return md

def update_readme_files():
    en_table, id_table, s_len, c_len, o_len = build_tables()
    en_section = build_portfolio_markdown_en(en_table)
    id_section = build_portfolio_markdown_id(id_table)

    with open('README.md') as f:
        readme_en = f.read()
    with open('README-ID.md') as f:
        readme_id = f.read()

    # Disable MD013 at top
    readme_en = re.sub(r'<!-- markdownlint-disable [^\n]+ -->', '<!-- markdownlint-disable MD033 MD041 MD013 -->', readme_en)
    readme_id = re.sub(r'<!-- markdownlint-disable [^\n]+ -->', '<!-- markdownlint-disable MD033 MD041 MD013 -->', readme_id)

    # Replace portfolio sections
    pattern_en = r"### 🚀 (?:Highlighted Repositories|Curated Repository Portfolio).*?(?=### 🏢 Industry Partners & Client Ecosystem)"
    new_readme_en = re.sub(pattern_en, en_section + "\n\n---\n\n", readme_en, flags=re.DOTALL)

    pattern_id = r"### 🚀 (?:Highlighted Repositories|Portofolio Repositori Terkurasi).*?(?=### 🏢 Klien & Mitra Industri)"
    new_readme_id = re.sub(pattern_id, id_section + "\n\n---\n\n", readme_id, flags=re.DOTALL)

    with open('README.md', 'w') as f:
        f.write(new_readme_en)
    with open('README-ID.md', 'w') as f:
        f.write(new_readme_id)

    print("Both README.md and README-ID.md re-updated and normalized successfully!")

if __name__ == '__main__':
    update_readme_files()
