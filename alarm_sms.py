import sql

conn = sql.getDbConnection()

r = sql.getSMSList(conn, 'scwook:ai1')

print(r)