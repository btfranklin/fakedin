"""Utilities for generating random realistic data."""

import random
from typing import Any

from faker import Faker

# Load data files
from fakedin.config import settings


def load_data_file(filename: str) -> list[str]:
    """Load data from a file in the data directory."""
    file_path = settings.data_dir / filename
    if not file_path.exists():
        raise FileNotFoundError(f"Data file not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


class PersonGenerator:
    """Generator for random person details."""

    def __init__(self):
        """Initialize the person generator."""
        # Initialize Faker for generating realistic data
        self.faker = Faker("en_US")

    def generate_person(self) -> dict[str, Any]:
        """Generate random details for a person."""
        # Generate name using Faker
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()

        # Generate contact information
        # Create a professional email
        professional_email = (
            f"{first_name.lower()}.{last_name.lower()}@{self.faker.domain_name()}"
        )
        phone_number = self.faker.phone_number()

        # Generate location using Faker - including small towns and cities
        city = self.faker.city()
        state_abbr = self.faker.state_abbr()
        location = f"{city}, {state_abbr}"

        # Generate career field and job title using Faker
        career_field = self.faker.job()

        age = random.randint(22, 65)  # Working age range

        # Randomize experience level based on age
        experience_years = min(
            random.randint(0, age - 21), 40
        )  # Assuming career starts at around 21

        # Determine experience level
        if experience_years < 3:
            experience_level = "Entry-Level"
        elif experience_years < 7:
            experience_level = "Mid-Level"
        elif experience_years < 15:
            experience_level = "Senior"
        else:
            experience_level = "Executive"

        return {
            "first_name": first_name,
            "last_name": last_name,
            "full_name": f"{first_name} {last_name}",
            "email": professional_email,
            "phone_number": phone_number,
            "age": age,
            "city": city,
            "state": state_abbr,
            "location": location,
            "career_field": career_field,
            "experience_years": experience_years,
            "experience_level": experience_level,
        }


class JobGenerator:
    """Generator for random job details."""

    # Industry-specific terminology for company name generation
    INDUSTRY_TERMS = {
        "Tech": [
            "Software",
            "Data",
            "Tech",
            "Digital",
            "Cloud",
            "Cyber",
            "AI",
            "Web",
            "Mobile",
            "Network",
            "Systems",
        ],
        "Finance": [
            "Capital",
            "Financial",
            "Invest",
            "Asset",
            "Wealth",
            "Equity",
            "Fund",
            "Banking",
            "Credit",
            "Tax",
        ],
        "Health": [
            "Health",
            "Medical",
            "Care",
            "Pharma",
            "Bio",
            "Life",
            "Therapy",
            "Wellness",
            "Clinic",
            "Diagnostic",
        ],
        "Business": [
            "Global",
            "Strategic",
            "Solution",
            "Consulting",
            "Service",
            "Management",
            "Enterprise",
            "Business",
            "Corporate",
            "Group",
        ],
        "Energy": [
            "Energy",
            "Solar",
            "Power",
            "Renewable",
            "Sustainable",
            "Green",
            "Electric",
            "Climate",
            "Carbon",
            "Clean",
        ],
        "Retail": [
            "Retail",
            "Consumer",
            "Shop",
            "Store",
            "Market",
            "Brand",
            "Product",
            "Goods",
            "Commerce",
            "Buy",
        ],
        "Manufacturing": [
            "Manufacturing",
            "Industrial",
            "Factory",
            "Production",
            "Assembly",
            "Engineering",
            "Materials",
            "Design",
            "Build",
            "Craft",
        ],
    }

    def __init__(self):
        """Initialize the job generator."""
        # Initialize Faker for generating job data
        self.faker = Faker("en_US")
        self.experience_levels = ["Entry-Level", "Mid-Level", "Senior", "Executive"]
        self.work_models = ["Remote", "Hybrid", "On-Site"]

    def _generate_company_name(self) -> str:
        """Generate a realistic company name using enhanced patterns."""
        company_patterns = [
            # Two word name + suffix
            lambda: f"{self.faker.word().capitalize()} {self.faker.word().capitalize()} {self.faker.company_suffix()}",
            # Last name + industry term + suffix
            lambda: f"{self.faker.last_name()} {random.choice(random.choice(list(self.INDUSTRY_TERMS.values())))} {self.faker.company_suffix()}",
            # Industry term + word + suffix
            lambda: f"{random.choice(random.choice(list(self.INDUSTRY_TERMS.values())))}{self.faker.word().capitalize()} {self.faker.company_suffix()}",
            # Geographic + industry term
            lambda: f"{self.faker.city()} {random.choice(random.choice(list(self.INDUSTRY_TERMS.values())))} {self.faker.company_suffix()}",
            # Standard Faker company
            lambda: self.faker.company(),
        ]

        pattern = random.choice(company_patterns)
        return pattern()

    def generate_job(self) -> dict[str, Any]:
        """Generate random details for a job."""
        company_name = self._generate_company_name()
        career_field = self.faker.job()
        experience_level = random.choice(self.experience_levels)
        work_model = random.choice(self.work_models)

        # Generate salary range based on experience level
        if experience_level == "Entry-Level":
            min_salary = random.randint(40000, 70000)
            max_salary = min_salary + random.randint(10000, 20000)
        elif experience_level == "Mid-Level":
            min_salary = random.randint(70000, 100000)
            max_salary = min_salary + random.randint(15000, 30000)
        elif experience_level == "Senior":
            min_salary = random.randint(100000, 150000)
            max_salary = min_salary + random.randint(20000, 50000)
        else:  # Executive
            min_salary = random.randint(150000, 250000)
            max_salary = min_salary + random.randint(50000, 100000)

        # Format salary range
        min_salary_formatted = f"${min_salary:,}"
        max_salary_formatted = f"${max_salary:,}"
        salary_range = f"{min_salary_formatted} - {max_salary_formatted}"

        return {
            "company_name": company_name,
            "career_field": career_field,
            "experience_level": experience_level,
            "work_model": work_model,
            "salary_range": salary_range,
            "min_salary": min_salary,
            "max_salary": max_salary,
        }
