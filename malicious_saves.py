import requests
from pathlib import Path
import magic
from datetime import datetime
import hashlib



def get_req(x,y):
    startTime = datetime.now()
    epoch_time = datetime.now().timestamp()

    url = "123.14.32.31"
    open_port = "34697"
    saved_file = str(epoch_time) + "-" + x + "-" + y + ".malicious"
    filename = Path(str(epoch_time) + "-" + x + "-" + y + ".malicious")
    resp = requests.get('http://' + x + ':' + y)
    filename.write_bytes(resp.content)

    file_type = magic.from_file(saved_file)

    if "ELF 32-bit MSB executable" in file_type:
        return magic.from_file(saved_file)
        with open(saved_file, 'rb') as f:
            data = f.read()
            sha256hash = hashlib.sha256(data).hexdigest().encode('utf-8')
            return "SHA256:", sha256hash

    else:
        pass

    print("Elapsed Time : ", datetime.now() - startTime)


