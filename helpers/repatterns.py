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


    @staticmethod
    def ieee_mac_address():
        """
        ieee_mac_address summary
            Creates a capture group for IEEE EUI-48 formatted MAC addresses
            i.e. 00-1B-77-49-54-FD

        Returns:
            object: A regular expression capture group
        """
        return re.compile(r"(?P<ieee_mac>^\w+-\w+-\w+-\w+-\w+-\w+$)")

    @staticmethod
    def cisco_mac_address():
        """
        cisco_mac_address summary
            Creates a capture group for Cisco triple hextet formatted MAC addresses
            i.e. 001B.7749.54FD

        Returns:
            object: A regular expression capture group
        """
        return re.compile(r"(?P<cisco_mac>^\w+\.\w+\.\w+$)")

    @staticmethod
    def unix_mac_address():
        """
        unix_mac_address summary
            Creates a capture group for common Unix formatted MAC addresses
            i.e. 00:1B:77:49:54:FD

        Returns:
            object: A regular expression capture group
        """
        return re.compile(r"(?P<unix_mac>^\w+:\w+:\w+:\w+:\w+:\w+$)")
