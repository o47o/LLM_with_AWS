# LLM_with_AWS

## 1. Setting up the work station in AWS.
### Create AWS Account

### Sign in to console
![home_screen](https://github.com/o47o/LLM_with_AWS/assets/142214789/e1737daa-a095-4bec-b2cb-b18d1ec2e06d)

### Change region as per your need, we will be going with Mumbai.
![change_region](https://github.com/o47o/LLM_with_AWS/assets/142214789/842f1fd6-d979-4889-bcac-0d7b7b33d2fa)

### Search for s3 and Create S3 buckets. 
1. Bucket to be created with default settings.
![s3_home_page](https://github.com/o47o/LLM_with_AWS/assets/142214789/229867d2-e939-4e70-9691-1c721018eaa2)

2. Bucket to have same reagion as Mumbai.
![s3_bucket](https://github.com/o47o/LLM_with_AWS/assets/142214789/cdd35303-be43-4ff3-a6e3-bca38e2db4b9)

3. Add files to bucket.
![add_files](https://github.com/o47o/LLM_with_AWS/assets/142214789/71788b97-8bf8-4b94-b308-c50069297a17)


### Search for *Amazon Kendra* and create new index.
1. Create a new role for the index
2. Keep access control as default
3. Once Index is created , add data sources to the index. We will use S3 bucket as our data source.
![add_ds_to_index](https://github.com/o47o/LLM_with_AWS/assets/142214789/cbfeb53b-caf1-4d31-b2c4-f28b6cca96b9)
4. Search for S3 connector.

5. Select the role that we created earlier.
![index_ds_role](https://github.com/o47o/LLM_with_AWS/assets/142214789/cf4db4ed-6ddb-4cdd-9164-cdf579a35caf)
6. Browse for S3 location, *note : If you have not configured the regions correctly , you will not see your S3 buckets. *
7. Select Frequency as ROD.
8. Sync the DS once it is added.

9. You will get an error while sync.
![sync_error](https://github.com/o47o/LLM_with_AWS/assets/142214789/b1348eb6-8a88-4611-9cc8-ed034f2d2afc)

10. Search for IAM on top serach bar.
11. Click on the Policies from left pane and add service to the role we created by editing the policy *** Use Visual For This***.
12. Search for S3 and select GetObject and ListBucket from dropdown.
13. Once all errors are fixed, sync your data source.
![sync_success](https://github.com/o47o/LLM_with_AWS/assets/142214789/ae3d8836-0b45-490a-a2f2-27fa2e3eaba0)


### Search for Sagemaker
1. Click on Studio, and create a new domain.
![sagemaker](https://github.com/o47o/LLM_with_AWS/assets/142214789/5bfaa068-0a95-4fbf-af73-8f0f49416721)

![sagemaker_domain](https://github.com/o47o/LLM_with_AWS/assets/142214789/3c15a4cb-7edd-4a22-bc15-729100d17df2)

2. Launch Studio
<img width="922" alt="image" src="https://github.com/o47o/LLM_with_AWS/assets/142214789/dd7914ae-b717-4cc6-a412-3becc7f5b000">

### Once Sagemaker is up , we can start coading our application.
### To run the application use File>>New>>Termainal to open a terminal and run the python code.

## 2. Architecture
We are building an application using **AWS** services (Kendra, S3 and Bedrock) to have answering capability on the information we provide to the app.
![AWS APP DIAGRAM (1)](https://github.com/o47o/LLM_with_AWS/assets/142214789/a87f9fe0-2628-4caa-97ef-f54429c79fa7)


## 3. Code 
### main.py
We are using **Kendra Services** to index the documents from **S3** buckets and pass these indexs to **LLM Model** , in this case **Bedrock-Anthropic Claude-Instant**.
The user can ask questions based on the docs and application will answer the question on the information from docs. 
**Execute by:** streamlit run ./main.py
![MicrosoftTeams-image](https://github.com/o47o/LLM_with_AWS/assets/142214789/c3bedd61-b4a0-4d0e-9854-17c617cac130)


### retriveCSVContent.py
We are using **Kendra Services** to index structured data in this case a **CSV** file from **S3** buckets and pass these indexs to **LLM Model** , in this case **Bedrock-Anthropic Claude-Instant**.
The user can ask questions based on the docs and application will answer the question on the information from docs. 
**Execute by:** streamlit run ./retriveCSVContent.py

# Observations
Kendra Service is using RAG to index the data for LLM model. We can achive same with vector stores at a **less cost**. Once the kendra indexes are created, user is billed for the service even if the index is not getting refreshed.
Accuracy of the model is not constant, we will have to provide shot prompts to educate the model.
While processing PDFs with text, graph, images and tables, the kendra index is not able to capture the information in graphs and images.
Instead of creating index directly from text we can try to convert doc's pages to images and then convert images to text.
**We can try this in local evn to create a logic and once logic is tested then we can move to cloud as services are expensive in cloud.**

# Requirments
1. pip install boto3
2. pip install python-dotenv
3. pip install streamlit
4. pip install langchain
5. pip install openai
6. create .env file and add OPENAI_API_KEY
