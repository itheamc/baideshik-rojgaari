import requests
import json
from foreign_job.models import ForeignJob


class JobHandler:
    def __init__(self):
        self.base_url = "https://foreignjob.dofe.gov.np"

    # Method to get the list of jobs
    def __get_jobs(self,
                   offset=1,
                   limit=100000,
                   country='',
                   skill_type='',
                   skill_name='',
                   company_name='',
                   search_text='',
                   salary_from=0,
                   salary_to=0,
                   gender='Male',
                   sort_by='LotNo',
                   order_by=1, ra_name='',
                   interview_venue='',
                   interview_date_from='',
                   interview_date_to=''):
        try:
            payloads = {
                'isSearched': 'true',
                'postdata': json.dumps({
                    'Offset': offset,
                    'Limit': limit,
                    'Country': country,
                    'SkillType': skill_type,
                    'SkillName': skill_name,
                    'CompanyName': company_name,
                    'SearchText': search_text,
                    'SalaryFrom': salary_from,
                    'SalaryTo': salary_to,
                    'Gender': gender,
                    'SortBy': sort_by,
                    'OrderBy': order_by,
                    'RaName': ra_name,
                    'InterviewVenue': interview_venue,
                    'InterviewDateFrom': interview_date_from,
                    'InterviewDateTo': interview_date_to
                })
            }

            jobs_list = requests.post(self.base_url + "/api/LotSearch/GetLotList", data=payloads)
            return jobs_list.json()
        except Exception as e:
            print(e)
            return None

    # Method to get the list of male jobs
    def male_jobs(self):
        jobs = self.__get_jobs(gender='Male')

        if jobs:
            for j in jobs['result']:
                try:
                    if ForeignJob.objects.filter(lot_detail_id=j['lotDetailID']).exists():
                        continue
                    ForeignJob.objects.update_or_create(
                        row_total=j['rowTotal'],
                        lot_detail_id=j['lotDetailID'],
                        lot_no=j['lotNo'],
                        skill_name=j['skillName'],
                        company_name=j['companyName'],
                        country_name=j['countryName'],
                        salary=j['salaryStr'],
                        currency=j['currency'],
                        deadline=j['deadLine'],
                        deadline_date=j['deadLineDate'],
                        for_female=False
                    )
                except Exception as e:
                    print(e)

    # Method to get the list of male jobs
    def female_jobs(self):
        jobs = self.__get_jobs(gender='Female')

        if jobs:
            for j in jobs['result']:
                try:
                    if ForeignJob.objects.filter(lot_detail_id=j['lotDetailID']).exists():
                        continue
                    ForeignJob.objects.update_or_create(
                        row_total=j['rowTotal'],
                        lot_detail_id=j['lotDetailID'],
                        lot_no=j['lotNo'],
                        skill_name=j['skillName'],
                        company_name=j['companyName'],
                        country_name=j['countryName'],
                        salary=j['salaryStr'],
                        currency=j['currency'],
                        deadline=j['deadLine'],
                        deadline_date=j['deadLineDate'],
                        for_female=True
                    )
                except Exception as e:
                    print(e)
