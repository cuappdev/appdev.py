from appdev.connectors.mysql_connector import MySQLConnector

def test_mysql():
  TEST_USERNAME = 'TODO'
  TEST_PASSWORD = 'TODO'
  TEST_HOST = 'TODO'
  TEST_DB_NAME = 'TODO'
  connector = MySQLConnector(TEST_USERNAME, TEST_PASSWORD, \
    TEST_HOST, TEST_DB_NAME)
  rows = connector.read_batch('TODO', interval_size=1000)
  print rows

if __name__ == '__main__':
  test_mysql()
