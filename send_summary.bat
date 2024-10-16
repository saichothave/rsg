@echo off
cd /d E:\Roopsangam-Dresses\rsg
call rsenv\Scripts\activate
python .\roopsangamnx_backend\manage.py send_summary
