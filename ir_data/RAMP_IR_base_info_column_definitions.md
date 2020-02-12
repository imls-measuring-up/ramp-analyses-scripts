# Data Table Definitions for the _RAMP-IR-base-info.csv_ file

The file, _RAMP-IR-base-info.csv_, contains data about RAMP participating IR that were be used to augment RAMP data for the anaylses described in Arlitsch, et al., 2020 (in review). These data were collected manually at the end of May, 2019. Information about index names specific to each IR's RAMP data have been added from an internal RAMP configuration file. These index names allow the data in this file to be cross referenced with RAMP data.

Data were compiled for 35 IR that were registered with RAMP during the period of January 1, 2019 - May 31, 2019. This is a subset of the total number of RAMP participants.

A detailed description of RAMP data and data processing is provided in the published subset of RAMP data:

> Wheeler, Jonathan et al. (2020), RAMP data subset, January 1 through May 31, 2019, v6, University of New Mexico, Dataset, <https://doi.org/10.5061/dryad.fbg79cnr0>

## Column definitions and data sources

**ir_index_root**

> Data type: string

> Description: Each IR in RAMP is assigned two indices in Elasticsearch. These indices are described below, but for each IR both indices have a common prefix or root that is unique to that IR. This field is essentially a unique identifier for IR in RAMP, and is recommended for scripting batch processes across or independently of index type.

> Data source: Internal RAMP IR configuration data.

**ir_page_click_index**

> Data type: string

> Description: Each IR in RAMP has one Elasticsearch index that contains search engine performance data per page or URL. This column provides the names of these indices for each IR. The values can be used to filter RAMP page-click data down to a specific repository, or to batch process page-click data one IR at a time.

> Data source: Internal RAMP IR configuration data.

**ir_access_info_index**

> Data type: string

> Description: Each IR in RAMP has one Elasticsearch index that contains search engine performance data aggregated by combination of country and device. In this case, the country refers to the country from which a search was conducted on a Google property. The device refers to the device that was used to conduct the search. This column provides the names of these indices for each IR. The values can be used to filter RAMP country-device data down to a specific repository, or to batch process country-device data one IR at a time.

> Data source: Internal RAMP IR configuration data.

**Institution**

> Data type: string

> Description: The name(s) of the instution or consortia members operating the IR.

> Data source: These data were collected manually from IR and institutional websites.

**Repository Name**

> Data type: string

> Description: The name of the IR.

> Data source: These data were collected manually from IR and institutional websites.

**URL**

> Data type: string

> Description: The root URL or home page of the IR.

> Data source: Internal RAMP IR configuration data.

**Items in repository on 2019-05-27**

> Data type: integer

> Description: The count of items hosted by the IR. Methods used to count items are identified in the _Item Count Method_ field described below.

> Data source: These data were collected manually from IR and institutional websites.

**Type**

> Data type: string

> Description: The type of organization or institution operating the IR. Current values include _University_ or _Consortium_.

> Data source: These data were collected manually from IR and institutional websites.

**Platform**

> Data type: string

> Description: The IR software platform. 

> Data source: Internal RAMP IR configuration data.

**Item Count Method**

> Data type: string

> Description: The method used to count total items and total ETD in the IR.

**ETD on 2019-06-07**

> Data type: integer

> Description: The count of electronic theses and dissertations in the IR. Null values are represented by a decimal point.

> Data source: These data were collected manually from IR and institutional websites.

**GS site operator 2019-06-07**

> Data type: integer

> Description: The SITE operator can be used with Google search engines to elicit a very rough count of the number items that Google has indexed from a given website or repository. It should not be used to assume anything more than an approximate count. The search command is "site:repository.institution.domain." Null values are represented by a decimal point.

> Example: site.scholarworks.montana.edu

> Data source: These data were collected manually from Google search engines.




