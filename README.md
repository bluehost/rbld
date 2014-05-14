rbld
======

RBLD is a daemon that reads arbitrary lists of IP addresses as either
blacklists or whitelists.  Clients can connect via Unix Domain Socket
and query for an IP address.

RBLD is most useful for applications that require realtime low-latency
lookups such as webservers, MTAs, and POP3/IMAP servers.
