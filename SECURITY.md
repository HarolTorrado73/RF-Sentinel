# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

Report security vulnerabilities via GitHub issues or email security@rf-sentinel.org.

## Security Best Practices

- No hardcoded credentials
- All SDR communication uses validated parameters
- Input sanitization on all API endpoints
- No root privileges required

## Security Analysis

CodeQL scans run on all PRs. Bandit for Python static analysis.