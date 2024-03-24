# kalamari-cli



How I would approach building an API:
* Invest time in good software architecture, esp a service layer but also a repository layer.
* ⁠Then build a CLI that hits the service layer, and use it as an admin tool internally.
* ⁠Next, fork the CLI and give it to customers. 
* ⁠Now I don’t need to build a dashboard at all (yay).
* ⁠Don’t add rate limiting until I can’t handle traffic any more.
* ⁠Also, don’t add usage until I need it. Instead, charge a flat monthly rate. Bump the monthly price as high as possible to discover how valuable the product really is. Then compute usage-based prices based on that when I transition to usage pricing.
* ⁠For auth, I would offload it to Auth0. Rolling your own auth is a huge pain and very risky IMO, and auth is the first experience new customers have with the product so I want it to be smooth or they’ll churn instantly.