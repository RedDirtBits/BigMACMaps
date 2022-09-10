import re


class IOSRexPatterns:
    """
     Regular Expression patterns for extracting values in the Cisco commands
     show ip arp and show mac address-table
    """

    @staticmethod
    def arp_table():
        """
        arp_table summary
            Creates a capture group for the show ip arp command

        Returns:
            object: A regular expression capture group
        """
        return re.compile(r"^\w+\s+(?P<ip_address>\d+\.\d+\.\d+\.\d+)\s+(?P<age_in_min>(\d+|-))\s+(?P<mac_address>\w+.\w+.\w+)\s+\w+\s+(?P<interface>\S+)")

    @staticmethod
    def mac_table():
        """
        mac_table summary
            Creates a capture group for the show mac address-table command

        Returns:
            object: A regular expression capture group
        """

        # return re.compile(r"^\s+(?P<vlan>\d+)\s+(?P<mac_address>\w+.\w+.\w+)\s+(?P<type>\w+)\s+(?P<interface>\S+)|^Total\D+(?P<total_mac_addresses>\d+)")
        return re.compile(r"^\s+(?P<vlan>\d+)\s+(?P<mac_address>\w+.\w+.\w+)\s+(?P<type>\w+)\s+(?P<interface>\S+)")
    
