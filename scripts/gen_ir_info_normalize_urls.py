import pandas as pd
import os
import fnmatch
from urllib.parse import urlparse
import re


def make_dspace_html_url(bitstream_url):
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

library(rio)
IR <- import("RAMP-IR-info_2020-01-09.xlsx")
str(IR)
# Items in repository
length(IR$ir)
summary(IR$`Items in repository on 2019-05-27`)
# Items by platform
library(dplyr)
IR%>% 
  group_by(Platform)%>% 
  summarise(sum = sum(`Items in repository on 2019-05-27`))%>%
  arrange(desc(sum))
IR$Platform <- factor(IR$Platform, levels = c("DSpace", "Digital Commons", "Eprints", "Fedora"))
library(psych)
describeBy(IR$`Items in repository on 2019-05-27`, IR$Platform)
# Items per country
IR%>% 
  group_by(Country)%>% 
  summarise(sum = sum(`Items in repository on 2019-05-27`))%>%
  arrange(desc(sum))
IR$Country <- factor(IR$Country, levels = c("USA", "Australia", "UK", "Canada", "Sweden", "New Zealand", "South Africa"))
describeBy(IR$`Items in repository on 2019-05-27`, IR$Country)
# Items by Type
IR%>% 
  group_by(Type)%>% 
  summarise(sum = sum(`Items in repository on 2019-05-27`))%>%
  arrange(desc(sum))
IR$Type <- factor(IR$Type, levels = c("University", "Consortium"))
describeBy(IR$`Items in repository on 2019-05-27`, IR$Type)
# Categories
IR$category <- ifelse(IR$`Use Ratio (COUNT unique CCD URLS / Count items in IR)`<=.5 & IR$`Items in repository on 2019-05-27` > 51000, "High Item Low Downloads",
                      ifelse(IR$`Use Ratio (COUNT unique CCD URLS / Count items in IR)`>=.51 & IR$`Items in repository on 2019-05-27` <= 17979,"Low items High Downloads", "Low items Low Downloads"))
table(IR$category)
# Items in use ratio category
library(psych)
IR$category <- factor(IR$category, levels = c("High Item Low Downloads", "Low items Low Downloads", "Low items High Downloads"))
describeBy(IR$`Items in repository on 2019-05-27`, IR$category)
IR%>% 
  group_by(category)%>% 
  summarise(sum = sum(`Items in repository on 2019-05-27`))%>%
  arrange(desc(sum))
# Use ratio category
describeBy(IR$`Use Ratio (COUNT unique CCD URLS / Count items in IR)`, IR$category)
# Items vs. Use ratio
mean(IR$`Items in repository on 2019-05-27`)
IR$Items <- ifelse(
  IR$`Items in repository on 2019-05-27` < 34927.51, "Below Average", "Above Average"
)
IR$Items <- as.factor(IR$Items)
describeBy(IR$`Use Ratio (COUNT unique CCD URLS / Count items in IR)`, IR$Items)
# Use ratio per platform
IR$Platform <- factor(IR$Platform, levels = c("Eprints", "Fedora", "DSpace", "Digital Commons"))
describeBy(IR$`Use Ratio (COUNT unique CCD URLS / Count items in IR)`, IR$Platform)
# Device/ country/ click/position data
#-------load data
dat1 <- import("2019-01_RAMP_all_country-device-info.csv")
dat2 <- import("2019-02_RAMP_all_country-device-info.csv")
dat3 <- import("2019-03_RAMP_all_country-device-info.csv")
dat4 <- import("2019-04_RAMP_all_country-device-info.csv")
dat5 <- import("2019-05_RAMP_all_country-device-info.csv")
str(dat1)
str(dat2)
str(dat3)
str(dat4)
str(dat5)
dat1 <- dat1[, c(-2, -5, -6, -8)]
dat2 <- dat2[, c(-2, -5, -6, -8)]
dat3 <- dat3[, c(-2, -5, -6, -8)]
dat4 <- dat4[, c(-2, -5, -6, -8)]
dat5 <- dat5[, c(-2, -5, -6, -8)]
country_device <- rbind(dat1, dat2)
country_device <- rbind(country_device, dat3)
country_device <- rbind(country_device, dat4)
country_device <- rbind(country_device, dat5)
length(unique(country_device$country))
dat6 <- import("North_South.xlsx")
head(dat6)
length(dat6$Countryabbre)
dat6$Countryabbre <- tolower(dat6$Countryabbre)
country_device_n <- merge(country_device, dat6, by.x = "country", by.y =  "Countryabbre")
length(unique(country_device_n$country))
dat7 <- unique(country_device$country)
dat8 <- unique(dat6$Countryabbre)
dat7[!(dat7 %in% dat8)]
dat8[!(dat8 %in% dat7)]
write.csv(country_device_n, file = "country_device_n.csv")
# Positions vs. clicks
describeBy(country_device_n$clicks, country_device_n$device)
describeBy(country_device_n$position, country_device_n$device)
#Top five countries which use the IRs
country_device_n%>%
  select(clicks, country)%>%
  group_by(country)%>%
  summarise(clicks = sum(clicks))%>%
  arrange(desc(clicks))%>%
  head(5)
# Device use
country_device_n%>%
  select(clicks, device)%>%
  group_by(device)%>%
  summarise(clicks = sum(clicks))%>%
  arrange(desc(clicks))%>%
  mutate(percent = clicks/sum(clicks)*100)
country_device_n$Location <- as.factor(country_device_n$Location)
# Clicks from users in the global north and the global south
country_device_n%>%
  select(clicks, Location)%>%
  group_by(Location)%>%
  summarise(clicks = sum(clicks))%>%
  arrange(desc(clicks))%>%
  mutate(percent = clicks/sum(clicks)*100)
# Device use between users in the global north and the global south
country_device_n%>%
  select(clicks, device, Location)%>%
  group_by(Location, device)%>%
  summarise(clicks = sum(clicks))%>%
  arrange(desc(clicks))%>%
  mutate(percent = clicks/sum(clicks)*100)
mean(country_device_n$clicks)
var(country_device_n$clicks)
range(country_device_n$clicks)
mod <- glm(clicks~position*device, data = country_device_n, family = c("quasipoisson"))
summary(mod)
round(cbind(exp(coef(mod)),
            exp(confint(mod))),3)

