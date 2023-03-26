REQUIRED_VARS = {
    "site_name": "",
    "site_abbreviation": "",
    "site_id": "",
    "ion_model": "",
    "ion_serial_number": "",
    "inet1": {
        "provider": "",
        "download": "",
        "upload": "",
        "category": "",
        "ip_cidr": "",
        "gateway": "",
    },
    "inet2": {
        "provider": "",
        "download": "",
        "upload": "",
        "category": "",
        "ip_cidr": "",
        "gateway": "",
    },
    "dhcp_domain_name": "",
    "snmpv2_community": "",
    "syslog_server": "",
    "service_binding": "",
    "dns_service_profile": "",
    "path_policy": "",
}

TEMPLATES = {
    "1K1C": "site_template_1K1C.j2",
    "1K2C": "site_template_1K2C.j2",
    "2K1C": "site_template_2K1C.j2",
    "2K2C": "site_template_2K2C.j2",
}
