### Constructing your consulting report

Every iBOTS team member has one document in our team sciebo consulting reports folder. Name of the document should be the name of the consultant.

Here are some guidelines to make sure that our pipeline can extract all the information from the reports.

## 
1. Each session is in a different page (use page breaks).
2. Has the following key words: </br>
    Type: [short, hands] </br>
    Date: str </br>
    Scholar: str </br>
    Topic: str </br> 
    Content: str </br>
3. (Recommended) Copy and paste the topic created with calendly event.
4. (Recommended) You can make content as descriptive as you like. 

---

### Installation and running the pipeline

1. Setting environment variables.

The pipeline needs credentials to access sciebo folder with consulting reports. Create a file named `.env` and set the environmental variables REPORT_USR and REPORT_PWD. 

2. Installation of packages: Navigate the the path with `environment.yml`.

``` shell
conda env create -f environment.yml
conda activate consulting-analysis
```

This installs all relevant libraries needed to run the pipeline.

3. Run the jupyter notebook titled `consulting_reports_pipeline.ipynb` using `consulting-analysis` kernel.
