from dataferry.functions import write_to_log

# ===================================================================================================
# EXPORT SQL STATEMENT/TABLE FROM DATABASE TO LOCAL TEXT FILE
# ===================================================================================================

class ExportSqlStatementAsTextFile:
    
    def __init__(self, my_connection, my_sql, my_file, my_separator, log_path):
        self.my_connection = my_connection
        self.my_sql = my_sql
        self.my_file = my_file
        self.my_separator = my_separator
        self.log_path = log_path
        self.fill_nas = []
    
    def add_fill_na(self, my_list, my_na, my_type):
        self.fill_nas.append((my_list, my_na, my_type))
         
    def export_data(self):  
        
        import pandas as pd
        import os
        
        # delete file if it already exists
        if os.path.exists(self.my_file):
            os.remove(self.my_file)
        
        if self.log_path != None and len(self.log_path) > 0:
            write_to_log(self.log_path, 'transfer to ' + self.my_table + ': started')
        
        i = 1
        for my_chunk in pd.read_sql(self.my_sql, self.my_connection.connection, chunksize=10**4):    
            # fill nas and set types
            for fn in self.fill_nas:
                my_chunk[fn[0]] = my_chunk[fn[0]].fillna(fn[1])
                my_chunk[fn[0]] = my_chunk[fn[0]].astype(fn[2])
            # append the first chunk with headers
            if i==1:
                my_chunk.to_csv(self.my_file, sep=self.my_separator, index=False, mode='w', header=True)
            # append the other chunks without headers
            else:
                my_chunk.to_csv(self.my_file, sep=self.my_separator, index=False, mode='a', header=False)
            if self.log_path != None and len(self.log_path) > 0:
                write_to_log(self.log_path, 'transfer to ' + self.my_table + ': chunk ' + str(i) + ' finished')
            i = i + 1
            
        if self.log_path != None and len(self.log_path) > 0:
            write_to_log(self.log_path, 'transfer to ' + self.my_table + ': finished')

class ExportSqlServerTableAsTextFile:
    
    def __init__(self, my_connection, my_database, my_table, my_file, my_separator, log_path):
        self.my_connection = my_connection
        self.my_database = my_database
        self.my_table = my_table
        self.log_path = log_path 
        self.my_file = my_file
        self.my_separator = my_separator
        self.fill_nas = []
    
    def add_fill_na(self, my_list, my_na, my_type):
        self.fill_nas.append((my_list, my_na, my_type))
         
    def export_data(self):  
        
        import pandas as pd
        import os
        
        # delete file if it already exists
        if os.path.exists(self.my_file):
            os.remove(self.my_file)
        
        if self.log_path != None and len(self.log_path) > 0:
            write_to_log(self.log_path, 'transfer to ' + self.my_table + ': started')
        
        i = 1
        my_sql = 'SELECT * FROM ' + self.my_database + '.dbo.' + self.my_table
        for my_chunk in pd.read_sql(my_sql, self.my_connection.connection, chunksize=10**4):    
            # fill nas and set types
            for fn in self.fill_nas:
                my_chunk[fn[0]] = my_chunk[fn[0]].fillna(fn[1])
                my_chunk[fn[0]] = my_chunk[fn[0]].astype(fn[2])
            # append the first chunk with headers
            if i==1:
                my_chunk.to_csv(self.my_file, sep=self.my_separator, index=False, mode='w', header=True)
            # append the other chunks without headers
            else:
                my_chunk.to_csv(self.my_file, sep=self.my_separator, index=False, mode='a', header=False)
            if self.log_path != None and len(self.log_path) > 0:
                write_to_log(self.log_path, 'transfer to ' + self.my_table + ': chunk ' + str(i) + ' finished')
            i = i + 1
            
        if self.log_path != None and len(self.log_path) > 0:
            write_to_log(self.log_path, 'transfer to ' + self.my_table + ': finished')

def export_sql_statement_as_text_file(my_connection, my_sql, my_file, my_separator, log_path):
    
# FUNCTION EQUIVALENT TO THE CLASS ExportSqlStatementAsTextFile
             
    import pandas as pd
    import os
    
    # delete file if it already exists
    if os.path.exists(my_file):
        os.remove(my_file)
    
    if log_path != None and len(log_path) > 0:
        write_to_log(log_path, 'transfer to ' + my_file + ': started')
    
    i = 1
    for my_chunk in pd.read_sql(my_sql, my_connection.connection, chunksize=10**4):    
        # append the first chunk with headers
        if i==1:
            my_chunk.to_csv(my_file, sep=my_separator, index=False, mode='w', header=True)
        # append the other chunks without headers
        else:
            my_chunk.to_csv(my_file, sep=my_separator, index=False, mode='a', header=False)
        if log_path != None and len(log_path) > 0:
            write_to_log(log_path, 'transfer to ' + my_file + ': chunk ' + str(i) + ' finished')
        i = i + 1
        
    if log_path != None and len(log_path) > 0:
        write_to_log(log_path, 'transfer to ' + my_file + ': finished')

# ===================================================================================================
# ===================================================================================================
# ===================================================================================================

# ===================================================================================================
# IMPORT LOCAL TEXT FILE TO DATABASE
# ===================================================================================================

class LoadTextFileToSqlServer:
    
    def __init__(self, my_file, my_separator, my_connection, my_database, my_table, log_path):
        self.my_file = my_file
        self.my_separator = my_separator
        self.my_connection = my_connection
        self.my_database = my_database
        self.my_table = my_table
        self.log_path = log_path
        self.my_read_dtype = None
        self.my_converters = None
        self.my_dtypes = None    
 
    def add_read_dtype(self, my_read_dtype):
        self.my_converters = None
        self.my_read_dtype = my_read_dtype
   
    def add_read_converters(self, my_converters):
        self.my_read_dtype = None
        self.my_converters = my_converters

    def add_to_dtypes(self, my_dtypes):
        self.my_dtypes = my_dtypes

    def run_sql_code(self, my_connection, my_sql):
        my_connection.cursor.execute(my_sql)
        my_connection.connection.commit()    

    def truncate_table(self):
        write_to_log(self.log_path, "truncation of " + self.my_table + ": started")
        self.run_sql_code(self.my_connection, "USE " + self.my_database)
        self.run_sql_code(self.my_connection, "IF EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[" + self.my_table + "]') AND type in (N'U')) TRUNCATE TABLE [dbo].[" + self.my_table + "]")
        self.run_sql_code(self.my_connection, "IF EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[" + self.my_database + "].[dbo].[" + self.my_table + "]') AND type in (N'U')) TRUNCATE TABLE [" + self.my_database + "].[dbo].[" + self.my_table + "]")                
        write_to_log(self.log_path, "truncation of " + self.my_table + ": finished")
        
    def drop_table(self):
        write_to_log(self.log_path, "dropping of " + self.my_table + ": started")
        self.run_sql_code(self.my_connection, "USE " + self.my_database)
        self.run_sql_code(self.my_connection, "IF EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[" + self.my_table + "]') AND type in (N'U')) DROP TABLE [dbo].[" + self.my_table + "]")
        self.run_sql_code(self.my_connection, "IF EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[" + self.my_database + "].[dbo].[" + self.my_table + "]') AND type in (N'U')) DROP TABLE [" + self.my_database + "].[dbo].[" + self.my_table + "]")                
        write_to_log(self.log_path, "dropping of " + self.my_table + ": finished")
         
    def load_data(self):   
        import pandas as pd
        # import datetime
        write_to_log(self.log_path, 'transfer to ' + self.my_table + ': started')
        i = 1
        for my_chunk in pd.read_csv(self.my_file, sep=self.my_separator, chunksize=10**4, dtype=self.my_read_dtype, converters=self.my_converters, keep_default_na=False, na_values=['NULL','null']):
            self.my_connection.engine.execute("USE " + self.my_database) # use ENGINE.execute and do NOT commit this line otherwise the default database will be used
            my_chunk.to_sql(self.my_table, self.my_connection.engine, if_exists='append', index=False, chunksize=10**4, dtype=self.my_dtypes)            
            write_to_log(self.log_path, 'transfer to ' + self.my_table + ': chunk ' + str(i) + ' finished')
            i = i + 1
        write_to_log(self.log_path, 'transfer to ' + self.my_table + ': finished')

# ===================================================================================================
# ===================================================================================================
# ===================================================================================================

# ===================================================================================================
# ETL (END-TO-END TRANSFER OF TABLE/SQL STATEMENT FROM ONE DATABASE/SERVER TO ANOTHER)
# ===================================================================================================

class Etl:
  
    def __init__(self, src_sql, dest_db, dest_tbl, xforms, src_conn, dest_conn, **kwargs):
        self.src_sql = src_sql
        self.dest_db = dest_db
        self.dest_tbl = dest_tbl
        self.xforms = xforms
        self.src_conn = src_conn
        self.dest_conn = dest_conn
        # self.log_path = log_path
        self.log_text = None
        self.my_dtypes = None

        # unpack **kwargs
        self.schema = 'dbo'
        for key, value in kwargs.items():
            if key == 'schema':
                self.schema = value
        self.log_path = None
        for key, value in kwargs.items():
            if key == 'log_path':
                self.log_path = value

    def add_to_dtypes(self, my_dtypes):
        self.my_dtypes = my_dtypes    

    def truncate_table(self):
        
        import datetime
        
        log_text = "truncation of " + self.dest_tbl + " started"
        if self.log_path != None:
            self.__write_to_log(log_text)
        else:
            print(datetime.datetime.now().strftime("%d/%m/%Y: %H:%M:%S") + ': ' + log_text)
        
        my_sql = "USE " + self.dest_db
        self.dest_conn.cursor.execute(my_sql)
        self.dest_conn.connection.commit()

        my_sql = "IF EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[" + self.schema + "].[" + self.dest_tbl + "]') AND type in (N'U')) TRUNCATE TABLE [" + self.schema + "].[" + self.dest_tbl + "]"
        self.dest_conn.cursor.execute(my_sql)
        self.dest_conn.connection.commit()
        
        log_text = "truncation of " + self.dest_tbl + " finished"
        if self.log_path != None:
            self.__write_to_log(log_text)
        else:
            print(datetime.datetime.now().strftime("%d/%m/%Y: %H:%M:%S") + ': ' + log_text)

    def drop_table(self):
        
        import datetime  
        
        log_text = "dropping of " + self.dest_tbl + " started"
        if self.log_path != None:
            self.__write_to_log(log_text)
        else:
            print(datetime.datetime.now().strftime("%d/%m/%Y: %H:%M:%S") + ': ' + log_text)
        
        my_sql = "USE " + self.dest_db
        self.dest_conn.cursor.execute(my_sql)
        self.dest_conn.connection.commit()
        
        my_sql = "IF EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[" + self.schema + "].[" + self.dest_tbl + "]') AND type in (N'U')) DROP TABLE [" + self.schema + "].[" + self.dest_tbl + "]"
        self.dest_conn.cursor.execute(my_sql)
        self.dest_conn.connection.commit()
        
        log_text = "dropping of " + self.dest_tbl + " finished"
        if self.log_path != None:
            self.__write_to_log(log_text)
        else:
            print(datetime.datetime.now().strftime("%d/%m/%Y: %H:%M:%S") + ': ' + log_text)  

    def transfer_data(self):
        
        import pandas as pd
        import datetime  
        
        log_text = "*** transfer to " + self.dest_tbl + " started ***"
        if self.log_path != None:
            self.__write_to_log(log_text)
        else:
            print(datetime.datetime.now().strftime("%d/%m/%Y: %H:%M:%S") + ': ' + log_text) 
        
        # start a counter to write the number of chunks transfered to the log file
        i = 1
        # transfer the data in chunks so only one chunk is in memory at a time
        for my_chunk in pd.read_sql(self.src_sql, self.src_conn.connection, chunksize=10**4):
            # iterate through transformations in my_trans_list
            for t in self.xforms:
                exec(t)
                
            self.dest_conn.engine.execute("USE " + self.dest_db) # use ENGINE.execute and do NOT commit this line otherwise the default database will be used
            # chunksize isn't strictly necessary in the next line as the data is read in chunks
            my_chunk.to_sql(self.dest_tbl, self.dest_conn.engine, if_exists='append', index=False, chunksize=10**4, schema=self.schema, dtype=self.my_dtypes)            
            
            log_text = 'transfer to ' + self.dest_tbl + ': chunk ' + str(i) + ' finished'
            if self.log_path != None:
                self.__write_to_log(log_text)
            else:
                print(datetime.datetime.now().strftime("%d/%m/%Y: %H:%M:%S") + ': ' + log_text)
            i = i + 1
        
        log_text = "*** transfer to " + self.dest_tbl + " finished ***"
        if self.log_path != None:
            self.__write_to_log(log_text)
        else:
            print(datetime.datetime.now().strftime("%d/%m/%Y: %H:%M:%S") + ': ' + log_text) 
        
    def __write_to_log(self, log_text):
        # ^^^ two underscores at the front means the method can't be viewed outside the class
        self.log_text = log_text
        import datetime
        output_text = datetime.datetime.now().strftime("%d/%m/%Y: %H:%M:%S") + ': ' + self.log_text
        print(output_text)
        if len(self.log_path) > 0:    
            log_file = open(self.log_path, 'a')
            log_file.write(output_text + '\n')
            log_file.close()

# ===================================================================================================
# ===================================================================================================
# ===================================================================================================