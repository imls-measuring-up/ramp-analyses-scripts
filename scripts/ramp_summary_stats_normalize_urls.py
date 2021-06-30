"""Generate RAMP IR Use Ratio and Summary Stats for Jan 1 - May 31, 2019

GitHub repository URL: <https://github.com/imls-measuring-up/ramp-analyses-scripts>

This script generates summary statistics of IR search engine performance data
as reported by Google and harvested by the RAMP application. It also cross-
references RAMP data with manually collected data about IR to calculate
the use ratio and other analyses described in 

  Arlitsch, Kenning, Jonathan Wheeler, Minh Thi Ngoc Pham, and Nikolaus Nova
  Parulian. 2020. "An analysis of use and performance data aggregated from 35
  institutional repositories." Online Information Review.
  https://doi.org/10.1108/OIR-08-2020-0328.

Dependencies:

1. Python modules pandas and requests, available from <https://pandas.pydata.org/>
and <https://requests.readthedocs.io/en/master/>. Should be installed
in the Python environment in which this script will be run.

The other imported libraries listed below are all included in the default Python
installation.

2. "RAMP_IR_base_info.csv": This file contains some IR specific configuration data from
RAMP, as well as manually collected data including the count of items in each IR. The data
were collected between May 27 and June 7, 2019. If this script was downloaded or cloned
from the ramp-analysis-scripts GitHub repository at
<https://github.com/imls-measuring-up/ramp-analyses-scripts>, then the "RAMP_IR_base_info.csv"
file should be in the repository's "ir_data" directory. Column definitions for this file
are provided in the "RAMP_IR_base_info_column_definitions.md" file, which is also
included in the GitHub repository and can be found in the "ir_data" directory.

3. RAMP data: A subset of RAMP data for the IR listed in the "RAMP-IR-base-info.csv" file
has been published at Dryad: <https://doi.org/10.5061/dryad.fbg79cnr0>. The data are too
large to be included in the GitHub repository, but the repository includes an empty
directory, 'ramp_data.' The data should be downloaded from Dryad into the 'ramp_data'
directory. Dataset documentation are included in the item record in Dryad. This script
includes the necessary code to download the data into the 'ramp_data' directory - please
be sure to comment out the corresponding lines of code after downloading the data.

This script will output a CSV file, "RAMP_summary_stats_YYYYMMDD.csv," where "YYYYMMDD"
will be the date on which the script is run. Brief output file column definitions are
provided inline below, but additional documentation is provided in the
"RAMP_summary_stats_documentation.md" file included in the GitHub repository, in the
"results" directory.

"""


import pandas as pd

import os

import fnmatch

import re

import requests

from urllib.parse import urlparse

from datetime import date


def make_dspace_html_url(bitstream_url):
    """For DSpace IR, generate a URL for an HTML page that contains a bitstream
       that has a positive click count in RAMP. Basically, this function attempts
       to infer or reverse-engineer the URL of a bitstream's parent HTML page
       using the bitstream's URL. For DSpace IR this requires extracting the item's
       Handle from the bitstream URL and inserting it into an item URL.

    Parameters
    ----------

    bitstream_url:
        The URL of a DSpace bitstream with a positive click count in RAMP.

    Returns
    -------

    An HTML URL:
        The URL of the HTML page ("item") that includes the bitstream.
        
    """
    
    p = urlparse(bitstream_url)

    # Compile a regular expression to find the DSpace handle in the bitstream URL.
    handle = re.compile("\/[0-9\?\.]+\/[0-9][0-9]+")

    # Search the bitstream URL for the UI type.
    xmlui = re.compile('xmlui')
    jspui = re.compile('jspui')
    dspace = re.compile('dspace')
    h = handle.search(p.path)
    x = xmlui.search(p.path)
    j = jspui.search(p.path)
    ds = dspace.search(p.path)

    # Construct and return the item HTML page.
    if h:
        if j:
            return p.scheme + '://' + p.netloc + '/' + 'jspui' + '/' + 'handle' + h.group()
        elif x:
            return p.scheme + '://' + p.netloc + '/' + 'xmlui' + '/' + 'handle' + h.group()
        elif ds:
            return p.scheme + '://' + p.netloc + '/' + 'dspace' + '/' + 'handle' + h.group()
        else:
            return p.scheme + '://' + p.netloc + '/' + 'handle' + h.group()


def make_dspace_item_uri(bitstream_url):
    """For DSpace IR, generate a URI for an HTML page that contains a bitstream
       that has a positive click count in RAMP. Basically, this function attempts
       to infer or reverse-engineer the URL of a bitstream's parent HTML page
       using the bitstream's URL. For DSpace IR this requires extracting the item's
       Handle from the bitstream URL and inserting it into an item URL.

       This is the same function as above, only instead of a URL, this returns
       a unique URI that can be used to deduplicate HTML URLs where both
       http and https protocols are present.

    Parameters
    ----------

    bitstream_url:
        The URL of a DSpace bitstream with a positive click count in RAMP.

    Returns
    -------

    An item URI:
        A locally unique URI of the HTML page ("item") that includes the bitstream.
        
    """
    
    p = urlparse(bitstream_url)

    # Compile a regular expression to find the DSpace handle in the bitstream URL.
    handle = re.compile("\/[0-9\?\.]+\/[0-9][0-9]+")

    # Search the bitstream URL for the UI type.
    xmlui = re.compile('xmlui')
    jspui = re.compile('jspui')
    dspace = re.compile('dspace')
    h = handle.search(p.path)
    x = xmlui.search(p.path)
    j = jspui.search(p.path)
    ds = dspace.search(p.path)

    # Construct and return the item HTML page.
    if h:
        return h.group()

def make_eprints_fedora_html_url(pdf_url):
    """For EPrints and Fedora IR, generate a URL for an HTML page that contains a content file
       that has a positive click count in RAMP. Basically, this function attempts
       to infer or reverse-engineer the URL of a file's parent HTML page
       using the file's URL. For EPrints and Fedora IR this requires extracting the item's
       internal ID number from the content file URL and inserting it into an item URL.
       Note that for EPrints and Fedora IR, RAMP is currently only filtering activity
       on PDF files, and does not filter activity on other content file types.

    Parameters
    ----------

    pdf_url:
        The URL of a PDF URL with a positive click count in RAMP.

    Returns
    -------

    An HTML URL:
        The URL of the HTML page ("item") that includes the PDF URL.
        
    """

    p = urlparse(pdf_url)

    # Compile a regular expression to find the internal ID numberof the item.
    pdf_path = re.compile("\/[0-9][0-9]+")
    pdf_id = pdf_path.search(p.path)

    # Construct and return the item HTML page.
    if pdf_id:
        return p.scheme + '://' + p.netloc + pdf_id.group()


def make_eprints_fedora_item_uri(pdf_url):
    """For EPrints and Fedora IR, generate a URL for an HTML page that contains a content file
       that has a positive click count in RAMP. Basically, this function attempts
       to infer or reverse-engineer the URL of a file's parent HTML page
       using the file's URL. For EPrints and Fedora IR this requires extracting the item's
       internal ID number from the content file URL and inserting it into an item URL.
       Note that for EPrints and Fedora IR, RAMP is currently only filtering activity
       on PDF files, and does not filter activity on other content file types.

       This is the same function as above, only instead of a URL, this returns
       a unique URI that can be used to deduplicate HTML URLs where both
       http and https protocols are present.

    Parameters
    ----------

    pdf_url:
        The URL of a PDF URL with a positive click count in RAMP.

    Returns
    -------

    An item URI:
        A locally unique URI of the HTML page ("item") that includes the PDF URL.
        
    """

    p = urlparse(pdf_url)

    # Compile a regular expression to find the internal ID numberof the item.
    pdf_path = re.compile("\/[0-9][0-9]+")
    pdf_id = pdf_path.search(p.path)

    # Construct and return the item HTML page.
    if pdf_id:
        return pdf_id.group()


def make_fedora_ne_html_url(pdf_url):
    """This function is the same as make_eprints_fedora_html_url,
       but the regular expression is modified to include a
       specific prefix present in all ID numbers.

    Parameters
    ----------

    pdf_url:
        The URL of a PDF URL with a positive click count in RAMP.

    Returns
    -------

    An HTML URL:
        The URL of the HTML page ("item") that includes the PDF URL.
        
    """

    p = urlparse(pdf_url)
    pdf_path = re.compile("\/files\/neu:[a-z0-9]+")
    pdf_id = pdf_path.search(p.path)
    if pdf_id:
        return p.scheme + '://' + p.netloc + pdf_id.group()


def make_fedora_ne_item_uri(pdf_url):
    """This function is the same as make_eprints_fedora_html_url,
       but the regular expression is modified to include a
       specific prefix present in all ID numbers.

       This is the same function as above, only instead of a URL, this returns
       a unique URI that can be used to deduplicate HTML URLs where both
       http and https protocols are present.

    Parameters
    ----------

    pdf_url:
        The URL of a PDF URL with a positive click count in RAMP.

    Returns
    -------

    An item URI:
        A locally unique URI of the HTML page ("item") that includes the PDF URL.
        
    """

    p = urlparse(pdf_url)
    pdf_path = re.compile("\/files\/neu:[a-z0-9]+")
    pdf_id = pdf_path.search(p.path)
    if pdf_id:
        return pdf_id.group()


def make_bepress_oai_url(pdf_url):
    """For BePress Digital Commons IR, generate an OAI-PMH identifier (UID) for an item
       that contains a content file
       that has a positive click count in RAMP. Basically, this function attempts
       to infer or reverse-engineer the OAI-PMH UID of a file's parent HTML page
       using the file's URL. For Digital Commons IR this requires extracting the item's
       'context' and 'article' ID numbers from the content file URL and inserting
       them into an OAI-PMH UID.

    Parameters
    ----------

    pdf_url:
        The URL of a PDF URL with a positive click count in RAMP.

    Returns
    -------

    An OAI-PMH UID:
        A UID that can be used to make an OAI-PMH request for the item that
        contains the content file.
        
    """

    p = urlparse(pdf_url)
    base_url = 'oai:' + p.netloc + ':'
    contextRe = re.compile(r'context=([a-z0-9_\-]*)')
    articleRe = re.compile(r'article=([0-9][0-9][0-9][0-9])')
    contextSearch = contextRe.search(pdf_url)
    articleSearch = articleRe.search(pdf_url)
    if contextSearch:
        if articleSearch:
            context = contextSearch.group().replace('context=', '')
            article = articleSearch.group().replace('article=', '')
            return base_url + str(context) + '-' + str(article)

def make_bepress_item_uri(pdf_url):
    """For BePress Digital Commons IR, generate an OAI-PMH identifier (UID) for an item
       that contains a content file
       that has a positive click count in RAMP. Basically, this function attempts
       to infer or reverse-engineer the OAI-PMH UID of a file's parent HTML page
       using the file's URL. For Digital Commons IR this requires extracting the item's
       'context' and 'article' ID numbers from the content file URL and inserting
       them into an OAI-PMH UID.

       This is the same function as above, only instead of a URL, this returns
       a unique URI that can be used to deduplicate HTML URLs where both
       http and https protocols are present.

    Parameters
    ----------

    pdf_url:
        The URL of a PDF URL with a positive click count in RAMP.

    Returns
    -------

    An OAI-PMH UID:
        A locally unique UID that can be used to make an OAI-PMH request for the item that
        contains the content file.
        
    """

    p = urlparse(pdf_url)
    base_url = 'oai:' + p.netloc + ':'
    contextRe = re.compile(r'context=([a-z0-9_\-]*)')
    articleRe = re.compile(r'article=([0-9][0-9][0-9][0-9])')
    contextSearch = contextRe.search(pdf_url)
    articleSearch = articleRe.search(pdf_url)
    if contextSearch:
        if articleSearch:
            context = contextSearch.group().replace('context=', '')
            article = articleSearch.group().replace('article=', '')
            return base_url + str(context) + '-' + str(article)


def construct_html_urls(ir_data, platform):
    """This is a helper function that takes RAMP data for a single IR
       and passes it to the appropriate function for building the
       HTML URLs of item pages containing content files with positive click
       values in RAMP. 
       

    Parameters
    ----------

    ir_data:
        A pandas data frame containing RAMP data for a single IR.
    platform:
        The IR's software platform.

    Returns
    -------

    ir_data:
        The IR data is returned with two new columns, 'html_url' and
        'unique_item_uri.' For each row,
        this is the URL of the HTML page of the item containing the content
        file URL referenced by the 'url' column in RAMP, and a URI that
        can be used to deduplicate items which are present in the dataset
        with both http and https URLs.
        
    """

    if platform == 'DSpace':
        ir_data['html_url'] = ir_ramp_data['url'].apply(make_dspace_html_url)
        ir_data['unique_item_uri'] = ir_ramp_data['url'].apply(make_dspace_item_uri) 
    if platform == 'EPrints 3':
        ir_data['html_url'] = ir_ramp_data['url'].apply(make_eprints_fedora_html_url)
        ir_data['unique_item_uri'] = ir_ramp_data['url'].apply(make_eprints_fedora_item_uri)
    if platform == 'Fedora/Samvera':
        ir_data['html_url'] = ir_ramp_data['url'].apply(make_fedora_ne_html_url)
        ir_data['unique_item_uri'] = ir_ramp_data['url'].apply(make_fedora_ne_item_uri)
    if platform == 'Fedora':
        ir_data['html_url'] = ir_ramp_data['url'].apply(make_eprints_fedora_html_url)
        ir_data['unique_item_uri'] = ir_ramp_data['url'].apply(make_eprints_fedora_item_uri)
    if platform == 'Digital Commons':
        ir_data['html_url'] = ir_ramp_data['url'].apply(make_bepress_oai_url)
        ir_data['unique_item_uri'] = ir_ramp_data['url'].apply(make_bepress_item_uri)
    return ir_data

# Set paths to data and output directories. Update as needed.
data_dir = '../ir_data/'
ramp_data_dir = '../ramp_data/'
results_dir = '../results/'

# Get today's date for the output filename.
today = date.today()
fname_date = today.strftime("%Y%m%d")

# Download the January - May 2019 RAMP data subset from Dryad.
# This only needs to be done the first time the analysis is run.
# Please comment out lines 278-282 as needed following download.

# These are the file URLs.
ramp_201901_ai = 'https://datadryad.org/stash/downloads/file_stream/237857'
ramp_201901_pc = 'https://datadryad.org/stash/downloads/file_stream/237862'
ramp_201902_ai = 'https://datadryad.org/stash/downloads/file_stream/237856'
ramp_201902_pc = 'https://datadryad.org/stash/downloads/file_stream/237861'
ramp_201903_ai = 'https://datadryad.org/stash/downloads/file_stream/237858'
ramp_201903_pc = 'https://datadryad.org/stash/downloads/file_stream/237863'
ramp_201904_ai = 'https://datadryad.org/stash/downloads/file_stream/237859'
ramp_201904_pc = 'https://datadryad.org/stash/downloads/file_stream/237864'
ramp_201905_ai = 'https://datadryad.org/stash/downloads/file_stream/237860'
ramp_201905_pc = 'https://datadryad.org/stash/downloads/file_stream/237865'

# Build a dictionary to match filenames with corresponding file URLs.
ramp_subset = {}
ramp_subset['2019-01_RAMP_subset_country-device-info.csv'] = ramp_201901_ai
ramp_subset['2019-01_RAMP_subset_page-clicks_v2.csv'] = ramp_201901_pc
ramp_subset['2019-02_RAMP_subset_country-device-info.csv'] = ramp_201902_ai
ramp_subset['2019-02_RAMP_subset_page-clicks_v2.csv'] = ramp_201902_pc
ramp_subset['2019-03_RAMP_subset_country-device-info.csv'] = ramp_201903_ai
ramp_subset['2019-03_RAMP_subset_page-clicks_v2.csv'] = ramp_201903_pc
ramp_subset['2019-04_RAMP_subset_country-device-info.csv'] = ramp_201904_ai
ramp_subset['2019-04_RAMP_subset_page-clicks_v2.csv'] = ramp_201904_pc
ramp_subset['2019-05_RAMP_subset_country-device-info.csv'] = ramp_201905_ai
ramp_subset['2019-05_RAMP_subset_page-clicks_v2.csv'] = ramp_201905_pc

# Download the data and save to the 'ramp_data' directory.
for file_name, file_pointer in ramp_subset.items():
    r = requests.get(file_pointer, stream=True)
    with open(ramp_data_dir + file_name, 'wb') as dl:
        for chunk in r.iter_content(chunk_size=512):
            dl.write(chunk)

# Create a list to hold the names of individual RAMP data files.
# Note that only page-click data are being used here.
click_data_files = []
for r, d, n in os.walk(ramp_data_dir):
    for f in n:
        if fnmatch.fnmatch(f, '*page-clicks*'):
            fname = os.path.join(r, f)
            click_data_files.append(fname)

# Read the first RAMP data file. 
ramp_data = pd.read_csv(click_data_files[0])

# Read the other RAMP data files. Since these files are large and can take
# some time to load, the next two lines can be commented out to run the rest
# of this script on one file for testing and debugging purposes.
for f in click_data_files[1:]:
    ramp_data = ramp_data.append(pd.read_csv(f))

# Read the file with the manually collected data about IR size, platform,
# country, etc.
ir_info = pd.read_csv(data_dir + 'RAMP_IR_base_info.csv')

# Define the columns that for the output data frame and file.
# More detailed column definitions are included in the file
# "RAMP_summary_stats_documentation.md."
cols = ['ir',                                            # ir_index_root
        'pc_index',                                      # ir_page_click_index
        'ai_index',                                      # ir_access_info_index
        'inst',                                          # Institution
        'repoName',                                      # Repository Name
        'rURL',                                          # URL
        'countItems',                                    # Items in repository on 2019-05-27
        'countCcdUrls',                                  # COUNT unique CC URLs Jan1 to May31 2019
        'countItemUrls',                                 # COUNT undeduplicated (including both http & https of a single URL) ITEM URLs in RAMP Jan1 to May31
        'countItemUris',                                 # COUNT unique (deduplicated) ITEM URLS and/or OAI identifiers
        'useRatio',                                      # Use Ratio (COUNT unique ITEM URIS in RAMP/ COUNT items in IR)
        'sumCcd',                                        # SUM of CCD in full dataset
        'ccdAggSum',                                     # SUM of clicks on unique CC urls (should equal sumCcd)
        'ccdAggCount',                                   # COUNT of unique CC urls (should equal countCcdUrls)
        'ccdAggMean',                                    # Average clicks per CC url
        'ccdAggStd',                                     # Standard deviation of clicks on CC urls
        'ccdAggMin',                                     # Minimum number of clicks on CC urls
        'ccdAgg25',                                      # First quartile num clicks on CC urls
        'ccdAgg50',                                      # Second quartile num clicks on CC urls
        'ccdAgg75',                                      # Third quartile num clicks on CC urls
        'ccdAggMax',                                     # Max number of clicks on CC urls
        'itemAggSum',                                    # SUM of clicks on unique ITEM uris (should equal sumCcd)
        'itemAggCount',                                  # COUNT of unique ITEM uris (should equal countItemUrls)
        'itemAggMean',                                   # Average clicks per ITEM uri
        'itemAggStd',                                    # Standard deviation of clicks on ITEM uris
        'itemAggMin',                                    # Minimum number of clicks on ITEM uris
        'itemAgg25',                                     # First quartile num clicks on ITEM uris
        'itemAgg50',                                     # Second quartile num clicks on ITEM uris
        'itemAgg75',                                     # Third quartile num clicks on ITEM uris
        'itemAggMax',                                    # Max number of clicks on ITEM uris
        'serp1',                                         # COUNT CCD URLs with Position <=10'
        'serp1CcdSum',                                   # SUM CCD clicks on URLs with Position <=10
        'serp100',                                       # COUNT CCD URLs with Position <=1000
        'serp100CcdSum',                                 # SUM CCD clicks on URLs with Position <= 1000
        'irCountry',                                     # Country where the IR is located
        'irType',                                        # Type of repository (university, consortia, etc.)
        'irPlat',                                        # IR Platform
        'normIrPlat',                                    # Normalized IR platform names - no versions, etc.
        'ctMethod',                                      # Item Count Method
        'ctEtd',                                         # ETD on 2019-06-07
        'pctEtd',                                        # Ratio of ETD in the IR: ctEtd / countItems
        'gsSO']                                          # GS site operator 2019-06-07

# Create the data frame to store the summary statistics.
outDf = pd.DataFrame(columns=cols)

"""
This long "for" loop generates RAMP summary statistics for each IR included in the IR_base_info.csv file.
Variables are defined in the data table definitions for the output file described in 
"RAMP_summary_stats_documentation.md." See Python pandas documentation for more information about
statistical functions.
"""
for i, r in ir_info.iterrows():
    try:
        ir = r['ir_index_root']
        pc_index = r['ir_page_click_index']
        ai_index = r['ir_access_info_index']
        inst = r['Institution']
        repoName = r['Repository Name']
        rURL = r['URL']
        countItems = int(r['Items in repository on 2019-05-27'])
        ir_ramp_data = ramp_data[(ramp_data['index'] == pc_index) & (ramp_data['citableContent'] == 'Yes') & (ramp_data['clicks'] > 0)].copy()
        """
        Deduplicate item URLs. A more detailed definition of what an "item"
        is in this context is included in the data table definitions
        for the output file. See "RAMP_summary_stats_documentation.md."
        """
        ir_ramp_data = construct_html_urls(ir_ramp_data, r['Platform'])
        ir_ramp_data.to_csv(results_dir + ir + "_ramp_data.csv", index=False)
        countCcdUrls = len(pd.unique(ir_ramp_data['url']))
        countItemUrls = len(pd.unique(ir_ramp_data['html_url']))
        countItemUris = len(pd.unique(ir_ramp_data['unique_item_uri']))
        useRatio = round(countItemUris / countItems, 2)
        sumCcd = ir_ramp_data['clicks'].sum()
        ccdAgg = ir_ramp_data.groupby('url').agg({'clicks': 'sum'})
        ccdAggSum = ccdAgg['clicks'].sum()
        ccdAggDesc = ccdAgg.describe()
        ccdAggCount = ccdAggDesc.loc['count'][0]
        ccdAggMean = ccdAggDesc.loc['mean'][0]
        ccdAggStd = ccdAggDesc.loc['std'][0]
        ccdAggMin = ccdAggDesc.loc['min'][0]
        ccdAgg25 = ccdAggDesc.loc['25%'][0]
        ccdAgg50 = ccdAggDesc.loc['50%'][0]
        ccdAgg75 = ccdAggDesc.loc['75%'][0]
        ccdAggMax = ccdAggDesc.loc['max'][0]
        itemAgg = ir_ramp_data.groupby('unique_item_uri').agg({'clicks': 'sum'})
        itemAggSum = itemAgg['clicks'].sum()
        itemAggDesc = itemAgg.describe()
        itemAggCount = itemAggDesc.loc['count'][0]
        itemAggMean = itemAggDesc.loc['mean'][0]
        itemAggStd = itemAggDesc.loc['std'][0]
        itemAggMin = itemAggDesc.loc['min'][0]
        itemAgg25 = itemAggDesc.loc['25%'][0]
        itemAgg50 = itemAggDesc.loc['50%'][0]
        itemAgg75 = itemAggDesc.loc['75%'][0]
        itemAggMax = itemAggDesc.loc['max'][0]
        serp1Df = ir_ramp_data[ir_ramp_data['position'] <= 10]
        serp1 = len(serp1Df)
        serp1CcdSum = serp1Df['clicks'].sum()
        serp100Df = ir_ramp_data[ir_ramp_data['position'] <= 1000]
        serp100 = len(serp100Df)
        serp100CcdSum = serp100Df['clicks'].sum()
        irCountry = r['Country']
        irType = r['Type']
        irPlat = r['Platform']
        normIrPlat = r['Normalized_Platform']
        ctMethod = r['Item Count Method']
        ctEtd = r['ETD on 2019-06-07']
        # Some IR don't have ETD
        pctEtd = 0
        if ctEtd == '.':
            pctEtd = '.'
        else:
            pctEtd = round(int(ctEtd) / countItems, 2)
        gsSO = r['GS site operator 2019-06-07']
        tdf = pd.DataFrame([[ir, pc_index, ai_index, inst, repoName, rURL, countItems, countCcdUrls, countItemUrls,
                             countItemUris, useRatio, sumCcd, ccdAggSum, ccdAggCount, ccdAggMean, ccdAggStd, ccdAggMin, ccdAgg25,
                             ccdAgg50, ccdAgg75, ccdAggMax, itemAggSum, itemAggCount, itemAggMean, itemAggStd,
                             itemAggMin, itemAgg25, itemAgg50, itemAgg75, itemAggMax,
                             serp1, serp1CcdSum, serp100, serp100CcdSum, irCountry, irType,
                             irPlat, normIrPlat, ctMethod, ctEtd, pctEtd, gsSO]], columns=cols)
        outDf = outDf.append(tdf)
    except Exception as e:
        print(r['ir_index_root'])
        print(e)

outDf.to_csv(results_dir + "RAMP_summary_stats_" + str(fname_date) + ".csv", index=False)

print("Done. The output file, 'RAMP_summary_stats_" + str(fname_date) + ".csv' is in the 'results' directory.")
