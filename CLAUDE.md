## Puppeteer Best Practices
- When using puppeteer, YOU ABSOLUTELY UNDER ANY CIRCUMSTANCE MUST use it in headless mode

## Website Deployment
- Website is hosted on Netlify: https://leotrs-website.netlify.app/ (custom domain: leotrs.com)
- Deploys automatically from GitHub when code is pushed to master branch
- SSL/TLS certificate managed automatically by Netlify via Let's Encrypt

## Email Configuration
- Email hosting: Namecheap Private Email ($1.28/month)
- Domain DNS managed through Namecheap
- Gmail configured to send/receive via POP/SMTP from Namecheap servers:
  - POP Server: mail.privateemail.com (port 995, SSL)
  - SMTP Server: mail.privateemail.com (port 587, TLS)

## Domain & DNS
- Domain registered at Namecheap: leotrs.com
- DNS managed through Namecheap BasicDNS
- Website: CNAME records pointing to leotrs-website.netlify.app
- Email: MX records pointing to mx1/mx2.privateemail.com