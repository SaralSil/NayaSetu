from django.db import models

class OfficialDirectory(models.Model):
    """Directory of West Bengal local administrative offices and portals"""
    OFFICE_TYPE_CHOICES = [
        ('bdo', 'Block Development Officer (BDO)'),
        ('sdo', 'Sub-Divisional Officer (SDO)'),
        ('dm', 'District Magistrate (DM)'),
        ('municipality', 'Municipality / Municipal Corporation'),
        ('duare_sarkar', 'Duare Sarkar Helpdesk'),
        ('cmo_cell', 'CMO Grievance Cell (Didi ke Bolo)'),
        ('prd_portal', 'P&RD Grievance Portal'),
    ]

    office_type = models.CharField(max_length=50, choices=OFFICE_TYPE_CHOICES)
    district = models.CharField(max_length=100)
    block_or_subdivision = models.CharField(max_length=100, blank=True)
    designation = models.CharField(max_length=255, help_text="e.g. To, The Block Development Officer")
    office_address = models.TextField()
    contact_phone = models.CharField(max_length=100, blank=True)
    official_email = models.EmailField(blank=True)
    grievance_portal_url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.designation} - {self.district}"


class GrievanceDraft(models.Model):
    """User-prepared representation/grievance draft"""
    GRIEVANCE_TYPE_CHOICES = [
        ('delay', 'Delay in Benefit Sanction / Disbursal'),
        ('rejection_review', 'Request for Reconsideration / Re-verification'),
        ('dbt_failure', 'Direct Benefit Transfer (DBT) Failure / Missing Installment'),
        ('correction', 'Correction of Personal/Bank Details'),
    ]

    applicant_name = models.CharField(max_length=255)
    contact_phone = models.CharField(max_length=15, blank=True)
    residence_address = models.TextField(blank=True)
    scheme_name = models.CharField(max_length=255)
    application_reference_no = models.CharField(max_length=100, blank=True)
    original_application_date = models.CharField(max_length=50, blank=True)
    
    grievance_type = models.CharField(max_length=50, choices=GRIEVANCE_TYPE_CHOICES)
    addressed_to_office = models.ForeignKey(OfficialDirectory, on_delete=models.SET_NULL, null=True, blank=True)
    language = models.CharField(max_length=10, default='bn') # 'bn' or 'en'
    
    facts_statement = models.TextField()
    generated_letter_text = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Grievance for {self.scheme_name} by {self.applicant_name}"
