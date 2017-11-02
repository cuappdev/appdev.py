import redis
import numpy as np


class RedisConn(object):
  """
    RedisConn object creates a connector to an already running Redis instance.
    Parameters:
        name (str): Naming the specific connection
        host (str): The host which we are connecting to. This is typically
                    localhost but could be a specific port pointing to a Redis
                    cluster
        port (int): Port which CLIENTS are using for communication. This is
                    typically kept at 6379.
        db   (int): Optional: This is a querystring index of the Redis instance.

    Example method uses:
    _single_connect(self):
          Returns a single connection that you can execute commands on
          Example:
            redis = RedisConn(...)
            connection = redis._single_connect()
    _connect_pool(self):
          Spawns a connection pool that you can pull connections from
          Example:
            redis = RedisConn(...)
            connection_pool = redis._connection_pool()
            connection = connection_pool.get_connection()
            connection.send_command(*args)
            connection.disconnect()
  """
  def __init__(self, name, host='localhost', port=6379, db=0):
     self.name = name
     self.host = host
     self.port = port
     self.db = db

  def _single_connect(self):
    # Connect to the DB
     return redis.Redis(host=self.host, port=self.port, db=self.db)

  def _connect_pool(self, max_c=None):
    # Connect to the connection pool
    pool = redis.ConnectionPool(host=self.host, port=self.port,
                                db=self.db, max_connections=max_c)
    return redis.Redis(connection_pool=pool).connection_pool

  def dump_matrix(self, conn, key, matrix):
    # Dumping numpy matrix into redis
    assert(isinstance(matrix, np.ndarray)), 'Input must be numpy matrix'
    rows, columns = matrix.shape
    return conn.execute_command( \
    'ml.matrix.set', key, rows, columns, *matrix.flatten())

  def get_matrix(self, conn, key):
    # Getting numpy matrix from redis given key
    result = conn.execute_command( \
    'ml.matrix.get', key)
    n_rows, n_columns, flattened_arr = result[0], result[1], result[2:]
    assert(isinstance(n_rows, long) \
      and isinstance(n_columns, long)), 'Assuming returned Row and Columns'
    return np.array(flattened_arr, dtype="float64").reshape(n_rows, n_columns)