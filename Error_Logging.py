# Author:  <Rohit Salunke>
# Create date: <Create Date,,>
# Description: <Description,,>


import logging

logger = logging.getLogger("error/info")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.FileHandler("D:\\default.log")
handler.setFormatter(formatter)
logger.addHandler(handler)
