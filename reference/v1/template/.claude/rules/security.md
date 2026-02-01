# Security Rules

## Core Principles

1. **Defense in depth** — Multiple layers of security controls
2. **Least privilege** — Minimum permissions required
3. **Fail secure** — Errors should deny access, not grant it
4. **Input validation** — Never trust external data
5. **Secrets protection** — Never hardcode, always rotate

---

## OWASP Top 10 Checklist

### A01: Broken Access Control
- [ ] Verify authorization on every request
- [ ] Deny by default
- [ ] Use RBAC or ABAC consistently
- [ ] Log access control failures
- [ ] Rate limit API access

### A02: Cryptographic Failures
- [ ] Use TLS 1.2+ for all data in transit
- [ ] Encrypt sensitive data at rest (AES-256)
- [ ] Use strong password hashing (bcrypt, Argon2)
- [ ] Never store secrets in code
- [ ] Rotate keys and certificates regularly

### A03: Injection
- [ ] Use parameterized queries (never string concatenation)
- [ ] Validate and sanitize all input
- [ ] Use ORM/prepared statements
- [ ] Escape output based on context
- [ ] Use allowlists over denylists

### A04: Insecure Design
- [ ] Threat model before building
- [ ] Use secure design patterns
- [ ] Implement business logic security
- [ ] Use established frameworks
- [ ] Review architecture with security lens

### A05: Security Misconfiguration
- [ ] Harden all environments
- [ ] Disable unnecessary features
- [ ] Use secure defaults
- [ ] Keep dependencies updated
- [ ] Review cloud/container configs

### A06: Vulnerable Components
- [ ] Maintain component inventory
- [ ] Monitor CVE databases
- [ ] Update dependencies promptly
- [ ] Remove unused dependencies
- [ ] Use only trusted sources

### A07: Authentication Failures
- [ ] Implement MFA where possible
- [ ] Use secure session management
- [ ] Prevent credential stuffing
- [ ] Implement account lockout
- [ ] Use secure password policies

### A08: Integrity Failures
- [ ] Verify software/data integrity
- [ ] Use signed commits and packages
- [ ] Secure CI/CD pipelines
- [ ] Validate deserialization
- [ ] Monitor for tampering

### A09: Logging Failures
- [ ] Log security events
- [ ] Don't log sensitive data
- [ ] Protect log integrity
- [ ] Set up alerting
- [ ] Retain logs appropriately

### A10: SSRF
- [ ] Validate and sanitize URLs
- [ ] Use allowlists for external calls
- [ ] Disable redirects or validate destinations
- [ ] Segment network access
- [ ] Don't return raw responses

---

## Authentication Standards

### Password Requirements
```
Minimum length: 12 characters
Require: uppercase, lowercase, number, special character
Block: common passwords, user info patterns
Hash: bcrypt (cost 12+) or Argon2id
```

### Session Management
```
Token: Cryptographically random, 256+ bits
Storage: HttpOnly, Secure, SameSite=Strict cookies
Expiry: 15-30 minutes idle, 8-24 hours absolute
Rotation: New token on privilege change
```

### API Authentication
```
Prefer: OAuth 2.0 + PKCE, API keys for service-to-service
Header: Authorization: Bearer <token>
Never: Credentials in URL parameters
Rate limit: Per-user and per-IP
```

---

## Secrets Management

### Never Commit
```
*.pem, *.key, *.p12, *.pfx
.env, .env.*
*credentials*, *secrets*
**/config/local.*
```

### Storage Hierarchy
1. **Hardware Security Modules** — Highest security
2. **Cloud secrets managers** — AWS Secrets Manager, Azure Key Vault
3. **HashiCorp Vault** — Self-hosted option
4. **Environment variables** — Minimum acceptable
5. **Config files** — Only with encryption at rest

### Rotation Schedule
| Secret Type | Rotation Period |
|------------|-----------------|
| API keys | 90 days |
| Service accounts | 90 days |
| User passwords | On compromise |
| Certificates | Before expiry |
| Encryption keys | 1 year |

---

## Input Validation

### Validation Strategies
```javascript
// Allowlist (preferred)
const VALID_TYPES = ['user', 'admin', 'guest'];
if (!VALID_TYPES.includes(type)) reject();

// Type coercion
const id = parseInt(input, 10);
if (isNaN(id) || id <= 0) reject();

// Pattern matching
const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
if (!EMAIL_REGEX.test(email)) reject();

// Length limits
if (input.length > MAX_LENGTH) reject();
```

### Context-Specific Encoding
| Context | Encoding |
|---------|----------|
| HTML body | HTML entity encode |
| HTML attribute | Attribute encode + quote |
| JavaScript | JS string encode |
| URL parameter | URL encode |
| CSS | CSS encode |
| SQL | Parameterized queries |

---

## Anti-Patterns

### Never Do This
```javascript
// SQL injection vulnerability
const query = `SELECT * FROM users WHERE id = ${userId}`;

// XSS vulnerability
element.innerHTML = userInput;

// Command injection
exec(`ping ${hostname}`);

// Path traversal
const file = fs.readFileSync(`./uploads/${filename}`);

// Hardcoded secrets
const API_KEY = "sk-1234567890abcdef";

// Weak crypto
const hash = md5(password);
```

---

## Security Review Checklist

Before approving code:

- [ ] No secrets in code or config files
- [ ] All inputs validated and sanitized
- [ ] Parameterized queries used
- [ ] Output encoded for context
- [ ] Authentication on protected routes
- [ ] Authorization checked per request
- [ ] Sensitive data encrypted
- [ ] Security logging in place
- [ ] Dependencies up to date
- [ ] Error messages don't leak info
