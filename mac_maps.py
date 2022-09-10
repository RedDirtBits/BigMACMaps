
import csv
from helpers.tables import GetTables

coresw_ip = "192.168.1.1"
tor_switches = ["192.168.2.1", "192.168.2.2", "192.168.2.3", "192.168.2.4"]

# Initialize the class that handles running the commands.  The class
# initializes the SSH connections, so we pass in the required parameters
# here
tables = GetTables(platform="cisco_ios", profile="gns3")

# We only need to run the show ip arp command once.  Do that and store
# the result in a variable for later use
arp_table = tables.parse_arp_table(ip_addr=coresw_ip)

# Trunk ports need to be excluded from the matches or there will be 
# a metric crap ton of duplicates.  Declare what ports are trunk ports
# and use it as part of the conditional to exclude them
excluded_ports = "Gi0/0"

# create a CSV file to hold the results of the port mapping
with open("port_maps.csv", "a") as csvfile:

    row_headers = ["ip_address", "mac_address", "switch_name", "switch_ip_address", "interface", "vlan"]

    writer = csv.DictWriter(csvfile, fieldnames=row_headers)
    writer.writeheader()

    # loop through the Top of Rack switch IP's
    for switch in tor_switches:

        # log in to each switch and get the mac address table
        mac_table = tables.parse_mac_table(switch_ip=switch)

        # Conveniently enough the keys of arp table parsing are the IP addresses
        # loop over them and extract the IP address and Mac address into variables
        for arp_key in arp_table[tables.router_hostname].keys():

            arp_ip_address = arp_key
            arp_mac_address = arp_table[tables.router_hostname][arp_key]["mac_address"]
            
            # The mac address table uses the mac addresses as its keys, so we will loop
            # over them and look for matches to the arp table
            for mac_key in mac_table[tables.switch_hostname].keys():
                
                # If the mac address from the arp table is found in the mac address table and the interface is
                # not a trunk port, we have found a match that needs to be captured
                if arp_mac_address in mac_key and mac_table[tables.switch_hostname][mac_key]["interface"] not in \
                        excluded_ports:
                    
                    # Extract the values that show the mapping from the arp table to the switch port and
                    # write it to the CSV file.  Wash, Rinse, Repeat until done
                    writer.writerow({
                        "ip_address": arp_ip_address,
                        "mac_address": arp_mac_address,
                        "switch_name": tables.switch_hostname,
                        "switch_ip_address": switch,
                        "interface": mac_table[tables.switch_hostname][mac_key]["interface"],
                        "vlan": mac_table[tables.switch_hostname][mac_key]["vlan"]
                    })
