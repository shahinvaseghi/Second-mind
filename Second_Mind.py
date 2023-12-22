import SSH
import os
import time


def Run_App():
    os.system("cls")
    print("SSH Connection\n"
          "--------------------")
    hostname = input('please enter IP or Host name: ')  # Hostname or ip address.
    port = int(input('please enter port: '))  # Port Number for ssh connection.
    username = input('please enter username: ')  # Username for authentication.
    password = input('please enter password: ')  # Password for password-based authentication (optional).
    connection = SSH.SSH_Connection(hostname=hostname, port=port, username=username, password=password)
    time.sleep(3)
    if not connection:  # connection is not valid
        response = input("Do you want to Try again?\n"
                         " (y or n) :")
        if response == "y" or response == "Y" or response == "yes":  # Try again
            Run_App()
        else:
            SSH.Close_SSH_Connection()
    elif connection:  # Run Command function to start configuring
        Run_Command()


def Run_Command():
    key = 1  # if key is 1 the app will be in a loop anf if key is 0 the app will be closed
    os.system("cls")
    SSH.Command("interface/print")  # print all interfaces
    input('Press Enter to continue...')
    while key == 1:
        time.sleep(1)
        os.system("cls")
        print("0| Close the Connection\n"
              "1| Command Line\n"
              "2| Reset the default configuration\n"
              "3| Change system identity\n"
              "4| Set Static IP\n"
              "5| Configure DHCP\n"
              "6| Configure NAT\n"
              "7| Configure DNS-Server\n"
              "8| Setup HomeCPE")
        command = int(input("Choose an option :"))
        if command == 0:  # If user selects 0, the connection will be closed
            SSH.Close_SSH_Connection()  # close the ssh connection
            time.sleep(2)
        elif command == 1:  # If user selects 1, free command line will be opened
            os.system("cls")
            print("COMMAND LINE\n"
                  "Enter 0 to exit"
                  "--------------------")
            os.system("cls")
            print("COMMAND LINE\n"
                  "------------")
            while True:
                command = input('>>>')  # input command
                SSH.Command(command)
                if command == '0':  # if the user enter 0, the command line will be closed
                    Run_Command()
                    break
        elif command == 2:  # If user selects 2,the default config will be reset
            os.system("cls")
            print('RESETTING SYSTEM CONFIGURATION\n'
                  '--------------------')
            SSH.Command("system/reset-configuration no-defaults=yes")  # reset the default config
            SSH.Command("y")
            print("wait few seconds")
            time.sleep(7)
            Run_App()
        elif command == 3:  # If user selects 3,system identity will be changed
            os.system("cls")
            print('CHANGE SYSTEM IDENTITY\n'
                  '--------------------')
            name = input("Name :")  # new identity name
            SSH.Command(f'system/identity/set name={name}')  # set the new name

        elif command == 4:  # If user selects 4,a static ip will be set to an interface
            ip = input("Choose the IP(with subnet mask) :")  # ip address
            interface = input("Choose the Interface(Only The Number) :")  # interface
            SSH.Command(f'ip/address/add address={ip} interface=ether{interface}')  # the command to set the static ip
        elif command == 5:  # If user selects 5,dhcp configuration will be started
            os.system("cls")
            print('CONFIGURING DHCP\n'
                  '------------')
            print("1| DHCP-Client\n"
                  "2| DHCP-Server")
            dhcp = int(input())  # choose between dhcp server and client
            if dhcp == 1:  # if the user selects 1, the dhcp client will be set
                interface = input("Choose the Interface(Only The Number) :")  # the interface to set dhcp client on it
                SSH.Command(f'ip/dhcp-client/add interface=ether{interface} disabled=no')  # set the dhcp client
            elif dhcp == 2:  # if the user selects 2, the dhcp server will be set
                print('Enter the questions empty for default configuration')
                interface = input("Choose the Interface(Only The Number) :")  # interface
                if not interface.strip():  # check if interface is empty or not
                    SSH.Command('interface/bridge/add name=Default-DHCP')
                    SSH.Command('interface/bridge/port/add bridge=Default-DHCP interface=ether2')
                    SSH.Command('interface/bridge/port/add bridge=Default-DHCP interface=ether3')
                    SSH.Command('interface/bridge/port/add bridge=Default-DHCP interface=ether4')
                    SSH.Command('interface/bridge/port/add bridge=Default-DHCP interface=ether5')
                    SSH.Command('interface/bridge/port/add bridge=Default-DHCP interface=wlan1')
                    SSH.Command('interface/bridge/port/add bridge=Default-DHCP interface=wlan2')
                ip_ranges = input("Choose the IP(with subnet mask) :")  # ip address
                if not ip_ranges.strip():  # check ip ranges is empty or not
                    SSH.Command('ip/pool/add name=Default-DHCP ranges=192.168.150.2-192.168.150.254')
                    SSH.Command('ip/address/add address=192.168.150.1 interface=Default-DHCP')
                    SSH.Command('ip/dhcp-server/add address-pool=Default-DHCP interface=Default-DHCP disabled=no')
                else:  # both is empty
                    pool_name = input("Choose a name for your IP-pool :")
                    SSH.Command(f'ip/pool/add name={pool_name} ranges={ip_ranges}')
                    SSH.Command(f'ip/dhcp-server/add address-pool={pool_name} interface=ether{interface} disabled=no')
        elif command == 6:  # If user selects 6,the nat configuration will be started
            os.system("cls")
            interface = input("Choose the Interface(Only The Number) :")
            SSH.Command(f'/ip/firewall/nat/ add chain=srcnat out-interface=ether{interface} action=masquerade')

        elif command == 7:  # If user selects 7,dns configuration will be started
            os.system("cls")
            print('CONFIGURING DNS\n'
                  '------------')
            dns = input("DNS server :")  # dns server
            SSH.Command(f'ip/dns/set servers={dns}')  # set the dns server
        elif command == 8:  # If user selects 8,HomeCPE configuration will be started
            SSH.Command('ip/dhcp-client/add interface=ether1 disabled=no')
            SSH.Command('interface/bridge/add name=HomeCPE-Bridge')
            SSH.Command('interface/bridge/port/add bridge=HomeCPE-Bridge interface=ether2')
            SSH.Command('interface/bridge/port/add bridge=HomeCPE-Bridge interface=ether3')
            SSH.Command('interface/bridge/port/add bridge=HomeCPE-Bridge interface=ether4')
            SSH.Command('interface/bridge/port/add bridge=HomeCPE-Bridge interface=ether5')
            SSH.Command('interface/bridge/port/add bridge=HomeCPE-Bridge interface=wlan1')
            SSH.Command('interface/bridge/port/add bridge=HomeCPE-Bridge interface=wlan2')
            SSH.Command('ip/pool/add name=HomeCPE ranges=192.168.150.2-192.168.150.254')
            SSH.Command('ip/address/add address=192.168.150.1 interface=HomeCPE-Bridge')
            SSH.Command('ip/dhcp-server/add address-pool=HomeCPE interface=HomeCPE-Bridge disabled=no')


if __name__ == "__main__":
    Run_App()
