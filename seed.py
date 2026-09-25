from app import app, db, Scholarship


scholarships = [

    Scholarship(
        name="Tata Capital Pankh Scholarship",
        provider="Tata Capital",
        description="Financial assistance for deserving students pursuing higher education.",
        amount="Up to ₹80,000",
        course="Diploma, Degree, B.Tech",
        category="Merit",
        income_limit="Below ₹4,00,000",
        state="All India",
        deadline="30 October 2026",
        application_link="https://www.tatacapital.com/"
    ),

    Scholarship(
        name="Reliance Foundation Scholarship",
        provider="Reliance Foundation",
        description="Scholarship support for undergraduate students pursuing higher education.",
        amount="Up to ₹2,00,000",
        course="B.Tech, Degree",
        category="Merit",
        income_limit="Based on eligibility",
        state="All India",
        deadline="15 November 2026",
        application_link="https://www.reliancefoundation.org/"
    ),

    Scholarship(
        name="LIC Golden Jubilee Scholarship",
        provider="LIC",
        description="Financial support for students from economically weaker sections.",
        amount="Up to ₹40,000 per year",
        course="Degree, Engineering",
        category="Need Based",
        income_limit="Below ₹4,00,000",
        state="All India",
        deadline="30 November 2026",
        application_link="https://licindia.in/"
    ),

    Scholarship(
        name="AICTE Pragati Scholarship",
        provider="AICTE",
        description="Scholarship scheme supporting girl students pursuing technical education.",
        amount="Up to ₹50,000 per year",
        course="Diploma, B.Tech",
        category="Women",
        income_limit="Below ₹8,00,000",
        state="All India",
        deadline="31 December 2026",
        application_link="https://www.aicte-india.org/"
    ),

    Scholarship(
        name="AICTE Saksham Scholarship",
        provider="AICTE",
        description="Financial assistance for specially-abled students pursuing technical education.",
        amount="Up to ₹50,000 per year",
        course="Diploma, B.Tech",
        category="Special Category",
        income_limit="Below ₹8,00,000",
        state="All India",
        deadline="31 December 2026",
        application_link="https://www.aicte-india.org/"
    ),

    Scholarship(
        name="National Scholarship Scheme",
        provider="Government of India",
        description="Government scholarship opportunities for eligible students pursuing higher education.",
        amount="Varies",
        course="Diploma, Degree, B.Tech",
        category="Government",
        income_limit="Varies",
        state="All India",
        deadline="31 December 2026",
        application_link="https://scholarships.gov.in/"
    ),

    Scholarship(
        name="Telangana ePASS Scholarship",
        provider="Government of Telangana",
        description="Financial assistance for eligible students studying in Telangana.",
        amount="Varies",
        course="Diploma, Degree, B.Tech",
        category="Government",
        income_limit="Based on eligibility",
        state="Telangana",
        deadline="31 December 2026",
        application_link="https://telanganaepass.cgg.gov.in/"
    ),

    Scholarship(
        name="Kotak Kanya Scholarship",
        provider="Kotak Education Foundation",
        description="Scholarship for meritorious girl students pursuing professional higher education.",
        amount="Up to ₹1,50,000 per year",
        course="B.Tech, Degree",
        category="Women",
        income_limit="Below ₹6,00,000",
        state="All India",
        deadline="15 October 2026",
        application_link="https://www.kotakeducationfoundation.org/"
    ),

]


with app.app_context():

    db.create_all()

    for scholarship in scholarships:

        db.session.add(scholarship)

    db.session.commit()

    print("Scholarships added successfully!")