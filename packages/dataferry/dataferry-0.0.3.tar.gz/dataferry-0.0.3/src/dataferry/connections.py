from dataferry.functions import write_to_log

# ===================================================================================================
# CREATE CONNECTIONS
# ===================================================================================================

# class sql_server_connection:
class SqlServerConnection:
    def __init__(self, my_server, config_path, **kwargs):
        self.my_server = my_server
        self.engine = None
        self.connection = None
        self.cursor = None
        self.platform = None
        
        # unpack **kwargs
        self.db = None
        self.log_path = None
        for key, value in kwargs.items():
            if key == 'db':
                self.db = value
            if key == 'log_path':
                self.log_path = value
        
        # import modules
        import configparser
        import sqlalchemy

        # define config
        config = configparser.ConfigParser()		
        config.read(config_path)
        sql_server = config[self.my_server]
        
        # get variables
        servername = sql_server["server"]
        authentication = sql_server['authentication']
        if self.db != None:
            dbname = self.db
        else:
            dbname = sql_server["database"]
        
        # determine authentication and set variables as appropriate
        if authentication == 'windows':
            connection_string = 'mssql+pyodbc://@' + servername + '/' + dbname + '?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server'
        else:
            uid = sql_server["uid"]
            pwd = sql_server["pwd"]
            connection_string = 'mssql+pyodbc://' + uid + ':' + pwd + '@' + servername + '/' + dbname + '?driver=ODBC+Driver+17+for+SQL+Server'
        
        # create connection
        self.engine = sqlalchemy.create_engine(connection_string, fast_executemany=True)
        self.connection = self.engine.connect().connection
        self.cursor = self.connection.cursor()  
        self.platform = 'sql_sever'
        
        # create update message
        my_msg = 'SQL Server connection class created | Server: ' + self.my_server
        if self.db != None:
            my_msg = my_msg + ' | Default database: ' + self.db
        
        # update the log file if applicable
        if self.log_path != None:
            write_to_log(self.log_path,  my_msg)

class DbxConnection:
    def __init__(self, my_dbx, config_path, **kwargs):
        self.my_dbx = my_dbx
        self.engine = None
        self.connection = None
        self.cursor = None
        self.platform = None

        # unpack **kwargs
        self.log_path = None
        for key, value in kwargs.items():
            if key == 'log_path':
                self.log_path = value
        
        # import modules
        import configparser
        
        # import objects
        from databricks import sql
        
        # define config
        config = configparser.ConfigParser()
        config.read(config_path)
        dbx = config[self.my_dbx]
        
        # get variables
        hostname = dbx["hostname"]
        http_path = dbx["http_path"]
        token = dbx["token"]
        platform = dbx["platform"]
        
        # create connection
        self.connection = sql.connect(server_hostname = hostname, http_path = http_path, access_token = token, fast_executemany=True)
        self.cursor = self.connection.cursor()
        self.platform = platform
        
        my_msg = 'Databricks connection class created'       
        if self.log_path != None:
            write_to_log(self.log_path,  my_msg)

class HiveConnection:
    def __init__(self, my_hive, config_path, **kwargs):
        self.my_hive = my_hive
        self.connection = None
        self.cursor = None
        self.platform = None

        # unpack **kwargs
        self.log_path = None
        for key, value in kwargs.items():
            if key == 'log_path':
                self.log_path = value
        
        # import modules
        import configparser
        import jaydebeapi
        
        # define config
        config = configparser.ConfigParser()
        config.read(config_path)
        hive = config[my_hive]
        
        # get variables
        user = hive['user']
        password = hive['password']
        driver = hive['driver']
        temp_url = hive["url"]
        driver_path = hive['driver_path']
        
        # set dynamic variables
        url = (temp_url)
        creds = [user, password]
        
        # make the connection
        self.connection = jaydebeapi.connect(driver, url, creds, driver_path)
        self.cursor = self.connection.cursor()
        self.platform = 'hive'
        
        # give the log file an update
        if self.log_path != None:
            write_to_log(self.log_path,  'Hive connection class created')

# ===================================================================================================
# ===================================================================================================
# ===================================================================================================