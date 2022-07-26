import requests
import json
from foreign_job.models import ForeignJob, Country, JobSkillOrTitle, Company


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
                   order_by=1,
                   ra_name='',
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
        self._handle_database_jobs(jobs=jobs, for_female=False)

    # Method to get the list of male jobs
    def female_jobs(self):
        jobs = self.__get_jobs(gender='Female')
        self._handle_database_jobs(jobs=jobs, for_female=True)

    # Function to handle database job
    def _handle_database_jobs(self, jobs=None, for_female=False):
        print(f"Started Job for Female -> {for_female}")
        if jobs and 'result' in jobs:
            for j in jobs['result']:
                try:
                    jobs_queryset = ForeignJob.objects.filter(lot_detail_id=j['lotDetailID'])
                    if jobs_queryset.exists():
                        job = jobs_queryset.first()
                        if j['salaryStr'] == job.salary and j['deadLine'] == job.deadline:
                            continue
                        job.salary = j['salaryStr']
                        job.deadline = j['deadLine']
                        job.deadline_date = j['deadLineDate']
                        job.save()
                    else:
                        # For country
                        country_queryset = Country.objects.filter(name__iexact=j['countryName'])
                        country = country_queryset.first() if country_queryset.exists() else None

                        if not country:
                            country = Country.objects.create(name=j['countryName'])

                        # For JobSkillOrTitle
                        job_skill_or_title_queryset = JobSkillOrTitle.objects.filter(title__iexact=j['skillName'])
                        job_skill_or_title = job_skill_or_title_queryset.first() if job_skill_or_title_queryset.exists() else None

                        if not job_skill_or_title:
                            job_skill_or_title = JobSkillOrTitle.objects.create(title=j['skillName'])

                        # For Company
                        company_queryset = Company.objects.filter(name__iexact=j['companyName'])
                        company = company_queryset.first() if company_queryset.exists() else None

                        if not company:
                            company = Company.objects.create(name=j['companyName'])

                        # Finally Creating the job
                        ForeignJob.objects.create(
                            row_total=j['rowTotal'],
                            lot_detail_id=j['lotDetailID'],
                            lot_no=j['lotNo'],
                            skill_or_title=job_skill_or_title,
                            company=company,
                            country=country,
                            salary=j['salaryStr'],
                            currency=j['currency'],
                            deadline=j['deadLine'],
                            deadline_date=j['deadLineDate'],
                            for_female=for_female
                        )
                except Exception as e:
                    print(e)
            print(f'Jobs Completed -> {for_female}')
        else:
            print("Jobs are None")
