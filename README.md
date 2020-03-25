# ramp-analyses-scripts


## To Do:

1. Document north_south.csv, add citations to source data referenced in the R markdown.

## Verifying the Analysis:

More info coming soon. But generally there are two steps to reproduce the results presented
and discussed in the manuscript:

1. Generate a summary statistics file. This file is output by a script, *ramp_summary_stats_normalizes_urls.py*, 
which reads in raw page-click data from RAMP and produces summary statistics for IR included in the study. The page-
click data are publicly available from Dryad and must be downloaded the first time the script is run. The script includes
all the code to needed to complete the download automatically. The output
summary stats are cross referenced with some manually collected data included in the file, *RAMP_IR_base_info.csv*. 

Please note that this step is optional, as the GitHUB repository includes the summary statistics file that was used in the
reported analyses, *RAMP_summary_stats_20200109.csv*.

2. Run the R scripts that were developed for the reported analyses. These scripts have been combined into an R Markdown
file also included in the GitHub repository, *RAMP_use_ratio_and_country_device_analyses.Rmd*. The markdown notebook is hard-coded to read the summary statistics file used for the analyses (*RAMP_summary_stats_20200109.csv*). This file is included in the GitHub repository.

Dependencies are documented in the scripts. All Python dependencies are either included as standard libraries or are available from pip. All R dependencies are available from CRAN. Please refer to installation instructions for your distribution or IDE.
