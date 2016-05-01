---
title: "Logstash Rolling Encrypted Logs"
tags: logstash logging encryption
---

Logstash does not currently support rolling file output. The _pipe_ output can be used with a Python script using 
logging support which *does* support rolling files.
As an added bonus, each log message is encrypted.

ENDOFSUMMARY


## Python Logging
The first requirement is a Python script which received logging messages on stdin and logs them to the Python logging facility.

<%= render_code("rolling-log.py", "python") %>


## Encryption
Encryption is an optional addition to the process. The following script reads messages from stdin, encrypts them, and writes to stdout. The Python Logging script above is agnostic about what it is logging out, so encrypting the content makes no difference there.

Dependencies:

~~~bash
pip3 install pycrypto bitstring
~~~

<%= render_code("crypt.py", "python") %>

Each line is independently encrypted with an IV written to the start of the line. This allows rolling logs and commands like head and tail to be used without worrying about breaking the encryption

To decrypt the log output later use the following script:

<%= render_code("uncrypt.py", "python") %>


## Logstash Config
Logstash is configured to pipe output through the two Python scripts.

In this example the input is setup to be compatible with [logstash-logback-encoder](https://github.com/logstash/logstash-logback-encoder) and [logstash-forwarder](https://github.com/elastic/logstash-forwarder)

<%= render_code("logstash.conf", "text") %>
