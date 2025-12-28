"""Utilities for generating random realistic person data."""

import random
from typing import Any

from faker import Faker

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
            f"{first_name.lower()}.{last_name.lower()}@"
            f"{self.faker.domain_name()}"
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
