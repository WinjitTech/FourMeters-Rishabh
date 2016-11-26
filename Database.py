# Author:  <Rohit Salunke>
# Create date: <Create Date,,>
# Description: <Description,,>

import pymssql

try:
    conn = pymssql.connect(server='rohits-pc', user='sa', password='Winjit@123', database='Rishabh')

    cursor = conn.cursor()
    print "connection done"
    cursor.execute("truncate table AngleDeflectionReadings")
    conn.commit()

except Exception as e:
    print("Database error")
    exit()
