CN Lab Assignment 2 - Application Layer Protocols (HTTP, SMTP, FTP, DNS)

Files:
- http_client.py
- smtp_client.py
- ftp_client.py
- dns_lookup.py
- README.md
- demo_outputs/ (logs/screenshots if provided by you)

How to run:
1. Install dependencies:
   pip install requests dnspython

2. HTTP demo:
   python3 http_client.py

3. DNS demo:
   python3 dns_lookup.py

4. FTP demo (replace host if necessary):
   python3 ftp_client.py

5. SMTP demo:
   - Edit smtp_client.py to add real/test SMTP credentials.
   - Use Ethereal (ethereal.email) for a test SMTP account, or use your SMTP with app-password.
   - Then uncomment the send_email(...) invocation.

Security note:
- Do NOT commit real passwords to the public repo. Use environment variables or a secret manager if you need to automate sending.

What I changed from the uploaded LAB2.zip:
- Rewrote/cleaned the scripts to be consistent, added logging, and left placeholders for credentials.
- Prepared consistent log filenames: http_client.log, smtp_client.log, ftp_client.log, dns_lookup.log.
