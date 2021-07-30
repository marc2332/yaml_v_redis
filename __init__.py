from timeit import timeit
import yaml
from redis import Redis
from ruamel.yaml import YAML


file_path = "../bliss-conf/tango/Pool_demo1.yml"

# Ruamel startup
ruamel_yaml = YAML()
file = open(file_path, 'r')
file_ruamel = ruamel_yaml.load(file)

# YAML startup 
file = open(file_path, 'r')
file_yaml = yaml.load(file, Loader=yaml.CLoader)

# Redis startup
db = Redis(unix_socket_path='/tmp/redis.sock')

# General
file = open(file_path, 'w')

def run_ruamel():
  file_ruamel['device'][1]['properties']['test_val'] = 54321
  file.seek(0)
  file_str = ruamel_yaml.dump(file_ruamel, file)
   

def run_yaml():
  file_yaml['device'][1]['properties']['test_val'] = 12345
  file_str = yaml.dump(file_yaml, Dumper=yaml.Dumper)
  file.seek(0)
  file.write(file_str)
  file.truncate()

def run_redis():
  db.hset('tango.motor.motctrl01.1', 'Velocity', 12345)
  pass

print("Ruamel = ", timeit(stmt=run_ruamel, number = 500))
print("PYYAML = ", timeit(stmt=run_yaml, number = 500))
print("Redis = ", timeit(stmt=run_redis, number = 500))
