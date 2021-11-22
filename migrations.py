import mysql.connector, logging, logging.config, configparser, yaml, os, time, datetime
from datetime import datetime

config = configparser.ConfigParser()

with open('./logconfig.yaml', 'r') as stream:
    logConfig = yaml.safe_load(stream)

logging.config.dictConfig(logConfig)

logger = logging.getLogger('root')

logger.info('Loading database configurations from file')
try:
    config.read('config.ini')
    DbConfig_db_host  = config.get('DbConfig', 'db_host')
    DbConfig_db = config.get('DbConfig', 'db')
    DbConfig_db_user = config.get('DbConfig', 'db_user')
    DbConfig_db_pass = config.get('DbConfig', 'db_pass')
except:
    logger.error('Configuration loading failed')
logger.info('Done')

connection = None
connected = False

def init_db():
    global connection
    connection = mysql.connector.connect(host=DbConfig_db_host, database=DbConfig_db, user=DbConfig_db_user, password=DbConfig_db_pass)

logger.info('Connecting to database')
init_db()

def get_cursor():
	global connection
	try:
		connection.ping(reconnect=True, attempts=1, delay=0)
		connection.commit()
	except mysql.connector.Error as err:
		logger.error("No connection to db " + str(err))
		connection = init_db()
		connection.commit()
	return connection.cursor()

try:
    cursor = get_cursor()
    cursor = connection.cursor()
    logger.info("Creating migrations table if it does not exist")
    cursor.execute("CREATE TABLE IF NOT EXISTS migrations ( id INT NOT NULL AUTO_INCREMENT, name VARCHAR(255), exec_ts varchar(50), exec_dt varchar(50), PRIMARY KEY (id))")
    connection.commit()
except:
    logger.error('Problem creating migrations table')

migrationsList = []
curDir = os.getcwd()
migrationsFilesList = os.listdir(curDir + "/Migrations/")
for fileName in migrationsFilesList:
    if(fileName.endswith('.sql')):
        migrationsList.append(fileName)

migrationsList.sort(reverse=False)

for migration in migrationsList:
    with open(curDir + "/Migrations/" + migration,'r') as file:
        migrationSql = file.read()
        logger.debug(migrationSql)
        logger.info("Executing migration: " + str(migration))
        try:
            cursor.execute(migrationSql)
            connection.commit()
            migExecTs = datetime.today().strftime('%H:%M:%S')
            migExecDt = datetime.today().strftime('%Y-%m-%d')
            cursor.execute("INSERT INTO migrations (name, exec_ts, exec_dt) VALUES (\'" + migration + "\', \'" + str(migExecTs) + "\', \'" + str(migExecDt) + "\' )")
            connection.commit()
        except:
            logger.error("Error executing migration")
        