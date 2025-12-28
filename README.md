# FakedIn
![fakedin social preview](https://raw.githubusercontent.com/btfranklin/fakedin/main/.github/social%20preview/fakedin_social_preview.jpg "FakedIn")

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

4. Optionally, specify which OpenAI model to use:

   ```bash
   # In your .env file
   OPENAI_MODEL=gpt-4o-mini  # Defaults to gpt-4o if not specified
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

### Generating Résumés Tailored to Jobs

You can also generate résumés that are specifically tailored to match a particular job description:

```bash
# First generate a job description
pdm run python generate_job.py 1 --output ./jobs

# Then generate 5 résumés tailored to that job in markdown format
pdm run python generate_resumes_for_job.py jobs/company_name_career_field_job.md 5

# Generate 3 résumés tailored to the job in PDF format
pdm run python generate_resumes_for_job.py jobs/company_name_career_field_job.md 3 --format pdf

# Specify an output directory
pdm run python generate_resumes_for_job.py jobs/company_name_career_field_job.md 2 --output ./applicants --format pdf
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

- **Tailored Résumé Generation**:
  - Generates résumés specifically customized to match job requirements
  - Highlights skills and experience relevant to the job
  - Creates realistic career trajectories that would qualify candidates for the position

## Customization

The project leverages the Faker library to generate all random data, including:

- Names (first and last names)
- Locations (cities and states)
- Contact information (email addresses and phone numbers)
- Career fields and job titles
- Company names with industry-specific terminology

You can modify the industry-specific terminology for company names in the `JobGenerator.INDUSTRY_TERMS` dictionary in `fakedin/job_data_generator.py`.

## Prompt Templates

FakedIn uses the [promptdown](https://github.com/btfranklin/promptdown) library for structured prompt templates. The templates are located in the `fakedin/prompts` directory:

- `resume.prompt.md`: Template for résumé generation
- `job_opening.prompt.md`: Template for job opening generation
- `resume_for_job.prompt.md`: Template for generating résumés tailored to specific job descriptions

You can modify these templates to customize the output. The templates follow the promptdown format with a title, System Message, and Conversation sections formatted in markdown. We use the simplified conversation format (with bold text like `**User:**` to indicate roles) for better readability with our long prompts.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Technical Features

- All scripts automatically create output directories if they don't exist
- Graceful error handling for all generation and file operations
- Defaults to Markdown format with PDF generation as an option
- Batch generation stops at the first failure
