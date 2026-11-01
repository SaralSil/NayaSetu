from django.db import models

class Department(models.Model):
    """West Bengal Government Department"""
    name_en = models.CharField(max_length=255)
    name_bn = models.CharField(max_length=255, blank=True)
    name_hi = models.CharField(max_length=255, blank=True)
    code = models.CharField(max_length=50, unique=True)
    portal_url = models.URLField(blank=True)
    helpline = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['name_en']

    def __str__(self):
        return f"{self.name_en} ({self.code})"


class Scheme(models.Model):
    """West Bengal Welfare Scheme Profile"""
    CATEGORY_CHOICES = [
        ('women', 'Women & Child Development'),
        ('agriculture', 'Agriculture & Farmers'),
        ('education', 'Education & Students'),
        ('social_security', 'Social Security & Pensions'),
        ('tribal_caste', 'Tribal & Backward Classes'),
        ('health', 'Healthcare & Nutrition'),
    ]

    BENEFIT_TYPE_CHOICES = [
        ('monthly_dbt', 'Monthly Direct Benefit Transfer (DBT)'),
        ('annual_grant', 'Annual Financial Assistance'),
        ('one_time', 'One-time Grant'),
        ('insurance', 'Cashless Health / Crop Insurance'),
        ('scholarship', 'Student Scholarship'),
    ]

    slug = models.SlugField(max_length=100, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='schemes')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    
    # Multilingual Names
    name_en = models.CharField(max_length=255)
    name_bn = models.CharField(max_length=255)
    name_hi = models.CharField(max_length=255, blank=True)

    tagline_en = models.CharField(max_length=500, blank=True)
    tagline_bn = models.CharField(max_length=500, blank=True)
    tagline_hi = models.CharField(max_length=500, blank=True)

    description_en = models.TextField(blank=True)
    description_bn = models.TextField(blank=True)
    description_hi = models.TextField(blank=True)

    benefit_type = models.CharField(max_length=50, choices=BENEFIT_TYPE_CHOICES, default='monthly_dbt')
    benefit_amount_text_en = models.CharField(max_length=255, blank=True)
    benefit_amount_text_bn = models.CharField(max_length=255, blank=True)

    application_channels = models.JSONField(
        default=list, 
        help_text="e.g. ['Duare Sarkar Camp', 'BDO Office', 'Online Portal']"
    )
    official_portal_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name_en']

    def __str__(self):
        return f"{self.name_en} ({self.name_bn})"


class SchemeEligibility(models.Model):
    """Eligibility criteria rule definition for a scheme"""
    scheme = models.OneToOneField(Scheme, on_delete=models.CASCADE, related_name='eligibility')
    min_age = models.PositiveIntegerField(null=True, blank=True)
    max_age = models.PositiveIntegerField(null=True, blank=True)
    
    GENDER_CHOICES = [
        ('all', 'All Genders'),
        ('female', 'Female Only'),
        ('male', 'Male Only'),
    ]
    gender_allowed = models.CharField(max_length=20, choices=GENDER_CHOICES, default='all')
    caste_categories = models.JSONField(
        default=list, 
        help_text="List of eligible categories: ['General', 'SC', 'ST', 'OBC-A', 'OBC-B', 'Minority']"
    )
    max_family_income = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    # Specific West Bengal criteria
    requires_single_bank_account = models.BooleanField(default=False, help_text="Lakshmir Bhandar requires single account")
    requires_aadhaar_dbt_linking = models.BooleanField(default=True, help_text="Aadhaar-NPCI DBT linking mandatory")
    requires_swasthya_sathi = models.BooleanField(default=False)
    requires_land_record = models.BooleanField(default=False, help_text="RoR / Porcha for Krishak Bandhu")
    
    rules_summary_en = models.TextField(blank=True)
    rules_summary_bn = models.TextField(blank=True)
    custom_rules = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"Eligibility for {self.scheme.name_en}"


class SchemeDocument(models.Model):
    """Required documents for scheme application"""
    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE, related_name='documents')
    name_en = models.CharField(max_length=255)
    name_bn = models.CharField(max_length=255)
    name_hi = models.CharField(max_length=255, blank=True)
    is_mandatory = models.BooleanField(default=True)
    clarification_en = models.TextField(blank=True, help_text="Specific note, e.g. 'Must be single account, not joint'")
    clarification_bn = models.TextField(blank=True)
    how_to_obtain_en = models.CharField(max_length=500, blank=True)
    how_to_obtain_bn = models.CharField(max_length=500, blank=True)

    class Meta:
        ordering = ['name_en']

    def __str__(self):
        return f"{self.name_en} ({self.scheme.name_en})"


class CommonRejectionReason(models.Model):
    """Catalog of common rejection or delay causes and their remedies"""
    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE, related_name='rejection_reasons', null=True, blank=True)
    code_or_phrase = models.CharField(max_length=255, help_text="Keywords found in status SMS/letter")
    
    title_en = models.CharField(max_length=255)
    title_bn = models.CharField(max_length=255)
    
    explanation_en = models.TextField()
    explanation_bn = models.TextField()
    explanation_hi = models.TextField(blank=True)
    
    remedy_steps_en = models.JSONField(default=list)
    remedy_steps_bn = models.JSONField(default=list)
    responsible_authority = models.CharField(max_length=255, help_text="e.g. Bank Branch Manager, BDO, Duare Sarkar Counter")

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.code_or_phrase} - {self.title_en}"
