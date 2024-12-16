from xmlrpc.server import SimpleXMLRPCServer
import os
import time

# Function to acquire a lock for a given account number
def acquire_lock(account_number):
    # Add this instance to the queue
    with open(f"queue3_files{account_number}.queue", "a") as queue_file:
        queue_file.write("{}\n".format(os.getpid()))

    # Wait until it's this instance's turn to proceed
    while True:
        with open(f"queue3_files{account_number}.queue","r+") as queue_file:
            queue_contents = queue_file.readlines()
            if int(queue_contents[0]) == os.getpid():
                break
            time.sleep(1)

    # print("Instance {} is now next in line. Proceeding...".format(os.getpid()))

    


# Function to release a lock for a given account number
def release_lock(account_number):
  with open(f"queue3_files{account_number}.queue", "r+") as queue_file:
      queue_contents = queue_file.readlines()
      del queue_contents[0]
      queue_file.seek(0)
      queue_file.writelines(queue_contents)
      queue_file.truncate()

# Function to deposit money into an account
def deposit(account_number, deposit, amount, counter):
      master_server_file = f"./servers/master_server/data_{account_number}"
      os.makedirs(os.path.dirname(master_server_file), exist_ok=True)
      acquire_lock(account_number)
      with open(master_server_file, 'a+') as f:
        f.write(f"{account_number}:{amount};deposit:{deposit};counter:{counter}\n")
      release_lock(account_number)
      return "Deposit in master is successful"


# Function to withdraw money from an account
def withdraw(account_number, withdraw, amount, counter):
      master_server_file = f"./servers/master_server/data_{account_number}"
      os.makedirs(os.path.dirname(master_server_file), exist_ok=True)
      acquire_lock(account_number)
      with open(master_server_file, 'a+') as f:
        f.write(f"{account_number}:{amount};withdraw:{withdraw};counter:{counter}\n")
      release_lock(account_number)
      return "Withdraw in master is successful"
    


server = SimpleXMLRPCServer(("localhost",8003))
print("Master Server listening on port 8003...")

server.register_function(deposit, "deposit")
server.register_function(withdraw, "withdraw")


# Run the server
server.serve_forever()
