# Author:  <Rohit Salunke>
# Create date: <Create Date,,>
# Description: <Description,,>

import py_compile
import glob

try:
        for file in glob.glob("*.py"):
                py_compile.compile(file)

        print ("Success...!!!")
except Exception, e:
        print str(e)
