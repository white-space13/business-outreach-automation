# Business Outreach Automation

A manually triggered Python workflow that creates a review-ready CSV for a company.

## Current scope
- Accepts a company name and website through GitHub Actions.
- Produces a downloadable CSV artifact.
- Does not invent contacts or email addresses.
- Does not scrape gated websites or send email.

## Run on GitHub
1. Open **Actions**.
2. Select **Generate outreach CSV**.
3. Tap **Run workflow** and enter the company name and website.
4. Download the `outreach-csv` artifact when the run completes.

Use only contact data from authorized sources. Review and verify contacts before outreach. Never commit passwords, API keys, or recipient lists.
