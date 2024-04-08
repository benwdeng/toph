from toph_lawfirm.models import LawFirmCouncil

all_rows = LawFirmCouncil.objects.all()

for row in all_rows:
    print(row.law_firm, row.council, row.council_email)
