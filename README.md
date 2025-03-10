# FakedIn

FakedIn is a set of Python utilities for generating realistic (but fake) résumés and job opening descriptions. It uses AI to create detailed, professional content that mimics real-world examples.

## Installation

### Prerequisites

- Python 3.12 or higher
- PDM package manager

### Setup

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/fakedin.git
   cd fakedin
   ```

2. Install dependencies with PDM:

   ```bash
   pdm install
   ```

3. Set up your OpenAI API key:

   ```bash
   echo "OPENAI_API_KEY=your_api_key_here" > .env
   ```

## Usage

FakedIn provides simple Python scripts for generating résumés and job openings.

### Generating Résumés

```bash
# Generate 5 résumés in markdown format
pdm run python generate_resume.py 5

# Generate 3 résumés in PDF format
pdm run python generate_resume.py 3 --format pdf

# Specify an output directory
pdm run python generate_resume.py 2 --output ./my_resumes --format pdf
```

### Generating Job Openings

```bash
# Generate 5 job openings
pdm run python generate_job.py 5

# Specify an output directory
pdm run python generate_job.py 3 --output ./job_listings
```

## Features

- **Résumé Generation**:
  - Randomly generates person details using Faker (names, locations, contact information)
  - Creates detailed, realistic résumés with work experience, education, and skills
  - Supports both Markdown and PDF output formats

- **Job Opening Generation**:
  - Randomly generates job details using Faker (career fields, company names)
  - Creates comprehensive job descriptions with responsibilities and requirements
  - Includes realistic salary ranges and work models (remote/hybrid/on-site)

## Customization

The project leverages the Faker library to generate all random data, including:

- Names (first and last names)
- Locations (cities and states)
- Contact information (email addresses and phone numbers)
- Career fields and job titles
- Company names with industry-specific terminology

You can modify the industry-specific terminology for company names in the `JobGenerator.INDUSTRY_TERMS` dictionary in `fakedin/data_generator.py`.

## Prompt Templates

FakedIn uses the [promptdown](https://github.com/btfranklin/promptdown) library for structured prompt templates. The templates are located in the `fakedin/prompts` directory:

- `resume.prompt.md`: Template for résumé generation
- `job_opening.prompt.md`: Template for job opening generation

You can modify these templates to customize the output. The templates follow the promptdown format with a title, System Message, and Conversation sections formatted in markdown. We use the simplified conversation format (with bold text like `**User:**` to indicate roles) for better readability with our long prompts.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
