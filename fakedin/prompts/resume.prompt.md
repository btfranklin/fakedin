# Generate a Realistic Resume

## Developer Message

You are a professional resume writer tasked with creating realistic, detailed resumes for fictional individuals.

## Conversation

**User:**
I need you to generate a realistic, professional resume for a fictional person with the following details:

Full Name: {{ full_name }}
First Name: {{ first_name }}
Last Name: {{ last_name }}
Age: {{ age }}
Email: {{ email }}
Phone: {{ phone_number }}
City: {{ city }}
State: {{ state }}
Full Location: {{ location }}
Career Field: {{ career_field }}
Experience Level: {{ experience_level }} ({{ experience_years }} years of experience)

Please create a detailed, realistic resume that includes:

1. Contact information (use the provided email and phone)
2. Professional summary that references their location ({{ city }}, {{ state }})
3. Work experience with 2-4 previous jobs showing career progression appropriate for their experience level ({{ experience_years }} years)
4. Education (appropriate for the career field and age of {{ age }})
5. Skills (technical and soft skills relevant to {{ career_field }})
6. Optional sections as appropriate (certifications, volunteer work, etc. that would be suitable for someone at the {{ experience_level }} level)

Make sure the resume is realistic with specific, concrete details that demonstrate actual accomplishments and skills. Avoid generic job descriptions. Tailor the overall presentation to someone who is {{ experience_level }} in their field with {{ experience_years }} years of experience.

Format the response in Markdown with appropriate sections and formatting. Do not surround it with triple-ticks (```), just raw Markdown.

Please provide *only* the resume, without any additional preamble or commentary. Your response will be saved directly to a file.
