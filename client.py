import xmlrpc.client
import time
import os
import queue


# Function to acquire a lock for a given account number
def acquire_lock(account_number):
    # Add this instance to the queue
    with open(f"queue_files{account_number}.queue", "a") as queue_file:
        queue_file.write("{}\n".format(os.getpid()))

    # Wait until it's this instance's turn to proceed
    while True:
        with open(f"queue_files{account_number}.queue","r+") as queue_file:
            queue_contents = queue_file.readlines()
            if int(queue_contents[0]) == os.getpid():
                break
            time.sleep(1)

    print("Instance {} is now next in line. Proceeding...".format(os.getpid()))

    


# Function to release a lock for a given account number
def release_lock(account_number):
  with open(f"queue_files{account_number}.queue", "r+") as queue_file:
      queue_contents = queue_file.readlines()
      del queue_contents[0]
      queue_file.seek(0)
      queue_file.writelines(queue_contents)
      queue_file.truncate()


# Function to deposit money into an account
def deposit(account_number, amount, server):
  acquire_lock(account_number)
  try:
    server1_proxy = xmlrpc.client.ServerProxy(f"http://localhost:800{server-1}/")
    print("Executing")
    # time.sleep(20)  #When need to check for failures
    response = server1_proxy.deposit(account_number, amount)
    return response
  except Exception as e:
    # Retry mechanism with exponential backoff
    retries = 3
    delay = 1
    while retries > 0:
      print(f"Deposit failed: {e}. Retrying in {delay} seconds...")
      time.sleep(delay)
      try:
        server1_proxy = xmlrpc.client.ServerProxy(f"http://localhost:800{server-1}/")
        response = server1_proxy.deposit(account_number, amount)
        return response
      except Exception as e:
        retries -= 1
        delay *= 2
    return f"Failed to deposit after retries: {e}"
  finally:
    release_lock(account_number)


# Function to check balance of an account
def check_balance(account_number, server):
  acquire_lock(account_number)
  try:
    server1_proxy = xmlrpc.client.ServerProxy(f"http://localhost:800{server-1}/")
    response = server1_proxy.check_balance(account_number)
    return response
  except Exception as e:
    return f"Failed to check balance: {e}"
  finally:
    release_lock(account_number)

def statement(account_number, server):
  acquire_lock(account_number)
  try:
    server1_proxy = xmlrpc.client.ServerProxy(f"http://localhost:800{server-1}/")
    response = server1_proxy.statement(account_number)
    return response
  except Exception as e:
    return f"Failed to get statement: {e}"
  finally:
    release_lock(account_number)

def withdraw(account_number, amount, server):
  acquire_lock(account_number)
  try:
    server1_proxy = xmlrpc.client.ServerProxy(f"http://localhost:800{server-1}/")
    response = server1_proxy.withdraw(account_number, amount)
    return response
  except Exception as e:
    return f"Failed to withdraw: {e}"
  finally:
    release_lock(account_number)

def transfer(account_number_from, account_number_to, amount, server):
  acquire_lock(account_number_from)
  acquire_lock(account_number_to)
  try:
    server1_proxy = xmlrpc.client.ServerProxy(f"http://localhost:800{server-1}/")
    response = server1_proxy.transfer(account_number_from, account_number_to, amount)
    return response
  except Exception as e:
    return f"Failed to transfer: {e}"
  finally:
    release_lock(account_number_from)
    release_lock(account_number_to)


def main():

  # Account number to deposit to
  account_number = int(input("Enter account number: "))
  #Sever to select
  server = int(input("Enter server to connect to: "))

  while True:
    print("Select from the following:")
    print("1. Deposit")
    print("2. Withdraw")
    print("3. Check Balance")
    print("4. Statement")
    print("5. Money Transfer")
    print("6. Exit")
    choice = int(input("Enter choice: "))

    if choice == 1:
      amount = int(input("Enter amount to deposit: "))
      response = deposit(account_number, amount, server)
      print(response)
    elif choice == 2:
      amount = int(input("Enter amount to withdraw: "))
      response = withdraw(account_number, amount, server)
      print(response)
    elif choice == 3:
      response = check_balance(account_number, server)
      print(response)
    elif choice == 4:
      response = statement(account_number, server)
      print(response)
    elif choice == 5:
      account_number_to = int(input("Enter account number to transfer to: "))
      amount = int(input("Enter amount to transfer: "))
      response = transfer(account_number, account_number_to, amount, server)
      print(response)
    elif choice == 6:
      break


if __name__=="__main__":
  main()

