from timeit import timeit
import yaml
from redis import Redis
from ruamel.yaml import YAML
import tango
import pdb
import traceback
import time
file_path = "../bliss-conf/tango/Sardana_test.yml"

# Ruamel startup
ruamel_yaml = YAML()
ruamel_yaml.allow_duplicate_keys = True
ruamel_yaml.default_flow_style = False
#file = open(file_path, 'r')
#file_ruamel = ruamel_yaml.load(file)

# YAML startup
#file = open(file_path, 'r')
#file_yaml = yaml.load(file, Loader=yaml.CLoader)

# Redis startup
db = Redis(unix_socket_path='/tmp/redis.sock')

# Tango startup
tango_db = tango.Database("localhost", 10000)

# Bliss startup
bliss_db = tango.Database("localhost", 10001)

# General
#file = open(file_path, 'w')

def run_ruamel():
  file_ruamel['device'][1]['properties']['test_val'] = 54321
  file.seek(0)
  ruamel_yaml.dump(file_ruamel, file)

def run_yaml():
  file_yaml['device'][1]['properties']['test_val'] = 12345
  file_str = yaml.dump(file_yaml, Dumper=yaml.CDumper)
  file.seek(0)
  file.write(file_str)
  file.truncate()

def run_redis():
  db.hset('tango.motor.motctrl01.1', 'Velocity', 12345)
  pass


def run_tango_sql():
  prop = {"magic_val": 123456789 }
  tango_db.put_device_property("Pool/test/1", prop)
  pass
def run_tango_bliss():
  prop = {"magic_val": 987654321 }
  bliss_db.put_device_property("Pool/test/1", prop)
  pass

def run_tango_bliss_create_device():
  # WIP
  dev_info =  tango.DbDevInfo()
  dev_info.name = "motor/motctrl01/150"
  dev_info._class = "Motor"
  dev_info.server =  "Sardana/test"
  bliss_db.add_device(dev_info)
  time.sleep(3)
  prop = { "axis": "150", "id": "150", "ctrl_id":"1", "Instrument_id": "32" }
  bliss_db.put_device_property("motor/motctrl01/150", prop)
  pass


#print("Ruamel = ", timeit(stmt=run_ruamel, number = 100) / 100)
print("create device + bliss", timeit(stmt=run_tango_bliss_create_device, number = 1))
#print("PYYAML = ", timeit(stmt=run_yaml, number = 100) / 100)
#print("Redis = ", timeit(stmt=run_redis, number = 100) / 100)
#print("tango+sql =", timeit(stmt=run_tango_sql, number = 100) / 100)
#print("tango+bliss =", timeit(stmt=run_tango_bliss, number = 100) / 100)

