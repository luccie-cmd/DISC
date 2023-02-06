@echo off
cls
git add .
git commit -m "added push.bat for myself"
git remote add origin https://github.com/luccie-cmd/disc.git
git branch -M main
git push -u origin main
pause
exit