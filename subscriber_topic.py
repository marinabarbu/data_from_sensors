#!/usr/bin/python3
# -*- coding: utf-8; mode: python -*-

import sys, os, django
from libcitisim import Broker
import mysql.connector
from mysql.connector import Error
import time

#sys.path.insert('C:/Users/Tehnic/PycharmProjects/Citisim_Web_Interface')
sys.path.append('C:/Users/Tehnic/PycharmProjects/Citisim_Web_Interface/RTD')

from models import Energy


NOTIFY_MSG = '''
New notification:
  * data: {:.6f}
  * source: {}'''


class Subscriber:
    def run(self, args):
        config = 'subscriber-bidir.config'
        if len(args) > 1:
            config = args[1]
        try:
            connection = mysql.connector.connect(host='localhost', database='webinterfacedatabase', user='root',
                                                 password='parola')
            if connection.is_connected():
                db_Info = connection.get_server_info()
                print("Connected to MySQL database... MySQL Server version on", db_Info)
                cursor = connection.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("You are connected to", record[0])
        except Error as e:
            print("Error while connecting to MySQL", e)
            input()
            exit()
        self.connection = connection
        self.cursor = cursor
        broker = Broker(config)

        # - subscribe only to a specific publisher
        # source = "FFFF735700000002"
        # broker.subscribe_to_publisher(source, self.event_printer)
        # print("Subscribing to '" + source + "' publisher")

        # - subscribe to all publishers of a channel
        topic_name = "Energy"
        broker.subscribe(topic_name, self.callback)
        print("Subscribing to '" + topic_name + "' topic")

        print("Awaiting data...")
        broker.wait_for_events()

    def callback(self, value, source, metadata):

        # Printing
        print(NOTIFY_MSG.format(value, source))
        # for key in metadata:
        print("  * {}: {}".format("timestamp", metadata["timestamp"]))

        # Process
        try:
            named_tuple = time.localtime()  # get struct_time
            time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
            print(time_string)
            sqlFormula = "INSERT INTO energy(timestamp, source, data, time) VALUES (%s,%s,%s,%s)"
            val = (str(metadata["timestamp"]),str(source), str(value), str(time_string))
            '''mycursor.execute(sqlFormula, val)
            mydb.commit()
            request = "INSERT INTO energy (timestamp, source, data, time) VALUES (" + str(
                metadata["timestamp"]) + ", '" + str(source) + "', " + str(value) + ", '" + str(time_string) + ");"
                '''

            self.cursor.execute(sqlFormula, val)
            self.connection.commit()
            print("Record inserted successfully into table")
        except mysql.connector.Error as error:
            connection.rollback()  # rollback if any exception occured
            print("Failed inserting record into table {}".format(error))


if __name__ == "__main__":
    Subscriber().run(sys.argv)
