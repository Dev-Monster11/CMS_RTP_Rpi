from pytapo import Tapo
user = 'jewell'
password = 'Jennydog14'
host = 'jewellfamily.ddns.net/stream1'
tapo = Tapo(host, user, password)
print(tapo.getBasicInfo())