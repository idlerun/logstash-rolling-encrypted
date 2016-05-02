Logstash does not currently support rolling file output. The _pipe_ output can be used with a Python script using 
logging support which *does* support rolling files.
As an added bonus, each log message is encrypted.

## Python Logging
The first requirement is a Python script which received logging messages on stdin and logs them to the Python logging facility.

#### [rolling-log.py](https://github.com/idlerun/logstash-rolling-encrypted/blob/master/rolling-log.py)


## Encryption
Encryption is an optional addition to the process. The following script reads messages from stdin, encrypts them, and writes to stdout. The Python Logging script above is agnostic about what it is logging out, so encrypting the content makes no difference there.

Dependencies:

~~~bash
pip3 install pycrypto bitstring
~~~

#### [crypt.py](https://github.com/idlerun/logstash-rolling-encrypted/blob/master/crypt.py)

Each line is independently encrypted with an IV written to the start of the line. This allows rolling logs and commands like head and tail to be used without worrying about breaking the encryption

To decrypt the log output later use the following script:

#### [uncrypt.py](https://github.com/idlerun/logstash-rolling-encrypted/blob/master/uncrypt.py)


## Logstash Config
Logstash is configured to pipe output through the two Python scripts.

In this example the input is setup to be compatible with [logstash-logback-encoder](https://github.com/logstash/logstash-logback-encoder) and [logstash-forwarder](https://github.com/elastic/logstash-forwarder)

#### [logstash.conf](https://github.com/idlerun/logstash-rolling-encrypted/blob/master/logstash.conf)
