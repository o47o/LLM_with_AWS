# LLM_with_AWS

### Create AWS Account

### Sign in to console

### Change region to Mumbai

### Search for s3 and Create S3 buckets. 
1. Bucket to be created with default settings.
2. Bucket to have same reagion as Mumbai.
3. Add files to bucket.

### Search for *Amazon Kendra* and create new index.
1. Create a new role for the index
2. Keep access control as default
3. Once Index is created , add data sources to the index. We will use S3 bucket as our data source.
4. Search for S3 connector.
5. Select the role that we created earlier.
6. Browse for S3 location, *note : If you have not configured the regions correctly , you will not see your S3 buckets. *
7. Select Frequency as ROD.
8. Sync the DS once it is added.
9. You will get an error while sync.
10. Search for IAM on top serach bar.
11. Click on the Policies from left pane and add service to the role we created by editing the policy *** Use Visual For This***.
12. Search for S3 and select GetObject and ListBucket from dropdown.

### Search for Sagemaker
1. Click on Studio, abd create a new domain.
2. Launch Studio

# Requirments
1. pip install boto3
2. pip install python-dotenv
3. pip install streamlit
4. pip install langchain
5. pip install openai
6. create .env file and add OPENAI_API_KEY

