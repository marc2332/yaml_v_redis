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
  file_yaml['device'][0]['properties']['test_val'] = 12345
  file_str = yaml.dump(file_yaml)
  file.seek(0)   
  file.write(file_str)
  file.truncate()

def run_redis():
  db.hset('tango.motor.motctrl01.1', 'Velocity', 12345)
  pass

print("YAML = ", timeit(stmt=run_yaml, number = 500))
print("Redis = ", timeit(stmt=run_redis, number = 500))
