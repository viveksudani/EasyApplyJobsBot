import unittest

from linkedin import Linkedin as JobProcessor
from models import Job, JobCounter


class test_skipping_jobs(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        # This will be executed once for the test class
        self.processor = JobProcessor()

    def setUp(self):
        # This will be executed before each test method
        pass

    def test_blacklisting_jobs(self):
        blacklisted_company_names = ["Crossover", "Jobot", "EPAM Anywhere", "BairesDev"]
        blacklisted_title_names = ["Web Developer"]

        # Creating a job with a blacklisted property
        blacklisted_company_job = Job(company = 'Crossover')
        blacklisted_title_job = Job(title = 'Web Developer')
        regular_job = Job(company = 'Google', title = 'Data Engineer')

        # Checking if the job is blacklisted
        isJobBlacklistedByCompany = self.processor.isJobBlacklisted(
            company = blacklisted_company_job.company, 
            title = blacklisted_company_job.title,
            blacklistedCompanies = blacklisted_company_names,
            blacklistedTitles = blacklisted_title_names)
        
        isJobBlacklistedByTitle = self.processor.isJobBlacklisted(
            company = blacklisted_title_job.company, 
            title = blacklisted_title_job.title,
            blacklistedCompanies = blacklisted_company_names,
            blacklistedTitles = blacklisted_title_names)
        
        isJobNotBlacklisted = self.processor.isJobBlacklisted(
            company = regular_job.company, 
            title = regular_job.title,
            blacklistedCompanies = blacklisted_company_names,
            blacklistedTitles = blacklisted_title_names)

        # Asserting the results
        self.assertTrue(isJobBlacklistedByCompany)
        self.assertTrue(isJobBlacklistedByTitle)
        self.assertFalse(isJobNotBlacklisted)

    
    def test_skipping_application_for_blacklisted_jobs(self):
        jobCounter = JobCounter()

        # Creating a job with a blacklisted property
        job_should_be_blacklisted_company = Job(company = 'Crossover')
        # This is the id of a Job from Crossover
        job_id_should_be_blacklisted_company = "3772904478" 

        # Checking if the job is blacklisted
        isJobBlacklistedByCompany = self.processor.isJobBlacklisted(company = job_should_be_blacklisted_company.company, title = job_should_be_blacklisted_company.title)

        # Asserting the blacklisting results
        self.assertTrue(isJobBlacklistedByCompany)

        # Applying for the job
        jobCounter = self.processor.processJob(
            jobID = job_id_should_be_blacklisted_company, 
            jobCounter = jobCounter)

        # Asserting that the job was skipped
        self.assertEqual(jobCounter.total, 1)
        self.assertEqual(jobCounter.applied, 0)
        self.assertEqual(jobCounter.skipped_blacklisted, 1)


    def test_skipping_application_for_already_applied_jobs(self):
        jobCounter = JobCounter()

        # This is the id of an already applied Job
        job_id_should_be_already_applied = "4087627195"

        # Applying for the job
        jobCounter = self.processor.processJob(
            jobID = job_id_should_be_already_applied, 
            jobCounter = jobCounter)
        
        # Asserting that the job was skipped
        self.assertEqual(jobCounter.total, 1)
        self.assertEqual(jobCounter.applied, 0)
        self.assertEqual(jobCounter.skipped_already_applied, 1)


if __name__ == '__main__':
    unittest.main()
