# Version liberación - Release ddmmyyyy
APP_VERSION = '1.6.0'
# Flask Settings
FLASK_SECRET_KEY = '0pt1m1$42560-$3cr3t4'
FLASK_SERVER_NAME = 'localhost' # '0.0.0.0'  # '20.206.88.85'
FLASK_SERVER_PORT = 9090  # 5000
FLASK_DEBUG = True
FLASK_THREADED = True
FLASK_ERROR_404_HELP = False
FLASK_APP_FOLDER = 'optidata-core'
FLASK_NAME_UPLOAD_FOLDER = 'files'
FLASK_NAME_EXPORT_FOLDER = 'exported-files'
FLASK_ALLOWED_EXTENSIONS = {'txt', 'csv', 'xls', 'xlsx'}
FLASK_MAX_CONTENT_LENGTH = 500 * 1024 * 1024
FLASK_NUMBER_PROCESSES = 2
FLASK_ROOT_PATH = ''
FLASK_UPLOAD_FOLDER = ''
FLASK_EXPORT_FOLDER = ''

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False
RESTPLUS_API_VERSION = '/v1'
RESTPLUS_EMPTY_RESULT = 'No existen registros asociados'

# Oracle Properties (SAP)
ORACLE_HOST = 'localhost'
ORACLE_PORT = '1521'
ORACLE_USERNAME = 'sys as sysadmin'
ORACLE_PASSWORD = 'Opt1m1$42560'
ORACLE_DB_NAME = 'orcl'
ORACLE_SERVICE_NAME = ''
ORACLE_DNS = f'{ORACLE_HOST}/{ORACLE_DB_NAME}'
ORACLE_ENCODING = 'UTF-8'

# MongoDB Configuration
MONGO_BATCH_SIZE = 100000
MONGO_DB_HOST = 'localhost'  # 'cxp-db'  # '20.206.88.85'  #'cxpnew2.brazilsouth.cloudapp.azure.com'  # 'cxp-db'
MONGO_DB_PORT = 27017
MONGO_DB_NAME = 'cxp_db'
MONGO_DB_URI = f'mongodb://{MONGO_DB_HOST}:{MONGO_DB_PORT}/{MONGO_DB_NAME}'
MONGO_DB_USER = ''
MONGO_DB_PWD = ''
MONGO_COLLECTIONS = {
    'reconciled',
    'total_reconciled',
    'unreconciled',
    'total_unreconciled',
    'duplicates',
    'total_duplicates',
    'config_rules',
    'config_rules_columns',
    'config_rules_columns_index',
    'config_rules_column_amount',
    'config_rules_column_date',
    'config_rules_columns_mapping',
    'upload_files',
    'config_process',
    'config_process_files',
    'users',
    'roles',
    'partners',
    'type_cycles',
    'cycles',
    'sersal',
    'sersal_detail',
    'cartola',
    'cartola_detail',
    'program_scheduler'
}

# MongoDB Documents
MONGO_COLLECTION_UPLOAD_FILE_USER_ID = 'user_id'
MONGO_COLLECTION_UPLOAD_FILE_PARTNER_ID = 'partner_id'
MONGO_COLLECTION_UPLOAD_FILE_CLIENT_ID = 'partner_id'
MONGO_COLLECTION_UPLOAD_FILE = 'upload_files'
MONGO_COLLECTION_CONFIG_RULES = 'config_rules'
MONGO_COLLECTION_CONFIG_RULES_DEFINED_COLUMNS = 'config_rules_columns'
MONGO_COLLECTION_CONFIG_RULES_DEFINED_INDEX_COLUMNS = 'config_rules_columns_index'
MONGO_COLLECTION_CONFIG_RULES_DEFINED_AMOUNT_COLUMN = 'config_rules_column_amount'
MONGO_COLLECTION_CONFIG_RULES_DEFINED_DATE_COLUMN = 'config_rules_column_date'
MONGO_COLLECTION_CONFIG_RULES_DEFINED_MAPPING_COLUMNS = 'config_rules_columns_mapping'
MONGO_COLLECTION_PROC_RECONCILED_CNF = 'config_process'
MONGO_COLLECTION_PROC_RECONCILED_FILE = 'config_process_files'
MONGO_COLLECTION_DATA_RECONCILED = 'reconciled'
MONGO_COLLECTION_DATA_TOTAL_RECONCILED = 'total_reconciled'
MONGO_COLLECTION_DATA_DUPLICATES = 'duplicates'
MONGO_COLLECTION_DATA_TOTAL_DUPLICATES = 'total_duplicates'
MONGO_COLLECTION_DATA_UNRECONCILED = 'unreconciled'
MONGO_COLLECTION_DATA_TOTAL_UNRECONCILED = 'total_unreconciled'
MONGO_COLLECTION_DATA_USERS = 'users'
MONGO_COLLECTION_DATA_ROLES = 'roles'
MONGO_COLLECTION_DATA_PARTNERS = 'partners'
MONGO_COLLECTION_DATA_TYPE_CYCLES = 'type_cycles'
MONGO_COLLECTION_DATA_CYCLES = 'cycles'
MONGO_COLLECTION_DATA_SERSAL_CAB = 'sersal'
MONGO_COLLECTION_DATA_SERSAL_DET = 'sersal_detail'
MONGO_COLLECTION_DATA_CARTOLA_CAB = 'cartola'
MONGO_COLLECTION_DATA_CARTOLA_DET = 'cartola_detail'
MONGO_COLLECTION_DATA_PROG_SCHEDULERS = 'program_scheduler'

# BCrypt Config
BCRYPT_LOG_ROUNDS = 13

# JWT Configuration
TOKEN_EXPIRE_HOURS = 1
TOKEN_EXPIRE_MINUTES = 15
TOKEN_REFRESH_EXPIRE_HOURS = 1
TOKEN_HEADER_NAME = 'X-Access-Token'
TOKEN_FORMAT = 'Bearer '

# Files Configuration
FILE_EXT_TXT = 'txt'
FILE_EXT_CSV = 'csv'
FILE_EXT_XLS = 'xls'
FILE_EXT_XLSX = 'xlsx'
CSV_SEPARATOR = ';'

# Vaex Configuration
VAEX_THREAD_COUNT = 10
VAEX_MAX_COLUMN = 10000

# Default Configurations - User/Role
DEFAULT_USERNAME = 'admin@optimisa.cl'
DEFAULT_PASSWORD = 123456
DEFAULT_FIRSTNAME = 'Administrador'
DEFAULT_LASTNAME = 'del Sistema'

DEFAULT_USER_USERNAME = 'consulta@optimisa.cl'
DEFAULT_USER_PASSWORD = 123456
DEFAULT_USER_FIRSTNAME = 'Usuario Consulta'
DEFAULT_USER_LASTNAME = 'del Sistema'
DEFAULT_ROLE_NAME_ADMIN = 'Administrador'
DEFAULT_ROLE_NAME_USER = 'Consulta'

# Kafka Properties
KAFKA_BOOSTRAP = 'localhost'
KAFKA_PORT = 19092
KAFKA_SASL_MECHANISM = 'PLAIN'
KAFKA_SECURITY_PROTOCOL = 'SASL_SSL'
KAFKA_USERNAME = ''
KAFKA_PASSWORD = ''
KAFKA_OFFSET = 'earliest'
KAFKA_TIMEOUT = 1000
KAFKA_ENCODE = 'UTF-8'

# Kafka Topics
KAFKA_TOPIC_SCHEDULER = ''
KAFKA_TOPIC_PETITION = ''

# SFTP Properties
SFTP_HOSTNAME = 'localhost'
SFTP_USERNAME = 'optimisa'
SFTP_PASSWORD = '0pt1m1$42560'
SFTP_PORT = 2323
SFTP_PATH_DEFAULT = 'sftp'

SFTP_PATH_CARTOLAS = 'cartolas'
SFTP_PATH_LOTES = 'lotes_pago'
SFTP_PATH_SERSAL = 'sersal'

SFTP_SERSAL_FILE_FORMAT = 'SERSALRYYYYMMDD'

# Scheduler Properties
SCHEDULER_MIN_TIME_RUN = 1
SCHEDULER_MIN_TIME_RUN_LOTES = 1
SCHEDULER_MIN_TIME_RUN_CARTOLA = 1
SCHEDULER_MIN_TIME_RUN_PA = 1
