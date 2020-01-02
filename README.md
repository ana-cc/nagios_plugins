# check_dns_rrsig

Long description by Analog / Ana C. Custura: [A tiny Nagios plugin to check DNSSEC RRSIG expiry](https://a.custura.eu/post/check-rrsig-nagios/).

## Setting up icinga2

* Copy `check_dns_rrsig.py` to your _PluginDir_ (`/usr/lib/nagios/plugins/` on Debian)
* Copy `commands-dnsrrsig.conf` to your _ConfigDir_`/conf.d` (`/etc/icinga2/conf.d/` on Debian)
  or _IncludeConfDir_`/plugins-contrib.d/` (`/usr/share/icinga2/include/plugins-contrib.d/` on Debian).

Add this to one of your service configs and change:
```
apply Service "dnsrrsig" {
  import "generic-service"

  check_command = "dnsrrsig"
  display_name = "rrsig for example.org"
  vars.dnsrrsig_domain = "example.org"
  vars.dnsrrsig_days_warn = 8
  vars.dnsrrsig_days_critical = 5
  vars.dnsrrsig_server = "ns1.example.net"

  check_interval = 8h
  retry_interval = 30m

  assign where host.name == NodeName
}
```
