from tld import get_tld
from dns import resolver
from pythonwhois.net import get_whois_raw as whois
from fingerprints import fprints, fprints_available


def safe_domain(domain):
    available = False
    domain = _set_domain(domain)
    
    tld = get_tld(domain, fix_protocol=True)
    bad_tld = _bad_tld(tld)

    query = _effective_tld_plus_one(domain)

    if not bad_tld:
        available = match(tld, _get_who_is(query))

    return available, bad_tld
    
def _effective_tld_plus_one(domain):
    tld = get_tld(domain, fix_protocol=True)

    tld_parts = tld.split(".")
    domain_parts = domain.split(".")

    if len(tld_parts) < len(domain_parts) :
        return ".".join(domain_parts[len(domain_parts) - len(tld_parts) - 1:])
    else:
        return domain 

def match(tld, who_is_response):
    available = False
    if who_is_response:
        who_is_response = " ".join(who_is_response)
    else:
        return available

    # .ca & .lt have opposite fingerprints
    if tld == "ca" or tld == "lt":
        if  fprints[tld] not in who_is_response:
            available = True

    """ Checks if the .tld is in our fingerprint list
	Then checks if the fingerprint is in the whois
	response data """

    if fprints.get(tld):
        print(fprints[tld])
        if fprints[tld] in who_is_response:
            available = True

    else :
        """ If the .tld isn't in our fingerprint list,
		this is the last resort options to check a
		list of possible responses. """
        for f in fprints_available:
            if f in who_is_response:
                break

    return available

def _get_who_is(doamin):
    try:
        w = whois(doamin)
    except Exception as e:
        print(e)
        return None
    
    return w
    

def _set_domain(domain):
    if "://" in domain:
        domain = domain.split("://")[1]

    if len(domain) > 1 :
        if domain[len(domain)-1:] == ".":
            domain = domain[:len(domain)-1]
    
    return domain.lower()

def _bad_tld(tld):
    try:
        resolver.resolve(tld + '.', 'SOA')
        return False
    except resolver.NXDOMAIN:
        return True


print(safe_domain("dreamdomain.iq"))