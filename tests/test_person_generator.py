from fakedin.person_generator import PersonGenerator


def test_generate_person_fields_and_consistency() -> None:
    generator = PersonGenerator()
    person = generator.generate_person()

    assert person["first_name"]
    assert person["last_name"]
    expected_full_name = f"{person['first_name']} {person['last_name']}"
    assert person["full_name"] == expected_full_name

    email_prefix = (
        f"{person['first_name'].lower()}.{person['last_name'].lower()}@"
    )
    assert person["email"].startswith(email_prefix)

    assert person["location"] == f"{person['city']}, {person['state']}"

    assert 22 <= person["age"] <= 65
    assert 0 <= person["experience_years"] <= min(
        person["age"] - 21,
        40,
    )

    experience_years = person["experience_years"]
    if experience_years < 3:
        expected_level = "Entry-Level"
    elif experience_years < 7:
        expected_level = "Mid-Level"
    elif experience_years < 15:
        expected_level = "Senior"
    else:
        expected_level = "Executive"

    assert person["experience_level"] == expected_level
