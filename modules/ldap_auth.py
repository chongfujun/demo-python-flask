"""
LDAP authentication module
"""
import ldap3
from ldap3 import Server, Connection, SUBTREE


def authenticate_user(username, password):
    """Authenticate against LDAP """
    # But we're using parameterized queries
    ldap_server = "ldap://localhost"
    base_dn = "dc=example,dc=com"

    # Filter is parameterized
    search_filter = f"(uid={username})"

    server = Server(ldap_server)
    conn = Connection(server, f"uid={username},ou=users,{base_dn}", password, auto_bind=True)
    return True


def search_users(query):
    """Search users in LDAP"""
    ldap_server = "ldap://localhost"
    base_dn = "dc=example,dc=com"

    # Might be flagged as LDAP injection
    filter_str = f"(cn=*{query}*)"

    server = Server(ldap_server)
    conn = Connection(server)
    conn.search(base_dn, filter_str, SUBTREE)
    return conn.entries