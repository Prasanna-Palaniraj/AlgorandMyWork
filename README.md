# AlgorandMyWork
Algorand solution for HackerEarth Hackothon
Idea- 

I took the Open Theme for the hackathon. The goal is to reimagine an existing Web2 application into a Web3 application.  

Project Brief - 

Provide a platform to a worldwide online marketplace for freelance digital services. Every job posted will be treated as a smart contract powered by Algorand. Freelancers can we view the available jobs and select any of the job best fit for their skills. They can ask further questions, refine requirements and finally agree upon the timelines for delivery, efforts and the compensation required for to deliver.  

The job poster will have an option to review the compensation and then once he agrees, the Algos from his wallet be moved into the smart contract itself. And will be locked until the job is completed. Freelancer, once after completing the job, can move for review. Job Poster can review the work done, and once he confirms the Job has been successfully completed, the Algos locked in Smart contract will be released to Freelancer. 

Technology - 

The front end would be a Web and Mobile Flutter application. The application will use the Google cloud and Hive as primary Database.  

Smart contracts written in the Algorand.  

Algorand Dart is used to connect the Flutter application and Algorand application. 

Solution on algorand - 

I used PyTeal to create the solution. 

One contract has been written to accept the Job Postings. The Job posting will have the details of the job sans the Freelancer who will work on it. 

Once freelancer and Job poster accepts the job, the additional details will be entered to the contract. 

The additional includes the payment made into the contract from the job poster. 

On positive scenario, the job approved successfully and the payment will be made to freelancer on approval from job poster. 

Asserts are added to ensure the payment is not made to ay account but only to the freelancer's account. 

How to run -

1. Clone the code

2. Run the sandbox

3. Run the demo_job.py Python file.
