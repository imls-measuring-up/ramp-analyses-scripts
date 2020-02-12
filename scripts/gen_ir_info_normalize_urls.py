"""Generate RAMP IR Use Ratio and Summary Stats for Jan 1 - May 31, 2019

This script generates summary statistics of IR search engine performance data
as reported by Google and harvested by the RAMP application. It also cross-
references RAMP data with manually collected data about IR to calculate
the use ratio and other analyses described in Arlitsch et al., 2020 (in review).

Dependencies:

1. Python pandas, available from <https://pandas.pydata.org/>. Should be installed
in the Python environment in which this script will be run.

2. "RAMP-IR-base-info.csv": This file contains some IR specific configuration data from
RAMP, as well as manually collected data including the count of items in each IR. The data
were collected between May 27 and June 7, 2019. If this script was downloaded or cloned
from the ramp-analysis-scripts GitHub repository at
<https://github.com/imls-measuring-up/ramp-analyses-scripts>, then the "RAMP-IR-base-info.csv"
file should be in the repository's "data" directory. Column definitions for this file
are provided in the "RAMP_IR_base_info_column_definitions.md" file, which is also
included in the GitHub repository.

3. RAMP data: A subset of RAMP data for the IR listed in the "RAMP-IR-base-info.csv" file
has been published at Dryad: <https://doi.org/10.5061/dryad.fbg79cnr0>. The data are too
large to be included in the GitHub repository, but the repository includes an empty
directory, 'ramp_data.' The data should be downloaded from Dryad into the 'ramp_data'
folder. Dataset documentation are included in the item record in Dryad.

This script will output a CSV file, "RAMP-IR-info_YYYY-MM-DD.csv," where "YYYY-MM-DD"
will be the date on which the script is run.

"""


import pandas as pd

import os

import fnmatch

from urllib.parse import urlparse

import re


def make_dspace_html_url(bitstream_url):
    """Brief description of what this function does

    Parameters
    ----------

    bitstream_url:
        What this is

    Returns
    -------

    object
        What the object is
    """
    
    p = urlparse(bitstream_url)
    handle = re.compile("\/[0-9\?\.]+\/[0-9][0-9]+")
    xmlui = re.compile('xmlui')
    jspui = re.compile('jspui')
    dspace = re.compile('dspace')
    h = handle.search(p.path)
    x = xmlui.search(p.path)
    j = jspui.search(p.path)
    d = dspace.search(p.path)
    if h:
        if j:
            return p.scheme + '://' + p.netloc + '/' + 'jspui' + '/' + 'handle' + h.group()
        elif x:
            return p.scheme + '://' + p.netloc + '/' + 'xmlui' + '/' + 'handle' + h.group()
        elif d:
            return p.scheme + '://' + p.netloc + '/' + 'dspace' + '/' + 'handle' + h.group()
        else:
            return p.scheme + '://' + p.netloc + '/' + 'handle' + h.group()


def make_eprints_fedora_html_url(pdf_url):
    p = urlparse(pdf_url)
    pdf_path = re.compile("\/[0-9][0-9]+")
    pdf_id = pdf_path.search(p.path)
    if pdf_id:
        return p.scheme + '://' + p.netloc + pdf_id.group()


def make_fedora_ne_html_url(pdf_url):
    p = urlparse(pdf_url)
    pdf_path = re.compile("\/files\/neu:[a-z0-9]+")
    pdf_id = pdf_path.search(p.path)
    if pdf_id:
        return p.scheme + '://' + p.netloc + pdf_id.group()


def make_bepress_ccd_urls(pdf_url):
    p = urlparse(pdf_url)
    base_url = 'oai:' + p.netloc + ':'
    contextRe = re.compile(r'context=([a-z0-9_\-]*)')
    articleRe = re.compile(r'article=([0-9][0-9][0-9][0-9])')
    contextSearch = contextRe.search(pdf_url)
    articleSearch = articleRe.search(pdf_url)
    if contextSearch:
        if articleSearch:
            context = contextSearch.group().strip('context=')
            article = articleSearch.group().strip('article=')
            return base_url + str(context) + '-' + str(article)


def construct_html_urls(ir_data, platform):
    if platform == 'DSpace':
        ir_data['html_url'] = ir_ramp_data['url'].apply(make_dspace_html_url)
    if platform == 'EPrints 3':
        ir_data['html_url'] = ir_ramp_data['url'].apply(make_eprints_fedora_html_url)
    if platform == 'Fedora/Samvera':
        ir_data['html_url'] = ir_ramp_data['url'].apply(make_fedora_ne_html_url)
    if platform == 'Fedora':
        ir_data['html_url'] = ir_ramp_data['url'].apply(make_eprints_fedora_html_url)
    if platform == 'Digital Commons':
        ir_data['html_url'] = ir_ramp_data['url'].apply(make_bepress_ccd_urls)
    return ir_data


data_dir = '../data/'
# ramp_data_dir = data_dir + 'ramp_raw/'
ramp_data_dir = '../data/published_data/'
# out_dir = data_dir + 'out/'

click_data_files = []

for r, d, n in os.walk(ramp_data_dir):
    for f in n:
        if fnmatch.fnmatch(f, '*page-clicks*'):
            fname = os.path.join(r, f)
            click_data_files.append(fname)

ramp_data = pd.read_csv(click_data_files[0])

for f in click_data_files[1:]:
    ramp_data = ramp_data.append(pd.read_csv(f))

ir_info = pd.read_csv(data_dir + 'RAMP-IR-info.csv')

cols = ['ir',                                            # ir_index_root
        'pc_index',                                      # ir_page_click_index
        'ai_index',                                      # ir_access_info_index
        'inst',                                          # Institution
        'repoName',                                      # Repository Name
        'rURL',                                          # URL
        'countItems',                                    # Items in repository on 2019-05-27
        'countCcdUrls',                                  # COUNT unique CC URLs Jan1 to May31 2019
        'countItemUrls',                                 # COUNT unique ITEM URLs in RAMP Jan1 to May31
        'useRatio',                                      # Use Ratio (COUNT unique ITEM URLS in RAMP/ COUNT items in IR)
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
        'itemAggSum',                                    # SUM of clicks on unique ITEM urls (should equal sumCcd)
        'itemAggCount',                                  # COUNT of unique ITEM urls (should equal countItemUrls)
        'itemAggMean',                                   # Average clicks per ITEM url
        'itemAggStd',                                    # Standard deviation of clicks on ITEM urls
        'itemAggMin',                                    # Minimum number of clicks on ITEM urls
        'itemAgg25',                                     # First quartile num clicks on ITEM urls
        'itemAgg50',                                     # Second quartile num clicks on ITEM urls
        'itemAgg75',                                     # Third quartile num clicks on ITEM urls
        'itemAggMax',                                    # Max number of clicks on ITEM urls
        'serp1',                                         # COUNT CCD URLs with Position <=10'
        'serp1CcdSum',                                   # SUM CCD clicks on URLs with Position <=10
        'serp100',                                       # COUNT CCD URLs with Position <=1000
        'serp100CcdSum',                                 # SUM CCD clicks on URLs with Position <= 1000
        'irCountry',                                     # Country where the IR is located
        'irType',                                        # Type of repository (university, consortia, etc.)
        'irPlat',                                        # IR Platform
        'ctMethod',                                      # Item Count Method
        'ctEtd',                                         # ETD on 2019-06-07
        'gsSO']                                          # GS site operator 2019-06-07

outDf = pd.DataFrame(columns=cols)

for i, r in ir_info.iterrows():
    ir = r['ir_index_root']
    print(ir)
    pc_index = r['ir_page_click_index']
    ai_index = r['ir_access_info_index']
    inst = r['Institution']
    repoName = r['Repository Name']
    rURL = r['URL']
    countItems = r['Items in repository on 2019-05-27']
    ir_ramp_data = ramp_data[(ramp_data['index'] == pc_index) &
                             (ramp_data['citableContent'] == 'Yes') &
                             (ramp_data['clicks'] > 0)].copy()
    # deduplicate item URLs
    ir_ramp_data = construct_html_urls(ir_ramp_data, r['Platform'])
    countCcdUrls = len(pd.unique(ir_ramp_data['url']))
    countItemUrls = len(pd.unique(ir_ramp_data['html_url']))
    useRatio = round(countItemUrls / countItems, 2)
    sumCcd = ir_ramp_data['clicks'].sum()
    # ir_ramp_data.groupby('url').agg({'clicks': 'sum'})
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
    itemAgg = ir_ramp_data.groupby('html_url').agg({'clicks': 'sum'})
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
    ctMethod = r['Item Count Method']
    ctEtd = r['ETD on 2019-06-07']
    gsSO = r['GS site operator 2019-06-07']
    tdf = pd.DataFrame([[ir, pc_index, ai_index, inst, repoName, rURL, countItems, countCcdUrls, countItemUrls,
                         useRatio, sumCcd, ccdAggSum, ccdAggCount, ccdAggMean, ccdAggStd, ccdAggMin, ccdAgg25,
                         ccdAgg50, ccdAgg75, ccdAggMax, itemAggSum, itemAggCount, itemAggMean, itemAggStd,
                         itemAggMin, itemAgg25, itemAgg50, itemAgg75, itemAggMax,
                         serp1, serp1CcdSum, serp100, serp100CcdSum, irCountry, irType,
                         irPlat, ctMethod, ctEtd, gsSO]], columns=cols)
    outDf = outDf.append(tdf)

outDf.to_csv(data_dir + "RAMP-IR-info_2020-01-09.csv", index=False)

