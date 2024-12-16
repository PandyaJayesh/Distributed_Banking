
# Distributed Banking System

The primary objective of this project is to design, develop, and demonstrate a distributed banking system. The system aims to showcase concepts of distributed computing, including fault tolerance, strong consistency in the very basic functionalities of banking like deposit money, withdraw money, transfer money from one account to another, checking balance and getting statements of the particular account. Along with all these functionalities the whole system is fault tolerant and has locking implementation for avoiding concurrency issues.


## Prerequisites

Python 3.12

Files that one should create before running the below script:
1). create a servers folder \
2). create folders named master_server, server1, server2 inside servers folder.\
3). create files data_101, data_102, data_103, data_104, data_105 inside each folders named master_server, server1, server2 respectively.\


## Running the script

Initialize all the servers: master_server, server1 and server2. Run all of these command in different terminals.
```bash
python3 master_server.py
python3 Server1.py
python3 server2.py
```

Initialize the client:
```bash
python3 client.py
```


## Assumptions

At every 10 seconds each server makes a choice if it will stay live or it will go down for
the next 10 seconds. The probability for a server being down/fail is 10 percent.\
\
Master server never fails in our case.
## Functionalities

Deposit\
Withdraw\
Check balance\
Statement\
Transfer money
## Main Features

Fault Tolerance system\
Locking mechanism for avoiding concurrency issues\
Strong consistency
