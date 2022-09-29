# Is 'domain.x' Available?

> IN WHOIS WE TRUST

My cheap way of checking whether a domain is available to be purchased or not (powered by [whois](https://github.com/domainr/whois)).

#### Disclaimer
This package _might not_ be able to check the available for _every_ possible domain TLD, since `whois` does not work with some TLDs. In the future, I might include options to call different APIs (Gandi API, Domainr, etc.).

### Example

```Python
package main

from available.checker import safe_domain

domain := "dreamdomain.io"
available, isBadTld = safe_domain(domain)

if available :
        print("[+] Success!")
        
```

The above example gives whether a domain is valid or not. Otherwise you could also simple check for domain availability

```Python
package main

from available.checker import domain

domain := "dreamdomain.io"
available = domain(domain)

if available :
        print("[+] Success!")
        
```