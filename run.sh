#!/bin/zsh

echo
source venv/bin/activate

python3 -m http.server 8080 --directory frontend & HTML_SERVER_PID=$!
echo "HTML SERVER: \033[32mON!\033[0m"

chmod -R 755 frontend

flask run -p 5433 > /dev/null 2>&1 & FLASK_SERVER_PID=$!
echo "FLASK SERVER: \033[32mON!\033[0m"

echo "\033[31m\nPress ENTER to kill the servers\033[0m"
echo "\033[33m\nRunning...\033[0m"
read

kill $HTML_SERVER_PID
echo "HTML server: \033[31mOFF\033[0m"


kill $FLASK_SERVER_PID
echo "Flask server: \033[31mOFF\033[0m"
echo
