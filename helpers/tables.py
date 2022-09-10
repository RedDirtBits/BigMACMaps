
from collections import defaultdict
from helpers.client import SSHClient
from helpers.ciscocmds import CiscoCommands
from helpers.repatterns import IOSRexPatterns


class GetTables:
    """
     The GetTables class provides methods to log into a network device and run the commands
     show ip arp and show mac address-table.  While they can be used independently if needed
     the ultimate aim is to use the parsed output of the method parse_arp_table with the
     output of the method parse_mac_table to identify the switch ports an IP address on the
     core switch or router appears

     Args:
        platform (str):
            The profile is a prefix for the user provided .env file which is loaded
            and read by the third-party library python-dotenv.  The load_dotenv()
            method is initialized as part of the class init.

            This allows for flexibility for when one may work in different environments
            where SSH login credentials may be different.  For example, testing,
            production, etc.

            This assumes the .env file has been written so that all credentials are written
            in a uniform manner using a uniform prefix to uniquely identify the environment

            Example: testing_username, testing_password, testing_secret

            In this case, the user would set the profile argument to "testing"

        profile (str):
            The Netmiko platform being connected to.  Can be cisco_ios for IOS
            devices, cisco_nxos for Nexus devices, cisco_telnet for when using
            Telnet, etc.
    """

    def __init__(self, platform: str, profile: str) -> None:

        self.platform = platform
        self.profile = profile

        self.cmds = CiscoCommands()
        self.regexes = IOSRexPatterns()

    def parse_arp_table(self, ip_addr: str):
        """
        parse_arp_table summary:
            Logs in to a router or core switch device for the purpose of running the command
            show ip arp and parsing the results

        Args:
            ip_addr (str): The hostname or IP address of the router/core switch

        Returns:
            defaultdict: The parsed output of the show ip arp command
        """

        # initialize the SSH client
        ssh_client = SSHClient(hostname=ip_addr, platform=self.platform, profile=self.profile)

        # log into the router
        ssh_client.ssh_host_login()

        # run the command show ip arp on the router/core switch
        arp_table = ssh_client.session.send_command(self.cmds.show_arp())

        # the hostname of the router/core switch is used as a key in the parsed output
        # that is returned.  Get that from the SSH session and save it to a variable
        self.router_hostname = ssh_client.session.find_prompt()[:-1]

        # initialize the dictionary that will hold the parsed output
        arp_result = defaultdict(dict)

        # loop through the lines of the show ip arp command
        for line in arp_table.strip().splitlines():

            # if there is a regex pattern match assign it to a variable
            arp_match = self.regexes.arp_table().match(line)

            # The arp_match variable will have a value of None until the regex pattern matches
            # if there is a match create dictionary for the key of the switch hostname and set
            # it as the default value
            if arp_match:
                if "ip_address" not in arp_result:
                    arp_result.setdefault(self.router_hostname, {})

                # Extract the values from the regex pattern capture group
                ip_addr = arp_match.groupdict()["ip_address"]
                mac_age = arp_match.groupdict()["age_in_min"]
                mac_addr = arp_match.groupdict()["mac_address"]
                iface = arp_match.groupdict()["interface"]

                # Create a value for the switch host name key that is equal to the
                # mac address extracted and set the value for that key to a dictionary
                arp_result[self.router_hostname][ip_addr] = {}

                # populate the mac address key with the extracted values
                arp_result[self.router_hostname][ip_addr]["age_in_min"] = mac_age
                arp_result[self.router_hostname][ip_addr]["mac_address"] = mac_addr
                arp_result[self.router_hostname][ip_addr]["interface"] = iface

        # log out of the device
        ssh_client.session.disconnect()

        return arp_result

    def parse_mac_table(self, switch_ip: str):
        """
        parse_mac_table summary
            Logs into a switch and runs the command show mac address-table, parses
            the output

        Args:
            switch_ip (str):
                A list of the top of rack switches to in order to retrieve
                the mac-address tables

        Returns:
            defaultdict: The parsed output of the show mac address-table command
        """

        # initialize the SSH client
        ssh_client = SSHClient(hostname=switch_ip, platform=self.platform, profile=self.profile)

        # log into the router
        ssh_client.ssh_host_login()

        mac_table = ssh_client.session.send_command(self.cmds.show_macs(), strip_prompt=True)
        self.switch_hostname = ssh_client.session.find_prompt()[:-1]

        mac_result = defaultdict(dict)

        # loop through the lines of the show ip arp command
        for line in mac_table.strip().splitlines():

            # if there is a pattern match, assign it to a variable
            mac_match = self.regexes.mac_table().match(line)

            # The mac_match variable will have a value of None until the regex pattern matches
            # if there is a match create dictionary for the key of the switch hostname and set
            # it as the default value
            if mac_match:
                if "mac_address" not in mac_result:
                    mac_result.setdefault(self.switch_hostname, {})

                # Extract the values from the regex pattern capture group
                mac_address = mac_match.groupdict()["mac_address"]
                vlan = mac_match.groupdict()["vlan"]
                iface = mac_match.groupdict()["interface"]
                mac_type = mac_match.groupdict()["type"]

                # Create a value for the switch host name key that is equal to the
                # mac address extracted and set the value for that key to a dictionary
                mac_result[self.switch_hostname][mac_address] = {}

                # populate the mac address key with the extracted values
                mac_result[self.switch_hostname][mac_address]["vlan"] = vlan
                mac_result[self.switch_hostname][mac_address]["interface"] = iface
                mac_result[self.switch_hostname][mac_address]["type"] = mac_type

        # Yeah, don't forget to log out
        ssh_client.session.disconnect()

        return mac_result


# router = "192.168.1.1"
# tables = GetTables(platform="cisco_ios", profile="gns3")
# print(tables.parse_arp_table(ip_addr=router))

# switches = ["192.168.2.1", "192.168.2.2"]
# print(tables.parse_mac_table(switches=switches))
