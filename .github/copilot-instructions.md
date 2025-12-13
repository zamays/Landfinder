# Copilot Instructions for landFinder

## Project Overview

landFinder is a Python application for scraping real estate websites to enable local data search and analysis. The project helps users aggregate and query property listings from various real estate platforms.

## Development Guidelines

### Python Standards

- Use Python 3.8+ features and syntax
- Follow PEP 8 style guidelines for code formatting
- Use type hints where appropriate for better code clarity
- Write docstrings for all public functions, classes, and modules using Google or NumPy style

### Code Quality

- Keep functions focused and single-purpose
- Use meaningful variable and function names that clearly convey intent
- Handle exceptions appropriately with specific exception types
- Add comments only when the code's purpose isn't immediately clear

### Web Scraping Best Practices

- Always respect robots.txt files and website terms of service
- Implement rate limiting to avoid overwhelming target websites
- Use appropriate user agents and headers
- Handle network errors gracefully with retries and backoff strategies
- Cache responses when appropriate to minimize redundant requests
- Parse HTML/XML content defensively, expecting missing or malformed data

### Data Handling

- Validate and sanitize all scraped data before storage
- Use appropriate data structures for efficient storage and retrieval
- Consider using databases (SQLite, PostgreSQL) for persistent storage
- Implement data versioning or timestamps to track when data was collected

### Dependencies

- Use virtual environments for dependency isolation
- Keep dependencies minimal and well-maintained
- Document any system-level dependencies required
- Pin dependency versions for reproducibility

### Testing

- Write unit tests for data parsing and transformation logic
- Mock external HTTP requests in tests
- Test error handling and edge cases
- Use pytest as the testing framework if not already established

### Security

- Never commit API keys, credentials, or sensitive data
- Use environment variables or secure configuration files for secrets
- Be cautious with user input if the application accepts any
- Follow ethical scraping practices and legal requirements

## Project Structure Conventions

- Keep scraping logic separate from data processing
- Use configuration files for target URLs and scraping parameters
- Organize code by functionality (scrapers, parsers, storage, etc.)
- Maintain clear separation between data collection and data analysis

## Common Tasks

When working on this project, you may need to:

- Add new scrapers for additional real estate websites
- Update existing scrapers when websites change their structure
- Implement data export functionality in various formats (CSV, JSON, etc.)
- Build search and filtering capabilities for local data queries
- Create data visualization or reporting features
