from xmlrpc.server import SimpleXMLRPCServer
import os

# Function to deposit money into an account
def deposit(account_number, deposit, amount, counter):
      master_server_file = f"./servers/master_server/data_{account_number}"
      os.makedirs(os.path.dirname(master_server_file), exist_ok=True)
      with open(master_server_file, 'a+') as f:
        f.write(f"{account_number}:{amount};deposit:{deposit};counter:{counter}\n")
      return "Deposit in master is successful"


# Function to withdraw money from an account
def withdraw(account_number, withdraw, amount, counter):
      master_server_file = f"./servers/master_server/data_{account_number}"
      os.makedirs(os.path.dirname(master_server_file), exist_ok=True)
      with open(master_server_file, 'a+') as f:
        f.write(f"{account_number}:{amount};withdraw:{withdraw};counter:{counter}\n")
      return "Withdraw in master is successful"
    


server = SimpleXMLRPCServer(("localhost",8003))
print("Master Server listening on port 8003...")

server.register_function(deposit, "deposit")
server.register_function(withdraw, "withdraw")


# Run the server
server.serve_forever()
