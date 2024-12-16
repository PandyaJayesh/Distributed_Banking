from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import os
import random
import threading
import time

# Shared dictionary to store account balances
shared_accounts = {}
counter = {}


# Function to acquire a lock for a given account number
def acquire_lock(account_number):
    # Add this instance to the queue
    with open(f"queue2_files{account_number}.queue", "a") as queue_file:
        queue_file.write("{}\n".format(os.getpid()))

    # Wait until it's this instance's turn to proceed
    while True:
        with open(f"queue2_files{account_number}.queue","r+") as queue_file:
            queue_contents = queue_file.readlines()
            if int(queue_contents[0]) == os.getpid():
                break
            time.sleep(1)

    print("Instance {} is now next in line. Proceeding...".format(os.getpid()))

    


# Function to release a lock for a given account number
def release_lock(account_number):
  with open(f"queue2_files{account_number}.queue", "r+") as queue_file:
      queue_contents = queue_file.readlines()
      del queue_contents[0]
      queue_file.seek(0)
      queue_file.writelines(queue_contents)
      queue_file.truncate()


# Function to update the balance of an account
def update_balance(account_number, new_balance, deposit=0, withdraw=0):
  if random_number<=0.9:
    if account_number in shared_accounts:
      shared_accounts[account_number] = new_balance
      counter[account_number] += 1
      server2_file = f"./servers/server2/data_{account_number}"
      os.makedirs(os.path.dirname(server2_file), exist_ok=True)
      acquire_lock(account_number)
      with open(server2_file, 'a+') as f:
        if deposit==0:
          f.write(f"{account_number}:{shared_accounts[account_number]};withdraw:{withdraw};counter:{counter[account_number]}\n")
        elif withdraw==0:
          f.write(f"{account_number}:{shared_accounts[account_number]};deposit:{deposit};counter:{counter[account_number]}\n")
      release_lock(account_number)
      return "Balance of account {} updated to {}".format(
          account_number, new_balance)
    else:
      return "Account {} does not exist".format(account_number)
  else:
    return "Server is down. Please try again later."


# Function to initialize accounts
def initialize_accounts():
  global shared_accounts
  global counter
  # Create some initial accounts with balances

  try:
     with open("./servers/server2/data_101","r") as f1, open("./servers/server2/data_102","r") as f2, open("./servers/server2/data_103","r") as f3, open("./servers/server2/data_104","r") as f4, open("./servers/server2/data_105","r") as f5:
        try:
          read1=f1.readlines()
          compare1=read1[len(read1)-1].split(":")
          value1_1=int(compare1[1].split(";")[0])
          value1_2=int(compare1[3])
        except:
          value1_1=1000
          value1_2=0
        try:
          read2=f2.readlines()
          compare2=read2[len(read2)-1].split(":")
          value2_1=int(compare2[1].split(";")[0])
          value2_2=int(compare2[3])
        except:
          value2_1=2000
          value2_2=0
        try:
          read3=f3.readlines()
          compare3=read3[len(read3)-1].split(":")
          value3_1=int(compare3[1].split(";")[0])
          value3_2=int(compare3[3])
        except:
          value3_1=500
          value3_2=0
        try:
          read4=f4.readlines()
          compare4=read4[len(read4)-1].split(":")
          value4_1=int(compare4[1].split(";")[0])
          value4_2=int(compare4[3])
        except:
          value4_1=1500
          value4_2=0
        try:
          read5=f5.readlines()
          compare5=read5[len(read5)-1].split(":")
          value5_1=int(compare5[1].split(";")[0])
          value5_2=int(compare5[3])
        except:
          value5_1=3000
          value5_2=0
        
        shared_accounts = {
            101: value1_1,
            102: value2_1,
            103: value3_1,
            104: value4_1,
            105: value5_1,
        }
        counter = {
            101: value1_2,
            102: value2_2,
            103: value3_2,
            104: value4_2,
            105: value5_2,
        }
     
  except:
    shared_accounts = {
        101: 1000,
        102: 2000,
        103: 500,
        104: 1500,
        105: 3000,
    }
    
    counter = {
        101: 0,
        102: 0,
        103: 0,
        104: 0,
        105: 0,
    }
  print("Accounts initialized successfully.")

def recovery():
   while True:
    try:
      for account_number in shared_accounts:
          acquire_lock(account_number)
          with open(f"./servers/server2/data_{account_number}","r+") as f2, open(f"./servers/master_server/data_{account_number}","r") as f1:
            try:
              read1=f1.readlines()
              read2=f2.readlines()
              compare1=read1[len(read1)-1].split(":")
              compare2=read2[len(read2)-1].split(":")
              if(int(compare1[3])>int(compare2[3])):
                f2.writelines(read1[len(read2):])
            except:
              pass
          release_lock(account_number)
    except:
       print("Blunder")
    print("Pinged")
    time.sleep(10)


def live():
  global random_number
  while True:
    random_number = random.random()
    time.sleep(10)




# Function to deposit money into an account
# Function to deposit money into an account
def deposit(account_number, amount):
  if random_number<=0.9:
    if account_number in shared_accounts:
      shared_accounts[account_number] += amount
      
      # Create an XML-RPC proxy for Server 1
      server1_proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")
      # Synchronize balance with the other server
      server1_proxy.update_balance(account_number,shared_accounts[account_number],amount,0)
      counter[account_number] += 1
      master_server_proxy=xmlrpc.client.ServerProxy("http://localhost:8003/")
      master_server_proxy.deposit(account_number,amount,shared_accounts[account_number],counter[account_number])
      server2_file = f"./servers/server2/data_{account_number}"
      os.makedirs(os.path.dirname(server2_file), exist_ok=True)
      acquire_lock(account_number)
      with open(server2_file, 'a+') as f:
        f.write(f"{account_number}:{shared_accounts[account_number]};deposit:{amount};counter:{counter[account_number]}\n")
      release_lock(account_number)
      return "Deposit of {} to account {} successful. New balance: {}".format(
          amount, account_number, shared_accounts[account_number])
    else:
      return "Account {} does not exist".format(account_number)
  else:
    return "Server is down. Please try again later."


# Function to withdraw money from an account
def withdraw(account_number, amount):
    if random_number<=0.9:
      if account_number in shared_accounts:
          if shared_accounts[account_number] >= amount:
              shared_accounts[account_number] -= amount
              server1_proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")
              # Synchronize balance with the other server
              server1_proxy.update_balance(account_number,
                            shared_accounts[account_number],0,amount)
              counter[account_number] += 1
              master_server_proxy = xmlrpc.client.ServerProxy("http://localhost:8003/")
              master_server_proxy.withdraw(account_number,amount,shared_accounts[account_number],counter[account_number])
              server2_file = f"./servers/server2/data_{account_number}"
              os.makedirs(os.path.dirname(server2_file), exist_ok=True)
              acquire_lock(account_number)
              with open(server2_file, 'a+') as f:
                f.write(f"{account_number}:{shared_accounts[account_number]};withdraw:{amount}:counter:{counter[account_number]}\n")
              release_lock(account_number)
              return "Withdrawal of {} from account {} successful. New balance: {}".format(amount, account_number, shared_accounts[account_number])
          else:
              return "Insufficient balance in account {}".format(account_number)
      else:
          return "Account {} does not exist".format(account_number)
    else:
      return "Server is down. Please try again later."

# Function to check balance of an account
def check_balance(account_number):
    if random_number<=0.9:
      if account_number in shared_accounts:
          return "Balance of account {}: {}".format(account_number, shared_accounts[account_number])
      else:
          return "Account {} does not exist".format(account_number)
    else:
      return "Server is down. Please try again later."

# Create a simple XML-RPC server for Server 2
server = SimpleXMLRPCServer(("localhost", 8001))
print("Server 2 listening on port 8001...")

def transfer(account_number_from, account_number_to, amount):
    if random_number<=0.9:
      if account_number_from in shared_accounts and account_number_to in shared_accounts:
          if shared_accounts[account_number_from] >= amount:
              shared_accounts[account_number_from] -= amount
              shared_accounts[account_number_to] += amount
              server1_proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")
              server1_proxy.update_balance(account_number_from,
                                            shared_accounts[account_number_from] ,0,amount)
              server1_proxy.update_balance(account_number_to,
                                          shared_accounts[account_number_to],amount,0)
              counter[account_number_from] += 1
              counter[account_number_to] += 1                           
              master_server_proxy=xmlrpc.client.ServerProxy("http://localhost:8003/")
              master_server_proxy.withdraw(account_number_from,amount,shared_accounts[account_number_from],counter[account_number_from])
              master_server_proxy.deposit(account_number_to,amount,shared_accounts[account_number_to],counter[account_number_to])
              server2_file = f"./servers/server2/data_{account_number_from}"
              os.makedirs(os.path.dirname(server2_file), exist_ok=True)
              acquire_lock(account_number_from)
              with open(server2_file, 'a+') as f:
                f.write(f"{account_number_from}:{shared_accounts[account_number_from]};withdraw:{amount};counter:{counter[account_number_from]}\n")
              release_lock(account_number_from)
              server2_file = f"./servers/server2/data_{account_number_to}"
              os.makedirs(os.path.dirname(server2_file), exist_ok=True)
              acquire_lock(account_number_to)
              with open(server2_file, 'a+') as f:
                f.write(f"{account_number_to}:{shared_accounts[account_number_to]};deposit:{amount};counter:{counter[account_number_to]}\n")
              release_lock(account_number_to)
              return "Transfer of {} from account {} to account {} successful.".format(amount, account_number_from, account_number_to)
          else:
              return "Insufficient balance in account {}".format(account_number_from)
      else:
          return "Account {} or {} does not exist".format(account_number_from, account_number_to)
    else:
      return "Server is down. Please try again later."
    
def statement(account_number):
    if random_number<=0.9:
      if account_number in shared_accounts:
          server2_file = f"./servers/server2/data_{account_number}"
          os.makedirs(os.path.dirname(server2_file), exist_ok=True)
          acquire_lock(account_number)
          with open(server2_file, 'r') as f:
            file_contents=f.read()
          release_lock(account_number)
          return file_contents
      else:
          return "Account {} does not exist".format(account_number)
    else:
      return "Server is down. Please try again later."

# Initialize accounts
initialize_accounts()
myThread1=threading.Thread(target=recovery)
myThread2=threading.Thread(target=live)
myThread1.start()
myThread2.start()

# Register the functions
server.register_function(deposit, "deposit")
server.register_function(withdraw, "withdraw")
server.register_function(check_balance, "check_balance")
# Register the update_balance function
server.register_function(update_balance, "update_balance")
server.register_function(transfer, "transfer")
server.register_function(statement, "statement")

# Run the server
server.serve_forever()
