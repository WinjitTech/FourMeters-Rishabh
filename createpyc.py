# Author:  <Rohit Salunke>
# Create date: <Create Date,,>
# Description: <Description,,>

import py_compile
import glob

try:
        for f in glob.glob("*.py"):
                py_compile.compile(f)
        print ("Success...!!!")
except Exception, e:
        print str(e)
