# Security Policy

GovInnovate AI welcomes responsible security research and reports that help
protect users, public-sector stakeholders, and project data.

## Supported Versions

Security fixes are applied to the latest version of the default branch. Older
commits, forks, and unofficial deployments may not receive security updates.

## Reporting a Vulnerability

Do not disclose suspected vulnerabilities in a public issue, merge request,
discussion, or social channel.

Report vulnerabilities privately using one of these methods:

1. Create a confidential issue in the project's GitLab repository, if that
   option is available.
2. Contact a project maintainer privately through the repository hosting
   platform and request a secure reporting channel.

Include enough information for maintainers to reproduce and assess the issue:

- A clear description of the vulnerability
- Affected component, file, endpoint, or workflow
- Reproduction steps or a minimal proof of concept
- Potential impact and attack conditions
- Suggested mitigation, if known
- Your preferred contact details and disclosure credit preference

Do not include real personal, government, confidential, or production data in a
security report.

## Responsible Disclosure

Reporters are asked to:

- Act in good faith and avoid privacy violations, service disruption, data
  destruction, or unauthorized access beyond what is necessary to demonstrate
  the issue.
- Allow maintainers reasonable time to investigate and release a fix before
  public disclosure.
- Coordinate public disclosure timing and technical details with maintainers.
- Stop testing and notify maintainers immediately if sensitive data is
  encountered.

Maintainers will make a reasonable effort to:

- Acknowledge a complete report within five business days.
- Assess severity, scope, and remediation options.
- Keep the reporter informed of material progress.
- Credit the reporter when requested and appropriate.
- Publish remediation or advisory information after affected users can take
  protective action.

Timelines may vary based on severity, complexity, and maintainer availability.

## Security Scope

Relevant issues include:

- Exposure of secrets, credentials, or sensitive report data
- Unsafe file handling or path traversal
- Injection vulnerabilities
- Authentication or authorization bypasses
- Dependency or configuration vulnerabilities affecting the application
- Unintended disclosure through generated reports, logs, SQLite data, or local
  datasets

General bugs, feature requests, and non-sensitive reliability issues should be
reported through the normal public issue workflow.

## Safe Deployment Practices

The hackathon MVP is designed for local demonstration data. Deployers are
responsible for securing their environment, protecting sensitive datasets,
restricting access, updating dependencies, and validating recommendations
before operational use.

