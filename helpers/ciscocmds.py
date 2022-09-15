class CiscoCommands:
    """
     Static methods for various Cisco device commands
    Returns:
        str: the command to be run
    """

    @staticmethod
    def show_routes():
        return "show ip route"

    @staticmethod
    def show_ifaces():
        return "show ip interface brief"

    @staticmethod
    def show_up_ifaces():
        return "show ip interface brief | i up"

    @staticmethod
    def show_configuration():
        return "show running-config"

    @staticmethod
    def show_vlans():
        return "show vlan"

    @staticmethod
    def show_arp():
        return "show ip arp"
    
    @staticmethod
    def show_macs():
        return "show mac address-table"

    @staticmethod
    def cdp_neighbors():
        return "show cdp neighbors"

    @staticmethod
    def lldp_neighbors():
        return "show lldp neighbors"