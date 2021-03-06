import json
import datetime
from wetland import config
import paho.mqtt.client as mqtt


# sensor name
name = config.cfg.get("wetland", "name")
listenport = config.cfg.getint("wetland", "wetland_port")

# urls to report
host = config.cfg.get("mqtt", "host")
keys_path = config.cfg.get("mqtt", "keys_path")
ca_certs = keys_path + 'ca.crt'
cert_file = keys_path + 'client.crt'
key_file = keys_path + 'client.key'

client = mqtt.Client()
client.tls_set(ca_certs=ca_certs,
               certfile=cert_file,
               keyfile=key_file)
client.connect(host)
client.loop_start()


class plugin(object):
    def __init__(self, server):
        self.server = server
        self.name = config.cfg.get("wetland", "name")
        self.client = client

    def send(self, subject, action, content):
        t = datetime.datetime.utcnow().isoformat()

        if subject == 'wetland' and \
           action in ('login_successful', 'shell command', 'exec command',
                      'direct_request', 'reverse_request', 'download'):
            pass

        elif subject in ('sftpfile', 'sftpserver'):
            pass

        elif subject == 'content' and action in ('pwd',):
            pass

        elif subject == 'upfile':
            pass

        # do not log to server
        else:
            return True

        data = {'timestamp': t, 'src_ip': self.server.hacker_ip,
                'dst_ip': self.server.myip, 'action': action,
                'content': content, 'sensor': self.name,
                'src_port': self.server.hacker_port,
                'dst_port': listenport, 'honeypot': 'wetland'}
        data = json.dumps(data)

        self.client.publish('ck/log/wetland', data, qos=1)
        return True
