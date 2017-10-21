from threading import Thread
from Queue import Queue
import mysql.connector


class DbThread(Thread):
  def __init__(self, connection, cursor, table, data, queue=None):
    super(DbThread, self).__init__()
    self.connection = connection
    self.cursor = cursor
    self.table = table
    self.data = data
    self.queue = queue


class WriterThread(DbThread):
  def run(self):
    # Create query in the format:
    #   "INSERT INTO salaries (emp_no, salary, from_date, to_date)
    #     VALUES (%(emp_no)s, %(salary)s, %(from_date)s, %(to_date)s)"
    values_string = ['%({})s'.format(col) for col in self.data.keys()]
    insert_query = "INSERT INTO {} ({}) VALUES ({})" \
      .format(self.table, ', '.join(self.data.keys()), ', '.join(values_string))
    self.cursor.execute(insert_query, self.data)
    self.connection.commit()


class ReaderThread(DbThread):
  def run(self):
    # data is (a, b) which indicates the inclusive range for this query
    read_query = "SELECT * FROM {0} OFFSET {1} LIMIT {2} - {1} + 1" \
                    .format(self.table, self.data[0], self.data[1])
    self.cursor.execute(read_query)
    return [_ for _ in self.cursor]


class MySQLConnector(Object):
  def __init__(self, user, password, host, database):
    self.connection = mysql.connector.connect(user=user,
                                              password=password,
                                              host=host,
                                              database=database)
    self.cursor = self.connection.cursor()

  def close(self):
    self.connection.close()

  def read_batch(self, table, start, end, num_workers):
    threads = []
    queue = Queue()
    range_size = (end - start + 1) / num_workers
    for i in num_workers:
      a = range_size * i
      b = a + range_size - 1
      thread = ReaderThread(self.connection, self.cursor,
                            table, (a, b), queue=queue)
      thread.start()
      threads.append(thread)
    for thread in threads:
      thread.join()
    rows = []
    while not queue.empty():
      rows.extend(queue.get())
    return rows

  def write_batch(self, table, rows):
    threads = []
    for i in range(rows):
      thread = WriterThread(self.connection, self.cursor, table, rows[i])
      thread.start()
      threads.append(thread)
    for thread in threads:
      thread.join()
