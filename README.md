# FakedIn
![fakedin social preview](https://raw.githubusercontent.com/btfranklin/fakedin/main/.github/social%20preview/fakedin_social_preview.jpg "FakedIn")

FakedIn is a set of Python utilities for generating realistic (but fake) résumés and job opening descriptions. It uses AI to create detailed, professional content that mimics real-world examples.

## Getting Started

You'll need Python 3.12+ and the PDM package manager.

```bash
pdm install
cp .env.example .env
```

Then set `OPENAI_API_KEY` in `.env`. If you want a specific model, add `OPENAI_MODEL` (defaults to `gpt-5.2`). See the Usage section below for CLI examples.

## Usage

FakedIn provides a CLI for generating resumes and job openings.

### Generating Resumes

```bash
# Generate 5 resumes in markdown format
pdm run fakedin resume 5

# Generate 3 resumes in PDF format
pdm run fakedin resume 3 --format pdf

# Specify an output directory
pdm run fakedin resume 2 --output ./my_resumes --format pdf
```

### Generating Job Openings

```bash
# Generate 5 job openings
pdm run fakedin job 5

# Specify an output directory
pdm run fakedin job 3 --output ./job_listings
```

### Generating Resumes Tailored to Jobs

You can also generate resumes that are specifically tailored to match a particular job description:

```bash
# First generate a job description
pdm run fakedin job 1 --output ./jobs

# Then generate 5 resumes tailored to that job in markdown format
pdm run fakedin resumes-for-job jobs/company_name_career_field_job.md 5

# Generate 3 resumes tailored to the job in PDF format
pdm run fakedin resumes-for-job jobs/company_name_career_field_job.md 3 --format pdf

# Specify an output directory
pdm run fakedin resumes-for-job jobs/company_name_career_field_job.md 2 --output ./applicants --format pdf
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

You can modify the industry-specific terminology for company names in the `JobGenerator.INDUSTRY_TERMS` dictionary in `src/fakedin/job_data_generator.py`.

## Prompt Templates

FakedIn uses the [promptdown](https://github.com/btfranklin/promptdown) library for structured prompt templates. The templates are located in the `src/fakedin/prompts` directory:

- `resume.prompt.md`: Template for résumé generation
- `job_opening.prompt.md`: Template for job opening generation
- `resume_for_job.prompt.md`: Template for generating résumés tailored to specific job descriptions

You can modify these templates to customize the output. The templates follow the promptdown format with a title, System Message, and Conversation sections formatted in markdown. We use the simplified conversation format (with bold text like `**User:**` to indicate roles) for better readability with our long prompts.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
