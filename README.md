# ramp-analyses-scripts

The data and code in this repository were used for the analysis and findings reported in 

* Arlitsch, Kenning, Jonathan Wheeler, Minh Thi Ngoc Pham, and Nikolaus Nova
  Parulian. 2020. "An analysis of use and performance data aggregated from 35
  institutional repositories." _Online Information Review_. <https://doi.org/10.1108/OIR-08-2020-0328>

## Verifying the Analysis:

There are two steps to reproduce the results presented and discussed in the manuscript:

1. Generate a summary statistics file. This file is output by a script, *ramp_summary_stats_normalizes_urls.py*, 
which reads in raw page-click data from RAMP and produces summary statistics for IR included in the study. The page-
click data are publicly available from Dryad and must be downloaded the first time the script is run. The script includes
all the code to needed to complete the download automatically. The output
summary stats are cross referenced with some manually collected data included in the file, *RAMP_IR_base_info.csv*. 

Please note that this step is optional, as the GitHUB repository includes the summary statistics file that was used in the
reported analyses, *RAMP_summary_stats_20200907.csv*.

2. Run the R scripts that were developed for the reported analyses. These scripts have been combined into an R Markdown
file also included in the GitHub repository, *RAMP_use_ratio_and_country_device_analyses.Rmd*. The markdown notebook is hard-coded to read the summary statistics file used for the analyses (*RAMP_summary_stats_20200907.csv*). This file is included in the GitHub repository. Update as needed to run the analysis on revised summary data.

Dependencies are documented in the scripts. All Python dependencies are either included as standard libraries or are available from pip. All R dependencies are available from CRAN. Please refer to installation instructions for your distribution or IDE.
