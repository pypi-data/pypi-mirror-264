# pgElephant
PostgreSQL Database Manager

# CREATE ADMIN
bank = PostgreSQL(dbname='your_db',user='your_user',password=your_password)

# CONNECT
bank.connect()

# CHECK
version = bank.version()

# GET ALL VALUES IN ONE TABLE
value_all = bank.get_all(table='users')

# GET A UNIQUE ITEM
value_single = bank.get_single(unique='ryansouza.cwb@gmail.com',table='users',column='email')

# GET A SINGLE LINE
value_first = bank.get_first(unique='ryansouza.cwb@gmail.com',table='users',column='email')

# COMMIT
bank.commit()

# DISCONNECT
bank.disconnect()