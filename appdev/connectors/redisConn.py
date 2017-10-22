import redis

# RedisConnection object
class RedisConn(object):

  def __init__(self, name, host='localhost', port=6379, db=0, max_execs=3,
               timeout=10, block_size=256, allslave_number=2):
     self.name = name
     self.host = host
     self.port = port
     self.db = db
     self.max_execs = max_execs
     self.timeout = timeout
     self.block_size = block_size
     self.slave_number = slave_number
     self.redisDb = self._connect_rd()
     # self.rPool = self._connect_pool()
     # self.rServer = self._create_server()

  def _connect_rd(self):
    # Connect to the DB
     return redis.Redis(host=self.host, port=self.port, db=self.db)

  def _connect_pool(self):
    # Connect to the connection pool
    pool = redis.ConnectionPool(host=self.host, port=self.port, db=self.db)
    return redis.Redis(connection_pool=pool)

  def _create_server(self):
    data = {}
    data['server_name'] = self.name
    data['jobs'] = {'max_execs': self.max_execs, 'timeout':self.timeout}
    data['matrix'] = {'block_size': self.block_size}
    data['redis_master'] = {'host':self.host, 'port':self.port, 'db':self.db}
    data['redis_slaves'] = {}
    for c in range(self.slave_number-self.db-1):
      data['redis_slaves']['slave'+str(c)] = \
        {'host':self.host, 'port':self.port, 'db':self.db+c}
    return server.Server(data)
