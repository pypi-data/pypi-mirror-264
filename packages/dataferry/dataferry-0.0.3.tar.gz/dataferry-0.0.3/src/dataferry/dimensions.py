from functions import write_to_log

# ===================================================================================================
# UPDATE DIMENSION TABLE
# ===================================================================================================

class UpdateDimensionTable():

# CREATES NEW DIMENSION RECORDS IN PYTHON THEN APPENDS THEM TO THE SQL SERVER TABLE
    
    def __init__(self, conn, dim_database, dim_table, dim_id, dim_desc, fact_database, fact_table, fact_desc):
        self.conn = conn
        self.dim_database = dim_database
        self.dim_table = dim_table
        self.dim_id = dim_id
        self.dim_desc = dim_desc
        self.fact_database = fact_database
        self.fact_table = fact_table
        self.fact_desc = fact_desc
    
    def update_table(self):
        
        import pandas as pd
    
        self.dim_frame = pd.read_sql('SELECT * FROM ' + self.dim_database + '.dbo.' + self.dim_table, self.conn.engine)
        self.fact_frame = pd.read_sql('SELECT DISTINCT ' + self.fact_desc + ' FROM ' + self.fact_database + '.dbo.' + self.fact_table, self.conn.engine)
        
        # temp_frame = pd.DataFrame({self.fact_desc: ['DUMMY 1', 'DUMMY 2']})
        # self.fact_frame = self.fact_frame.append(temp_frame)
        # self.fact_frame = self.fact_frame.reset_index(drop=True)
        
        mask = self.fact_frame[self.fact_desc].isin(self.dim_frame[self.dim_desc])
        new_frame = self.fact_frame.loc[~mask]
        
        n = self.dim_frame[self.dim_id].max()
        # new[dim_id] = new[fact_desc].astype('category').cat.codes.add(n + 1)
        new_frame[self.dim_id] = new_frame[self.fact_desc].ne(new_frame[self.fact_desc].shift()).cumsum() + n
        new_frame = new_frame[[self.dim_id, self.dim_desc]]
        
        self.conn.engine.execute("USE " + self.dim_database) # use ENGINE.execute and do NOT commit this line otherwise the default database will be used
        new_frame.to_sql(self.dim_table, self.conn.engine, if_exists='append', index=False)

def update_dbx_dimension_table(my_max_id_table, my_fact_table, my_dimension_table, my_dimension_name, my_dimension_id, my_connection, my_log):

# RUNS SQL CODE ON DBX TO UPDATE DIMENSION TABLE
    
    from gen_mods.data_conns import run_dbx_code
    
    my_sql = '''drop table if exists ''' + my_max_id_table
    run_dbx_code(my_connection, my_sql, my_log)
    
    my_sql = '''
            create table ''' + my_max_id_table + ''' as
            select 'MAX_KEY' as max_key, max(cast(''' + my_dimension_id + ''' as int)) as max_id
            from ''' + my_dimension_table           
    run_dbx_code(my_connection, my_sql, my_log)

    my_sql = '''
            insert into ''' + my_dimension_table + '''
            select cast(mxi.max_id + qry.temp_id as int) as ''' + my_dimension_id + ''', qry.''' + my_dimension_name + '''
            from
              (select a.''' + my_dimension_name + ''', row_number() over(order by a.''' + my_dimension_name + ''') as temp_id, 'MAX_KEY' as max_key
              from (select distinct ''' + my_dimension_name + ''' from ''' + my_fact_table + ''') as a
              left outer join ''' + my_dimension_table + ''' as b on a.''' + my_dimension_name + ''' = b.''' + my_dimension_name + '''
              where b.''' + my_dimension_name + ''' is null) as qry
            left outer join ''' + my_max_id_table + ''' as mxi on qry.max_key = mxi.max_key    
            '''
    run_dbx_code(my_connection, my_sql, my_log)

    my_sql = '''drop table if exists ''' + my_max_id_table
    run_dbx_code(my_connection, my_sql, my_log)

class UpdateHiveDimTable():

# CREATES NEW DIMENSION RECORDS IN PYTHON THEN APPENDS THEM TO THE HIVE TABLE
# WITH OPTIONAL SQL SERVER REPLICATION
    
    def __init__(self, conn, dim_database, dim_table, dim_id, dim_desc, fact_data_frame, fact_desc, output_folder, **kwargs):
        
        self.conn = conn
        self.dim_database = dim_database
        self.dim_table = dim_table
        self.dim_id = dim_id
        self.dim_desc = dim_desc
        self.fact_data_frame = fact_data_frame
        self.fact_desc = fact_desc
        self.output_folder = output_folder
        self.sql_server_replica = []
        
        # unpack **kwargs
        self.log_path = None
        for key, value in kwargs.items():
            if key == 'log_path':
                self.log_path = value
        
    def replicate_in_sql_server(self, ss, db, tbl):
        self.ss = ss
        self.db = db
        self.tbl = tbl
        self.sql_server_replica = [self.ss, self.db, self.tbl]

    def create_new_table(self):
            
        import pandas as pd
        import numpy as np
        
        if self.log_path != None:
            write_to_log(self.log_path, 'create new dimension table proceess started: ' + self.dim_table)
        
        self.dim_frame = pd.read_sql('SELECT * FROM ' + self.dim_database + '.' + self.dim_table, self.conn.connection)
        self.fact_frame = pd.DataFrame(self.fact_data_frame[self.fact_desc].drop_duplicates())
        
        # dummy_frame = pd.DataFrame({self.fact_desc: ['DUMMY 1', 'DUMMY 2']})
        # self.fact_frame = self.fact_frame.append(dummy_frame)
        # self.fact_frame = self.fact_frame.reset_index(drop=True)
        
        mask = self.fact_frame[self.fact_desc].isin(self.dim_frame[self.dim_desc])
        self.new_frame = self.fact_frame.loc[~mask]
        
        n = np.nan_to_num(self.dim_frame[self.dim_id].max()).astype(np.int32)
        self.new_frame[self.dim_id] = self.new_frame[self.fact_desc].ne(self.new_frame[self.fact_desc].shift()).cumsum() + n
        self.new_frame = self.new_frame[[self.dim_id, self.dim_desc]]
        
        self.output_frame = self.dim_frame
        self.output_frame = self.output_frame.append(self.new_frame)
        self.output_frame = self.output_frame.sort_values(self.dim_id)
        
        my_path = self.output_folder + '\\' + self.dim_table + '.txt'
        if self.log_path != None:
            write_to_log(self.log_path, 'started exporting ' + self.dim_table + ' to ' + my_path)        
        self.output_frame.to_csv(my_path, sep="|", index=False)
        if self.log_path != None:
            write_to_log(self.log_path, 'finished exporting ' + self.dim_table + ' to ' + my_path)   
        
        if len(self.sql_server_replica) > 0:            
            self.sql_server_replica[0].engine.execute("USE " + self.sql_server_replica[1])            
            if self.log_path != None:
                write_to_log(self.log_path, 'started exporting ' + self.dim_table + ' to ' + self.sql_server_replica[1] + ' database in ' +  self.sql_server_replica[0].my_server + ' sql server')            
            self.output_frame.to_sql(self.sql_server_replica[2], self.sql_server_replica[0].engine, if_exists='replace', index=False)
            if self.log_path != None:
                write_to_log(self.log_path, 'finished exporting ' + self.dim_table + ' to ' + self.sql_server_replica[1] + ' database in ' +  self.sql_server_replica[0].my_server + ' sql server')            
        if self.log_path != None:
            write_to_log(self.log_path, 'create new dimension table proceess finished: ' + self.dim_table)

# ===================================================================================================
# ===================================================================================================
# ===================================================================================================