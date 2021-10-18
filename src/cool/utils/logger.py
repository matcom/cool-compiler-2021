import logging
import os

cwd = os.getcwd()

try:
    logging.basicConfig(
        level=logging.DEBUG,
        filename=f"{cwd}/src/cool/parser/output/parselog.txt",
        filemode="w",
        format="%(filename)10s:%(lineno)4d:%(message)s"
    )

    log = logging.getLogger()
except:
    logging.basicConfig(
        level=logging.DEBUG,
        filename=f"{cwd}/cool/parser/output/parselog.txt",
        filemode="w",
        format="%(filename)10s:%(lineno)4d:%(message)s"
    )

    log = logging.getLogger()
