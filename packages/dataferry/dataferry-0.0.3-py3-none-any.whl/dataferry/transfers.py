from dataferry.functions import write_to_log
from dataferry.execution import run_hive_code

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

class ExportHiveSQLStatementsToLocalFiles():
    
    def __init__(self, script_folder, master_list, **kwargs):

        # pass the class a list so it can generate and execute one set of scripts in one go 
        # becasue creating a class per export would mean running a set of scripts per file
        # list order: [my_connection, source_table, local_file, edge_node_folder]

        self.script_folder = script_folder
        self.master_list = master_list
        
        # unpack **kwargs
        self.process_name = None
        for key, value in kwargs.items():
            if key == 'process_name':
                self.process_name = value        
        self.log_path = None
        for key, value in kwargs.items():
            if key == 'log_path':
                self.log_path = value
        
    def generate_scripts(self):    
        
        import configparser
        import config.generic_defs as gd
        from gen_mods.misc_fns import write_to_new_text_file, append_to_text_file
        from config.config_defs import CONFIG_PATH
        
        if self.log_path != None:
            write_to_log(self.log_path, 'started generating putty script')
        
        # generate putty script        
        my_path = self.script_folder + r'\auto_gen_putty_script.txt'    
        write_to_new_text_file(my_path, gd.putty_generic_start)        

        # over-ride generic variables
        if self.process_name != None:            
            log_name = 'log_' + self.process_name               
            my_text = "my_header='" + log_name + "'"
            append_to_text_file(my_path, my_text)
            # log_path = edge_node_folder + log_name + ".txt"       
            my_text = "log_path=${logs_folder}'" + log_name + ".txt'"
            append_to_text_file(my_path, my_text)
            
        # create log and tell it the process has started
        my_text = "fn_create_log 'process started'"
        append_to_text_file(my_path, my_text)
        my_text = "fn_update_email 'process started'"
        append_to_text_file(my_path, my_text)

        for ml in self.master_list:            
                
            # get variables from list
            sql_statement = ml[1]            
            local_file = ml[2]
            edge_node_folder = ml[3]
            
            # my_split = source_table.split('.')
            # my_database = my_split[0]
            
            # get file name from path
            my_split = local_file.split('\\')
            my_file = my_split[len(my_split)-1]
            
            # tell log file exporting has started
            # my_text = "echo `date +%d/%m/%Y` - `date +%H:%M:%S` - 'started exporting " + source_table + " to " + edge_node_folder + my_file  + "' >> ${log_path}"
            my_text = "fn_update_log '" + "started exporting data to " + edge_node_folder + my_file  + "'"
            append_to_text_file(my_path, my_text)
            
            # write command to export data to script file
            # my_text = "fn_export_data '" + my_database + "' '" + source_table + "'"
            my_text = '''hive -e "set hive.cli.print.header=true; ''' + sql_statement + r'''" | sed "s/[\t]/|/g" > "''' + edge_node_folder + my_file + '''"'''
            append_to_text_file(my_path, my_text)
            
            # tell log file exporting has finished
            # my_text = "echo `date +%d/%m/%Y` - `date +%H:%M:%S` - 'finished exporting " + source_table + " to " + edge_node_folder + my_file  + "' >> ${log_path}"
            my_text = "fn_update_log '" + "finished exporting data to "  + edge_node_folder + my_file  + "'"
            append_to_text_file(my_path, my_text)
        
        append_to_text_file(my_path, gd.putty_generic_end)

        if self.log_path != None:
            write_to_log(self.log_path, 'finished generating putty script')

        if self.log_path != None:
            write_to_log(self.log_path, 'started generating winscp script')

        # generate winscp script
        my_path = self.script_folder + r'\auto_gen_winscp_script.txt'
        write_to_new_text_file(my_path, gd.winscp_generic_start)           
        for ml in self.master_list:
            
            # get variables from list
            local_file_path = ml[2]
            edge_node_folder = ml[3]    
            
            # get file from path
            my_split = local_file_path.split('\\')
            my_file = my_split[len(my_split)-1]
            
            # write command to copy file to script file
            my_text = '''get "''' + edge_node_folder + my_file + '''" "''' + local_file_path + '''"'''            
            append_to_text_file(my_path, my_text) 
            
        append_to_text_file(my_path, gd.winscp_generic_end)   

        if self.log_path != None:
            write_to_log(self.log_path, 'finished generating winscp script')

        if self.log_path != None:
            write_to_log(self.log_path, 'started generating batch script')
            
        # generate batch_script
        my_path = self.script_folder + r'\auto_gen_batch_script.bat'
        write_to_new_text_file(my_path, gd.generic_batch_start)
        append_to_text_file(my_path, gd.generic_batch_putty)
        append_to_text_file(my_path, gd.generic_batch_winscp)
        append_to_text_file(my_path, gd.generic_batch_end)

        if self.log_path != None:
            write_to_log(self.log_path, 'finished generating batch script')

        if self.log_path != None:
            write_to_log(self.log_path, 'started creating home folder path file')
        
        # create home folder path file    
        config = configparser.ConfigParser()		
        config.read(CONFIG_PATH)
        other = config["other"]        
        home_folder = other["local_folder"] + '\\'    
        my_path = self.script_folder + r'\home_folder_path.txt'
        write_to_new_text_file(my_path, home_folder)

        if self.log_path != None:
            write_to_log(self.log_path, 'finished creating home folder path file')

    def create_files(self):
        
        from gen_mods.misc_fns import run_subprocess  
        
        run_subprocess(self.script_folder + r'\auto_gen_batch_script.bat', self.log_path)

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

class ExportHiveTablesToLocalFiles():
    
    def __init__(self, script_folder, master_list, **kwargs):

        # pass the class a list so it can generate and execute one set of scripts in one go 
        # becasue creating a class per export would mean running a set of scripts per file
        # list order: [my_connection, source_table, local_file, edge_node_folder]

        self.script_folder = script_folder
        self.master_list = master_list
        
        # unpack **kwargs
        self.process_name = None
        for key, value in kwargs.items():
            if key == 'process_name':
                self.process_name = value        
        self.log_path = None
        for key, value in kwargs.items():
            if key == 'log_path':
                self.log_path = value        

    def generate_scripts(self):    
        
        import configparser
        import config.generic_defs as gd
        from gen_mods.misc_fns import write_to_new_text_file, append_to_text_file
        from config.config_defs import CONFIG_PATH
        
        if self.log_path != None:
            write_to_log(self.log_path, 'started generating putty script')
        
        # generate putty script        
        my_path = self.script_folder + r'\auto_gen_putty_script.txt'    
        write_to_new_text_file(my_path, gd.putty_generic_start)        

        # over-ride generic variables
        if self.process_name != None:            
            log_name = 'log_' + self.process_name               
            my_text = "my_header='" + log_name + "'"
            append_to_text_file(my_path, my_text)
            # log_path = edge_node_folder + log_name + ".txt"       
            my_text = "log_path=${logs_folder}'" + log_name + ".txt'"
            append_to_text_file(my_path, my_text)
            
        # create log and tell it the process has started
        my_text = "fn_create_log 'process started'"
        append_to_text_file(my_path, my_text)
        my_text = "fn_update_email 'process started'"
        append_to_text_file(my_path, my_text)

        for ml in self.master_list:            
                
            # get variables from list
            source_table = ml[1]            
            local_file = ml[2]
            edge_node_folder = ml[3]
            
            # my_split = source_table.split('.')
            # my_database = my_split[0]
            
            # get file name from path
            my_split = local_file.split('\\')
            my_file = my_split[len(my_split)-1]
            
            # tell log file exporting has started
            # my_text = "echo `date +%d/%m/%Y` - `date +%H:%M:%S` - 'started exporting " + source_table + " to " + edge_node_folder + my_file  + "' >> ${log_path}"
            my_text = "fn_update_log '" + "started exporting " + source_table + " to " + edge_node_folder + my_file  + "'"
            append_to_text_file(my_path, my_text)
            
            # write command to export data to script file
            # my_text = "fn_export_data '" + my_database + "' '" + source_table + "'"
            my_text = "hive -e 'set hive.cli.print.header=true; select * from " + source_table + r"' | sed 's/[\t]/|/g' > '" + edge_node_folder + my_file + "'"
            append_to_text_file(my_path, my_text)             
            
            # tell log file exporting has finished
            # my_text = "echo `date +%d/%m/%Y` - `date +%H:%M:%S` - 'finished exporting " + source_table + " to " + edge_node_folder + my_file  + "' >> ${log_path}"
            my_text = "fn_update_log '" + "finished exporting " + source_table + " to " + edge_node_folder + my_file  + "'"
            append_to_text_file(my_path, my_text)
        
        append_to_text_file(my_path, gd.putty_generic_end)

        if self.log_path != None:
            write_to_log(self.log_path, 'finished generating putty script')

        if self.log_path != None:
            write_to_log(self.log_path, 'started generating winscp script')

        # generate winscp script
        my_path = self.script_folder + r'\auto_gen_winscp_script.txt'
        write_to_new_text_file(my_path, gd.winscp_generic_start)           
        for ml in self.master_list:
            
            # get variables from list
            local_file_path = ml[2]
            edge_node_folder = ml[3]    
            
            # get file from path
            my_split = local_file_path.split('\\')
            my_file = my_split[len(my_split)-1]
            
            # write command to copy file to script file
            my_text = '''get "''' + edge_node_folder + my_file + '''" "''' + local_file_path + '''"'''            
            append_to_text_file(my_path, my_text) 
            
        append_to_text_file(my_path, gd.winscp_generic_end)   

        if self.log_path != None:
            write_to_log(self.log_path, 'finished generating winscp script')

        if self.log_path != None:
            write_to_log(self.log_path, 'started generating batch script')
            
        # generate batch_script
        my_path = self.script_folder + r'\auto_gen_batch_script.bat'
        write_to_new_text_file(my_path, gd.generic_batch_start)
        append_to_text_file(my_path, gd.generic_batch_putty)
        append_to_text_file(my_path, gd.generic_batch_winscp)
        append_to_text_file(my_path, gd.generic_batch_end)

        if self.log_path != None:
            write_to_log(self.log_path, 'finished generating batch script')

        if self.log_path != None:
            write_to_log(self.log_path, 'started creating home folder path file')
        
        # create home folder path file    
        config = configparser.ConfigParser()		
        config.read(CONFIG_PATH)
        other = config["other"]        
        home_folder = other["local_folder"] + '\\'    
        my_path = self.script_folder + r'\home_folder_path.txt'
        write_to_new_text_file(my_path, home_folder)

        if self.log_path != None:
            write_to_log(self.log_path, 'finished creating home folder path file')

    def create_files(self):
        
        from gen_mods.misc_fns import run_subprocess  
        
        run_subprocess(self.script_folder + r'\auto_gen_batch_script.bat', self.log_path)

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

class LoadTextFileToDatabricks():
    
    def __init__(self, dbx_connection, activate_bat, local_file, file_delimiter, dbfs_file, dbx_table, field_definitions):
        
        self.dbx_connection = dbx_connection
        self.activate_bat = activate_bat
        self.local_file = local_file
        self.file_delimiter = file_delimiter
        self.dbfs_file = dbfs_file
        self.dbx_table = dbx_table
        self.field_definitions = field_definitions
        self.log_path = ''

    def load_data(self):    

        import subprocess
        
        # copy the local file to dbfs
        subprocess.run(r'call ' + self.activate_bat + ' && call activate my_env && call dbfs cp ' + self.local_file + ' dbfs:' + self.dbfs_file + ' --overwrite', shell=True)
    
        # create the table to be populated
        cursor = self.dbx_connection.connection.cursor()
        cursor.execute('drop table if exists ' + self.dbx_table)
        cursor.execute('create table ' + self.dbx_table + '( ' + self.field_definitions + ')')
     
        # COPY INTO default.tam_seg_stg_james_is_a_winner
        # FROM '/FileStore/tables/james_is_a_winner.txt'
        # FILEFORMAT = CSV
        # FORMAT_OPTIONS ('inferSchema' = 'true', 'header' = 'true', 'delimiter' = '|')
        # COPY_OPTIONS ('inferSchema' = 'true');    
     
        # copy the data into the table
        cursor.execute("COPY INTO " + self.dbx_table + " FROM '" + self.dbfs_file + "' FILEFORMAT = CSV FORMAT_OPTIONS ('inferSchema' = 'true', 'header' = 'true', 'delimiter' = '" + self.file_delimiter + "') COPY_OPTIONS ('inferSchema' = 'true')")
    
        # delete the text file from dbfs
        subprocess.run(r'call ' + self.activate_bat + ' && call activate my_env && call databricks fs rm dbfs:'  + self.dbfs_file, shell=True)

class LoadLocalFilesToHiveTables():
    
    def __init__(self, script_folder, master_list, **kwargs):
        
        # pass the class a list so it can generate and execute one set of scripts in one go
        # # becasue creating a class per export would mean running a set of scripts per file
        # list order: [my_connection, local_file_path, edge_node_folder, destination_table, create_table_statement]

        self.script_folder = script_folder
        self.master_list = master_list

        # unpack **kwargs
        self.process_name = None
        for key, value in kwargs.items():
            if key == 'process_name':
                self.process_name = value
        self.log_path = None
        for key, value in kwargs.items():
            if key == 'log_path':
                self.log_path = value
                
    def generate_scripts(self):    
        
        import configparser
        import config.generic_defs as gd
        from gen_mods.misc_fns import write_to_new_text_file, append_to_text_file
        from config.config_defs import CONFIG_PATH

        if self.log_path != None:
            write_to_log(self.log_path, 'started generating winscp script')
    
        # generate winscp script
        my_path = self.script_folder + r'\auto_gen_winscp_script.txt'
        write_to_new_text_file(my_path, gd.winscp_generic_start)           
        for ml in self.master_list:
            
            # get variables from list
            local_file_path = ml[1]
            edge_node_folder = ml[2]    
            
            # get file name from path
            my_split = local_file_path.split('\\')
            my_file = my_split[len(my_split)-1]
            
            # write command to copy file to script file
            my_text = '''put "''' + local_file_path + '''" "''' + edge_node_folder + my_file + '''"'''
            append_to_text_file(my_path, my_text)         
            
        append_to_text_file(my_path, gd.winscp_generic_end)

        if self.log_path != None:
            write_to_log(self.log_path, 'finished generating winscp script')

        if self.log_path != None:
            write_to_log(self.log_path, 'started generating putty script')

        # generate putty script        
        my_path = self.script_folder + r'\auto_gen_putty_script.txt'    
        write_to_new_text_file(my_path, gd.putty_generic_start)
        
        # over-ride generic variables
        if self.process_name != None:            
            log_name = 'log_' + self.process_name               
            my_text = "my_header='" + log_name + "'"
            append_to_text_file(my_path, my_text)
            # log_path = edge_node_folder + log_name + ".txt"       
            my_text = "log_path=${logs_folder}'" + log_name + ".txt'"
            append_to_text_file(my_path, my_text)
            
        # create log and tell it the process has started
        my_text = "fn_create_log 'process started'"
        append_to_text_file(my_path, my_text)
        my_text = "fn_update_email 'process started'"
        append_to_text_file(my_path, my_text)   
                
        for ml in self.master_list:
            
            # get variables frm list
            local_file_path = ml[1]
            edge_node_folder = ml[2]  
            destination_table = ml[3]   
            
            # get database name from full table name
            my_split = destination_table.split('.')
            my_database_folder = '/data/warehouse/' + my_split[0] + '/'   
            
            # get file name from path
            my_split = local_file_path.split('\\')
            my_file = my_split[len(my_split)-1]    
            
            # tell log file copying has started
            # my_text = "echo `date +%d/%m/%Y` - `date +%H:%M:%S` - 'started copying " + edge_node_folder + my_file + " to " + my_database_folder + my_file  + "' >> ${log_path}"
            my_text = "fn_update_log '" + "started copying " + edge_node_folder + my_file + " to " + my_database_folder + my_file  + "'"
            append_to_text_file(my_path, my_text)
            
            # write command to copy file to log file
            my_text = "hdfs dfs -put -f " + edge_node_folder + my_file + " " + my_database_folder + my_file
            append_to_text_file(my_path, my_text)      
            
            # tell log file copying has finished
            # my_text = "echo `date +%d/%m/%Y` - `date +%H:%M:%S` - 'finished copying " + edge_node_folder + my_file + " to " + my_database_folder + my_file  + "' >> ${log_path}"
            my_text = "fn_update_log '" + "finished copying " + edge_node_folder + my_file + " to " + my_database_folder + my_file  + "'"
            append_to_text_file(my_path, my_text)
            
        append_to_text_file(my_path, gd.putty_generic_end)

        if self.log_path != None:
            write_to_log(self.log_path, 'finished generating putty script')

        if self.log_path != None:
            write_to_log(self.log_path, 'started generating batch script')
        
        # generate batch_script
        my_path = self.script_folder + r'\auto_gen_batch_script.bat'
        write_to_new_text_file(my_path, gd.generic_batch_start)
        append_to_text_file(my_path, gd.generic_batch_winscp)
        append_to_text_file(my_path, gd.generic_batch_putty)
        append_to_text_file(my_path, gd.generic_batch_end)

        if self.log_path != None:
            write_to_log(self.log_path, 'finished generating batch script')

        if self.log_path != None:
            write_to_log(self.log_path, 'started creating home folder path file')
        
        # create home folder path file    
        config = configparser.ConfigParser()		
        config.read(CONFIG_PATH)
        other = config["other"]        
        home_folder = other["local_folder"] + '\\'    
        my_path = self.script_folder + r'\home_folder_path.txt'
        write_to_new_text_file(my_path, home_folder)

        if self.log_path != None:
            write_to_log(self.log_path, 'finished creating home folder path file')
        
    def transfer_files(self):
        
        from gen_mods.misc_fns import run_subprocess  
        
        run_subprocess(self.script_folder + r'\auto_gen_batch_script.bat', self.log_path)
        
    def load_data(self):
        
        from gen_mods.data_conns import LoadHdfsFileToHiveTable
        
        for ml in self.master_list:
        
            my_connection = ml[0]
            local_file_path = ml[1]
            destination_table = ml[3]
            create_table_statement = ml[4]

            my_split = destination_table.split('.')
            my_database_folder = '/data/warehouse/' + my_split[0] + '/'              
            my_split = local_file_path.split('\\')
            my_file = my_split[len(my_split)-1]
            
            my_load = LoadHdfsFileToHiveTable(my_connection, destination_table, create_table_statement, my_database_folder + my_file, self.log_path)
            my_load.load_data()

class LoadHdfsFileToHiveTable():
    
    def __init__(self, my_connection, destination_table, create_table_statement, text_file_path, log_path):
        
        self.my_connection = my_connection
        self.destination_table = destination_table
        self.create_table_statement = create_table_statement
        self.text_file_path = text_file_path
        self.log_path = log_path
        
    def load_data(self):

        run_hive_code(self.my_connection, 'drop table if exists ' + self.destination_table, self.log_path)
        run_hive_code(self.my_connection, self.create_table_statement, self.log_path)
        my_sql = "load data inpath '" + self.text_file_path + "' overwrite into table " + self.destination_table
        run_hive_code(self.my_connection, my_sql, self.log_path)

def load_text_file_to_databricks(dbx_connection, activate_bat, local_file, file_delimiter, dbfs_file, dbx_table, field_definitions):

# FUNCTION EQUIVALENT TO THE CLASS LoadTextFileToDatabricks    

    import subprocess
    
    # copy the local file to dbfs
    subprocess.run(r'call ' + activate_bat + ' && call activate my_env && call dbfs cp ' + local_file + ' dbfs:' + dbfs_file + ' --overwrite', shell=True)

    # create the table to be populated
    cursor = dbx_connection.connection.cursor()
    cursor.execute('drop table if exists ' + dbx_table)
    cursor.execute('create table ' + dbx_table + '( ' + field_definitions + ')')
 
    # COPY INTO default.tam_seg_stg_james_is_a_winner
    # FROM '/FileStore/tables/james_is_a_winner.txt'
    # FILEFORMAT = CSV
    # FORMAT_OPTIONS ('inferSchema' = 'true', 'header' = 'true', 'delimiter' = '|')
    # COPY_OPTIONS ('inferSchema' = 'true');    
 
    # copy the data into the table
    cursor.execute("COPY INTO " + dbx_table + " FROM '" + dbfs_file + "' FILEFORMAT = CSV FORMAT_OPTIONS ('inferSchema' = 'true', 'header' = 'true', 'delimiter' = '" + file_delimiter + "') COPY_OPTIONS ('inferSchema' = 'true')")

    # delete the text file from dbfs
    subprocess.run(r'call ' + activate_bat + ' && call activate my_env && call databricks fs rm dbfs:'  + dbfs_file, shell=True)

# ===================================================================================================
# ===================================================================================================
# ===================================================================================================

# ===================================================================================================
# ETL (END-TO-END TRANSFER OF TABLE FROM ONE DATABASE/SERVER TO ANOTHER)
# ===================================================================================================

class Etl:

# *** TRANSFER TABLE FROM DATABRICKS OR HIVE TO SQL SERVER BUT NOT THE OTHER WAY ROUND ***
# THE OTHER WAY ROUND REQUIRES EITHER: 
# A TWO-STEP PROCESS USING SQL SERVER TO LOCAL TEXT FILE THEN LOCAL TEXT FILE TO DATABRICKS OR HIVE) OR:
# FOR SQL SEVER TO DATABRICKS, THE CLASS TransferDataToDataBricks
# NO END_TO_END CLASS EXISTS FOR SQL SERVER HIVE SO A TWO-STEP PROCESS IS REQUIRED (A CLASS COULD BE BUILT EASILY ENOUGH THOUGH)
  
    # def __init__(self, src_sql, dest_db, dest_tbl, xforms, src_conn, dest_conn, log_path):
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

        # my_sql = "IF EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[" + self.dest_tbl + "]') AND type in (N'U')) TRUNCATE TABLE [dbo].[" + self.dest_tbl + "]"
        if self.dest_conn.platform == 'dbx':
            my_sql = "truncate table " + self.dest_db + "." + self.dest_tbl
        else:
            my_sql = "IF EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[" + self.schema + "].[" + self.dest_tbl + "]') AND type in (N'U')) TRUNCATE TABLE [" + self.schema + "].[" + self.dest_tbl + "]"
        # my_sql = "TRUNCATE TABLE [dbo].[" + self.dest_tbl + "]"
        # my_sql = "TRUNCATE TABLE [" + self.dest_db + "].[dbo].[" + self.dest_tbl + "]"
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
        
        # my_sql = "IF EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[" + self.dest_tbl + "]') AND type in (N'U')) DROP TABLE [dbo].[" + self.dest_tbl + "]"
        if self.dest_conn.platform == 'dbx':
            my_sql = "drop table if exists " + self.dest_db + "." + self.dest_tbl
        else:
            my_sql = "IF EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[" + self.schema + "].[" + self.dest_tbl + "]') AND type in (N'U')) DROP TABLE [" + self.schema + "].[" + self.dest_tbl + "]"
        # my_sql = "TRUNCATE TABLE [dbo].[" + self.dest_tbl + "]"
        # my_sql = "TRUNCATE TABLE [" + self.dest_db + "].[dbo].[" + self.dest_tbl + "]"
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
            
            # if self.dest_conn.platform == 'dbx':
            #     self.dest_conn.cursor.execute("USE " + self.dest_db)
            #     my_chunk.to_sql(self.dest_tbl, self.dest_conn.engine, if_exists='append', index=False, chunksize=10**4)            
            # else:
                
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

class TransferDataToDataBricks:

# TRANSFER RESULT OF SQL STATEMENT FROM SQL SERVER OR HIVE TO DATABRICKS
# AT PRESENT THE MODULE TO ADD AN SQL ALCHEMY ENGINE TO THE DATABRICK MODULE CANNOT BE INSTALLED
# SO THIS IS A WORK-AROUND THAT USES TWO STEPS
# ONE TO EXPORT AN SQL STATEMENT TABLE AS A TEXT FILE
# AND ONE TO COPY TEH TEXT FILE TO DBFS USING CLI THEN LOAD IT TO A TABLE "COPY INTO schema.table"
    
    def __init__(self, source_connection, dbx_connection, source_sql, activate_bat, local_file, file_delimiter, dbfs_file, dbx_table, field_definitions):
        
        self.source_connection = source_connection
        self.dbx_connection = dbx_connection
        self.source_sql = source_sql
        self.activate_bat = activate_bat
        self.local_file = local_file
        self.file_delimiter = file_delimiter
        self.dbfs_file = dbfs_file
        self.dbx_table = dbx_table
        self.field_definitions = field_definitions
        self.log_path = ''

    def export_sql_statement_as_text_file(self):
                 
        import pandas as pd
        import os
        
        # delete file if it already exists
        if os.path.exists(self.local_file):
            os.remove(self.local_file)
        
        msg = 'started transferring results of sql statement to ' + self.local_file
        print(msg)
        if self.log_path != None and len(self.log_path) > 0:
            # write_to_log(self.log_path, 'transfer to ' + self.dbx_table + ': started')
            write_to_log(self.log_path, msg)
        
        i = 1
        for my_chunk in pd.read_sql(self.source_sql, self.source_connection.connection, chunksize=10**4):    
            # append the first chunk with headers
            if i==1:
                my_chunk.to_csv(self.local_file, sep=self.file_delimiter, index=False, mode='w', header=True)
            # append the other chunks without headers
            else:
                my_chunk.to_csv(self.local_file, sep=self.file_delimiter, index=False, mode='a', header=False)
            msg = 'transfer to ' + self.local_file + ': chunk ' + str(i) + ' finished'
            print(msg)
            if self.log_path != None and len(self.log_path) > 0:
                # write_to_log(self.log_path, 'transfer to ' + self.dbx_table + ': chunk ' + str(i) + ' finished')
                write_to_log(self.log_path, msg)
            i = i + 1
        
        msg = 'finished transferring results of sql statement to ' + self.local_file
        if self.log_path != None and len(self.log_path) > 0:
            # write_to_log(self.log_path, 'transfer to ' + self.dbx_table + ': finished')
            write_to_log(self.log_path, msg)
        
    def load_text_file_to_databricks(self):
    
        import subprocess

        # copy the local file to dbfs
        msg = 'started copying ' + self.local_file + ' to ' + self.dbfs_file
        print(msg)
                
        subprocess.run(r'call ' + self.activate_bat + ' && call activate my_env && call dbfs cp ' + self.local_file + ' dbfs:' + self.dbfs_file + ' --overwrite', shell=True)

        msg = 'finished copying ' + self.local_file + ' to ' + self.dbfs_file
        print(msg)
    
        # create the table to be populated
        msg = 'started creating ' + self.dbx_table
        print(msg)

        # create string for create table statement
        my_string = ''
        for m in self.field_definitions:
            my_string = my_string + m[0] + ' ' + m[1] + ","
        my_string = my_string[:-1]

        cursor = self.dbx_connection.connection.cursor()
        cursor.execute('drop table if exists ' + self.dbx_table)
        # cursor.execute('create table ' + self.dbx_table + '( ' + self.field_definitions + ')')
        cursor.execute('create table ' + self.dbx_table + '( ' + my_string + ')')

        msg = 'finished creating ' + self.dbx_table
        print(msg)
        
        # COPY INTO default.tam_seg_stg_james_is_a_winner
        # FROM '/FileStore/tables/james_is_a_winner.txt'
        # FILEFORMAT = CSV
        # FORMAT_OPTIONS ('inferSchema' = 'true', 'header' = 'true', 'delimiter' = '|')
        # COPY_OPTIONS ('inferSchema' = 'true');    

        # COPY INTO default.tam_seg_stg_tbl_ref_vip_no_ecc_b
        # FROM '/FileStore/tables/tbl_ref_vip_no_ecc_b.txt'
        # FILEFORMAT = CSV
        # FORMAT_OPTIONS ('mergeSchema' = 'true', 'header' = 'true', 'delimiter' = '|')
        # COPY_OPTIONS ('mergeSchema' = 'true');   
     
        # copy the data into the table
        msg = 'started copying ' + self.dbfs_file + ' into ' + self.dbx_table
        print(msg)        

        # create string for copy into statement
        my_string = ''
        for m in self.field_definitions:
            my_string = my_string + m[0] + '::' + m[1] + ","
        my_string = my_string[:-1]
       
        # cursor.execute("COPY INTO " + self.dbx_table + " FROM '" + self.dbfs_file + "' FILEFORMAT = CSV FORMAT_OPTIONS ('inferSchema' = 'true', 'header' = 'true', 'delimiter' = '" + self.file_delimiter + "') COPY_OPTIONS ('inferSchema' = 'true')")
        # cursor.execute("COPY INTO " + self.dbx_table + " FROM '" + self.dbfs_file + "' FILEFORMAT = CSV FORMAT_OPTIONS ('mergeSchema' = 'true', 'header' = 'true', 'delimiter' = '" + self.file_delimiter + "') COPY_OPTIONS ('mergeSchema' = 'true')")
        # cursor.execute("COPY INTO " + self.dbx_table + " FROM (SELECT " + my_string + " FROM '" + self.dbfs_file + "') FILEFORMAT = CSV FORMAT_OPTIONS ('inferSchema' = 'true', 'header' = 'true', 'delimiter' = '" + self.file_delimiter + "') COPY_OPTIONS ('inferSchema' = 'true')")
        cursor.execute("COPY INTO " + self.dbx_table + " FROM (SELECT " + my_string + " FROM '" + self.dbfs_file + "') FILEFORMAT = CSV FORMAT_OPTIONS ('mergeSchema' = 'true', 'header' = 'true', 'delimiter' = '" + self.file_delimiter + "') COPY_OPTIONS ('mergeSchema' = 'true')")       
        # ^^^ use 'mergeSchema' = 'true' to use the field data types specified in the create table statment

        self.dbx_connection.cursor.execute("select count(*) from " + self.dbx_table)        
        my_row_count = self.dbx_connection.cursor.fetchone()[0]
        msg = str(f"{my_row_count:,}") + " records loaded to " + self.dbx_table
        print(msg)

        msg = 'finished copying ' + self.dbfs_file + ' into ' + self.dbx_table
        print(msg)   
        
        # databricks fs rm dbfs:/FileStore/tables/TD_OPG.txt
        
        # delete the text file from dbfs
        subprocess.run(r'call ' + self.activate_bat + ' && call activate my_env && call databricks fs rm dbfs:'  + self.dbfs_file, shell=True)
        
    def transfer_data_to_databricks(self):
        
        print('*** process started ***')
        
        self.export_sql_statement_as_text_file()
        self.load_text_file_to_databricks()

        print('*** process finished ***')

def transfer_data_to_databricks(source_connection, dbx_connection, source_sql, activate_bat, local_file, file_delimiter, dbfs_file, dbx_table, field_definitions):

# A FUNCTION THAT DOES THE SAME AS THE ABOVE CLASS    

    # import subprocess
    # import pandas as pd    
    
    # # load the source data to a dataframe
    # df = pd.read_sql(source_sql, source_connection.connection)
    
    # # export the dataframe to a local file
    # df.to_csv(local_file, index=False, sep = '|')
    
    # # copy the local file to dbfs
    # subprocess.run(r'call ' + activate_bat + ' && call activate my_env && call dbfs cp ' + local_file + ' dbfs:' + dbfs_file + ' --overwrite', shell=True)

    # # create the table to be populated
    # cursor = dbx_connection.connection.cursor()
    # cursor.execute('drop table if exists ' + dbx_table)
    # cursor.execute('create table ' + dbx_table + '( ' + field_definitions + ')')
 
    # # COPY INTO default.tam_seg_stg_james_is_a_winner
    # # FROM '/FileStore/tables/james_is_a_winner.txt'
    # # FILEFORMAT = CSV
    # # FORMAT_OPTIONS ('inferSchema' = 'true', 'header' = 'true', 'delimiter' = '|')
    # # COPY_OPTIONS ('inferSchema' = 'true');    
 
    # # copy the data into the table
    # cursor.execute("COPY INTO " + dbx_table + " FROM '" + dbfs_file + "' FILEFORMAT = CSV FORMAT_OPTIONS ('inferSchema' = 'true', 'header' = 'true', 'delimiter' = '" + file_delimiter + "') COPY_OPTIONS ('inferSchema' = 'true')")
    
    export_sql_statement_as_text_file(source_connection, source_sql, local_file, file_delimiter, '')
    load_text_file_to_databricks(dbx_connection, activate_bat, local_file, file_delimiter, dbfs_file, dbx_table, field_definitions)

# ===================================================================================================
# ===================================================================================================
# ===================================================================================================