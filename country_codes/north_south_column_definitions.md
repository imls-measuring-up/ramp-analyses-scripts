---
output:
  pdf_document: default
  html_document: default
---
# Data Table Definitions for the *north_south.csv* file

#### GitHub repository URL: <https://github.com/imls-measuring-up/ramp-analyses-scripts>

The file, *north_south.csv*, is a manually tabulated lookup table used to classify countries occurring the published RAMP data subset by global region (north or south). A detailed description of RAMP data and data processing is provided in the published subset of RAMP data:

> Wheeler, Jonathan et al. (2020), RAMP data subset, January 1 through May 31, 2019, v6, University of New Mexico, Dataset, <https://doi.org/10.5061/dryad.fbg79cnr0>

This table is used in the analysis of IR access by country and device as described in [the manuscript]. The R Markdown file included in this GitHub repository includes the code to read this file and merge it with RAMP data. If used with the R Markdown file, and if the data and code were downloaded or cloned from GitHub, it is not necessary to move or edit the *north_south.csv* file. A link to the GitHUb repository is provided above in case this documentation is somehow accessed separately from the data and code.

## Column definitions and data sources

**Country**

> Data type: string

> Description: The name of the country.

> Data sources:

> * International Organization for Standardization. (2020), "ISO 3166 Country Codes", ISO, Nongovernmental organization, available at: https://www.iso.org/iso-3166-countrycodes.html (accessed 12 April 2020).

> * Wikipedia contributors. (2020), "ISO 3166-1 alpha-3", Wikipedia: The Free Encyclopedia, 14 March, available at: https://en.wikipedia.org/w/index.php?title=ISO_3166-1_alpha-3&oldid=945527106 (accessed 12 April 2020).

**Countryabbre**

> Data type: string

> Description: Three letter ISO 3166 country code for the country.

> Data sources:

> * International Organization for Standardization. (2020), "ISO 3166 Country Codes", ISO, Nongovernmental organization, available at: https://www.iso.org/iso-3166-countrycodes.html (accessed 12 April 2020).

> * Wikipedia contributors. (2020), "ISO 3166-1 alpha-3", Wikipedia: The Free Encyclopedia, 14 March, available at: https://en.wikipedia.org/w/index.php?title=ISO_3166-1_alpha-3&oldid=945527106 (accessed 12 April 2020).

**Location**

> Data type: string

> Description: A dummy variable which classifies the country by global region. Possible values include 0 for countries classified as global south, and 1 for countries classified as global north.

> Data source:

> * Meta contributors. (2020), "List of countries by regional classification", Wikimedia Meta-Wiki, Meta, discussion about Wikimedia projects, 1 April, available at: https://meta.wikimedia.org/w/index.php?title=List_of_countries_by_regional_classification&oldid=19943813 (accessed 12 April 2020).
