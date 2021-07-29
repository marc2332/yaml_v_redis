from timeit import timeit
import yaml
from redis import Redis

# YAML startup 
file_path =  '../bliss-conf/tango/Pool_demo1.yml'
file = open(file_path, 'r')
file_yaml = yaml.safe_load(file)
file = open(file_path, 'w')

# Redis startup
db = Redis(unix_socket_path='/tmp/redis.sock')

def run_yaml():
  file_yaml['device'][1]['properties']['test_val'] = 12345
  file_str = yaml.dump(file_yaml)
  file.write(file_str)
  return None

def run_redis():
  db.hset('tango.motor.motctrl01.1', 'Velocity', 12345)
  pass

print("YAML = ", timeit(stmt=run_yaml, number = 150))
print("Redis = ", timeit(stmt=run_redis, number = 150))
