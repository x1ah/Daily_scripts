#!/usr/bin/env python
# encoding: utf-8

import os
import csv
import sqlite3

def all_classes(path):
    for root, dirs, files in os.walk(path):
        for f in files:
            yield os.path.join(root, f)

connect_db = lambda db: sqlite3.connect(db)

class CsvToDB:
    def __init__(self, csvdir, database, tablename):
        self.connect = connect_db(database)
        self.database = database
        self.tablename = tablename
        self.all_csv_file = all_classes(csvdir)

    def create_table(self):
        self.connect.execute("""create table {0}(
                            Sno char(10) primary key,
                            Pswd char(6) not null);""".format(self.tablename))
        self.connect.commit()

    def insert(self):
        for classes in self.all_csv_file:
            with open(classes, 'rb') as csvfile:
                spam = csv.reader(csvfile)
                for item in spam:
                    sno, pswd = item[1], item[3][2:-1]
                    if sno.isdigit():
                        patt = ("INSERT INTO {0} VALUES (\"{1}\", \"{2}\");"
                                .format(self.tablename, sno, pswd))
                        self.connect.execute(patt)
                        print(patt)
        self.connect.commit()

    def close(self):
        self.connect.close()

if __name__ == "__main__":
    main = CsvToDB("CUMTB-16", "test16.db", "testtable")
    main.create_table()
    main.insert()
    main.close()
