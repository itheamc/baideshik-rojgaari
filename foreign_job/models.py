from django.db import models


# Model for the jobs table
class ForeignJob(models.Model):
    """
    row_total        rowTotal = 56,
    lot_detail_id     lotDetailID = 14910,
    lot_no       lotNo = "245712",
    skill_name       skillName = "Cleaner",
    company_name     companyName = "humble hunter d.o.o",
    country_name     countryName = "Croatia",
    salary       salaryStr = "500.00",
    currency        currency = "HRK",
    deadline        deadLine = "Expired",
    deadline_date        deadLineDate = "3/7/2025 2:00:08 PM"

    """
    row_total = models.IntegerField()
    lot_detail_id = models.IntegerField(unique=True)
    lot_no = models.CharField(max_length=20)
    skill_name = models.CharField(max_length=240)
    company_name = models.CharField(max_length=100)
    country_name = models.CharField(max_length=100)
    salary = models.CharField(max_length=100)
    currency = models.CharField(max_length=20)
    deadline = models.CharField(max_length=100)
    deadline_date = models.CharField(max_length=100)
    for_female = models.BooleanField(default=False)

    def __str__(self):
        return self.lot_no

    # Property for as_dict
    @property
    def as_dict(self):
        return {
            'id': self.id,
            'row_total': self.row_total,
            'lot_detail_id': self.lot_detail_id,
            'lot_no': self.lot_no,
            'skill_name': self.skill_name,
            'company_name': self.company_name,
            'country_name': self.country_name,
            'salary': self.salary,
            'currency': self.currency,
            'deadline': self.deadline,
            'deadline_date': self.deadline_date,
            'for_female': self.for_female
        }

    class Meta:
        verbose_name = 'Foreign Job'
        verbose_name_plural = 'Foreign Jobs'
