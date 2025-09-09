#!/usr/bin/env python3
"""
ftp_client.py
- Connects to FTP server, lists directory, downloads available file, verifies content.
"""
from ftplib import FTP, error_perm
import logging

LOGFILE = "ftp_client.log"
logging.basicConfig(filename=LOGFILE, level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s", filemode="w")

def ftp_demo(host, port=21, username='anonymous', password='anonymous@', filename="readme.txt"):
    ftp = FTP()
    try:
        ftp.connect(host, port, timeout=60)
        ftp.login(username, password)
        ftp.set_pasv(True)  # Enable passive mode
        logging.info("Connected and logged in to FTP: %s", host)
        print("Connected to FTP server:", host)

        # List files in the root directory
        print("\nDirectory listing:")
        ftp.retrlines("LIST")

        # Try downloading the given file
        downloaded = []
        try:
            ftp.retrbinary(f"RETR {filename}", lambda b: downloaded.append(b))
            downloaded_bytes = b"".join(downloaded)
            print("\nDownloaded size:", len(downloaded_bytes))
            print("Downloaded content (first 500 chars):")
            print(downloaded_bytes.decode('utf-8', errors='replace')[:500])
            logging.info("Downloaded %s (size %d)", filename, len(downloaded_bytes))
        except Exception as e:
            logging.warning("Could not download file: %s", e)
            print("Download failed:", e)
    except Exception as ex:
        logging.exception("FTP error: %s", ex)
        print("FTP error:", ex)
    finally:
        try:
            if ftp.sock:
                ftp.quit()
        except:
            pass

if __name__ == "__main__":
    ftp_host = "ftp.byethost11.com"
    ftp_demo(ftp_host, username="b11_39899405", password="s3101@2005", filename="readme.txt")