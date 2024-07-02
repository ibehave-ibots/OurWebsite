### Constructing your consulting report

1. Each session is in a different page (use page breaks).
2. Has the following key words:
    Type: [short, hands]
    Date: str
    Scholar: str
    Topic: str 
    Content: str
3. (Recommended) Copy and paste the topic created with calendly event.
4. (Recommended) You can make content as descriptive as you like. 



### Workflows

#### Download raw reports
```shell
cd workflows/workflow_download
snakemake --cores 1
```

Raw Data Download: The download_from_sciebo rule will check if the raw/ directory exists. If not, it will download the raw reports from Sciebo using ScieboDataDownload.

Timestamp Deletion: The delete_timestamp rule checks for and deletes a timestamp file in the raw/ directory, then logs the download completion time in download.log. Timestamp file is used by snakemake and has no relevance for any of our analysis.

#### Analysis results of consulting reports

```shell
cd workflows/workflow_analysis
snakemake --cores 1
```

Raw Data Download: The download_from_sciebo rule will check if the raw/ directory exists. If not, it will download the raw reports from Sciebo using ScieboDataDownload.

Data Analysis and Upload: The analysis_and_upload_to_sciebo rule processes the downloaded raw data, analyzes it to extract various metrics, and uploads the results back to Sciebo. The analysis results are also logged in analysis.log.
