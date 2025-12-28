"""Utilities for generating random realistic job data."""

import random
from typing import Any

from faker import Faker


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
