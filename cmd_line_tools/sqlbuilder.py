import sqlite3

sqlite_file = 'passwords.sqlite'    # name of the sqlite database file
table_name1 = 'auth'  # name of the table to be created
new_field = 'user' # name of the column
field_type = 'TEXT'  # column data type
new_field1 = 'password'
field_type1 = 'TEXT'  # column data type

# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

# Creating a new SQLite table with 1 column
# c.execute('DROP TABLE {tn}'\
#         .format(tn=table_name1, nf=new_field, ft=field_type, nf1=new_field1, ft1=field_type1))

# c.execute('CREATE TABLE {tn} ({nf} {ft}, {nf1} {ft1})'\
#         .format(tn=table_name1, nf=new_field, ft=field_type, nf1=new_field1, ft1=field_type1))

# c.execute('insert into {tn} values ("user1", "supersecret")'\
#         .format(tn=table_name1))

c.execute('Select * from {tn}'\
        .format(tn=table_name1))
print(c.fetchall())

# Committing changes and closing the connection to the database file
# conn.commit()
conn.close()