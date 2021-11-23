echo "Preparing environment"
echo "------------"

echo "Checking if log file exists"
if test -f "logfile.log"; then
	echo "exists"
else 
	echo "Logfile not found, creating one."
	touch logfile.log
fi
echo "-----------------"

echo "Creating database"
sudo mysql -u root -e "CREATE DATABASE IF NOT EXISTS memorygame"; 
if [ $? -eq 0 ]; then echo "OK"; else echo "Problem creating database"; exit 1; fi

echo "Getting python3 executable loc"
python_exec_loc=$(which python3)
if [ $? -eq 0 ]; then echo "OK"; else echo "Problem getting python3 exec location"; exit 1; fi
echo "$python_exec_loc"
echo "------------------------------------------------"

echo "Running database migrations"
$python_exec_loc db_migrate.py
if [ $? -eq 0 ]; then echo "OK" else echo "Database migration failed."; exit 1; fi
echo "------------------"

echo "Running tests"
$python_exec_loc testing.py
if [ $? -eq 0 ]; then echo "OK"; else echo "Testing failed."; exit 1; fi
echo "-----------------"

echo "Setup finished"
echo "To start game, execute:"
echo "$python_exec_loc MemoryGame.py"
