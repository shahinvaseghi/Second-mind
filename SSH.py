import paramiko

# Create an SSH connection.
SSH_client = paramiko.SSHClient()


def SSH_Connection(hostname, port, username, password=None):
    """
    Establish an SSH connection.

    hostname: Hostname or IP address.
    port: Port number for SSH (usually 22).
    username: Username for authentication.
    password: Password for password-based authentication (optional).
    private_key_path: Path to the private key file for key-based authentication (optional).
    """

    try:
        # Automatically add the server's host key
        SSH_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # Password-based authentication
        SSH_client.connect(hostname, port, username, password)

        print("SSH connection established successfully!")
        return True
    except Exception as e:
        print(f"Failed to establish SSH connection: {e}")
        return False


def Command(command):
    """
    Send and Receive Commands to the ssh connection.
    """
    try:
        stdin, stdout, stderr = SSH_client.exec_command(command)
        for line in stdout:
            print(line.strip('\n'))
    except Exception as e:
        print(f"Error executing command: {e}")
        print("An Error Occurred! ")


def Close_SSH_Connection():
    """
    Close the SSH connection.
    """
    SSH_client.close()
    print("SSH connection closed.")


if __name__ == "__main__":
    hostname = input('please enter IP or Host name: ')  # Hostname or ip address.
    port = int(input('please enter port: '))  # Port Number for ssh connection.
    username = input('please enter username: ')  # Username for authentication.
    password = input('please enter password: ')  # Password for password-based authentication (optional).
    SSH_Connection(hostname=hostname, port=port, username=username, password=password)