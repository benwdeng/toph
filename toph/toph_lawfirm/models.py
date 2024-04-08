from django.db import models
import uuid
import random

def generate_random_number():
    return random.randint(100000000000, 999999999999)


class LawFirmCouncil(models.Model):
    law_firm = models.CharField(max_length=255)
    council = models.CharField(max_length=255)
    council_email = models.CharField(max_length=255, null=True, blank=True)
    council_phone = models.CharField(max_length=255, null=True, blank=True)
    council_address = models.CharField(max_length=255, null=True, blank=True)

class LawFirmCouncilFile(models.Model):
    law_firm_council = models.ForeignKey(LawFirmCouncil, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='law_firm_council_files/')

class Entry(models.Model):
    
    # Define status choices
    STATUS_CHOICES = [
        ('0_costing', 'Costing'),
        ('1_engagement', 'Engagement'),
        ('2_drafting', 'Drafting'),
        ('3_review', 'Review'),
        ('4_signing', 'Signing'),
        ('5_lodgement', 'Lodgement'),
        ('6_closed', 'Closed'),
    ]

    COUNCIL_CHOICES = [
        ('Casey City Council', 'Casey City Council'),
        ('Melbourne City Council', 'Melbourne City Council'),
        ('Port Phillip City Council', 'Port Phillip City Council'),
        ('Baw Baw Shire Council', 'Baw Baw Shire Council'),
        ('Cardinia Shire Council', 'Cardinia Shire Council'),
    ]

    law_firm = models.CharField(max_length=255)
    council = models.CharField(max_length=255, choices=COUNCIL_CHOICES, default='')
    subject_land_address = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='0_costing')
    rdm_num = models.BigIntegerField(default=generate_random_number, unique=True, editable=False)

    def action_required(self):
        for approval in self.approval_set.all():
            for review in approval.review_set.all():
                if review.party.name == "Cardinia Shire Council" and review.status in [None, '']:
                    return "Yes"
        return "No"

class Person(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    rdm_num = models.BigIntegerField(default=generate_random_number, unique=True, editable=False)

class Document(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    document = models.FileField(upload_to='documents/', null=True, blank=True)
    rdm_num = models.BigIntegerField(default=generate_random_number, unique=True, editable=False)

class Party(models.Model):

    ROLE_CHOICES = [
        ('Owner', 'Owner'),
        ('Mortgager', 'Mortgager'),
        ('Caveator', 'Caveator'),
        ('Lawyer', 'Lawyer'),
        ('Council', 'Council')
    ]

    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255, choices=ROLE_CHOICES, default='Owner')
    email = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    rdm_num = models.BigIntegerField(default=generate_random_number, unique=True, editable=False)

class Approval(models.Model):
    OUTCOME_CHOICES = [
        ('Rejected', 'Rejected'),
        ('Approved', 'Approved'),
    ]
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    document = models.FileField(upload_to='approvals/', null=True, blank=True)
    outcome = models.CharField(max_length=255, choices=OUTCOME_CHOICES, null=True, blank=False)
    rdm_num = models.BigIntegerField(default=generate_random_number, unique=True, editable=False)

    @property
    def reviews_count(self):
        return self.review_set.count()

    @property
    def reviewed_count(self):
        return self.review_set.exclude(status__isnull=True).count()

class Review(models.Model):
    STATUS_CHOICES = [
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    approval = models.ForeignKey(Approval, on_delete=models.CASCADE)
    party = models.ForeignKey(Party, on_delete=models.CASCADE, null=True, blank=True)
    date_sent = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    reminder_delay = models.IntegerField(null=True, blank=True)
    reminder_frequency = models.IntegerField(null=True, blank=True)
    date_reviewed = models.DateTimeField(auto_now=True, null=True, blank=True)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='Approved', null=True, blank=False)
    comment = models.TextField()
    document = models.FileField(upload_to='reviews/', null=True, blank=True)
    rdm_num = models.BigIntegerField(default=generate_random_number, unique=True, editable=False)

class Signature(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    document = models.FileField(upload_to='signature/', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    rdm_num = models.BigIntegerField(default=generate_random_number, unique=True, editable=False)

class Signer(models.Model):
    signature = models.ForeignKey(Signature, on_delete=models.CASCADE)
    person = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, null=True)
    rdm_num = models.BigIntegerField(default=generate_random_number, unique=True, editable=False)

class Lodge(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    to = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    dealing_number = models.CharField(max_length=255, null=True, blank=True)
    updated_cert = models.FileField(upload_to='lodge/', null=True, blank=True)
    rdm_num = models.BigIntegerField(default=generate_random_number, unique=True, editable=False)

class LodgeFile(models.Model):
    lodge = models.ForeignKey(Lodge, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='lodge_files/')