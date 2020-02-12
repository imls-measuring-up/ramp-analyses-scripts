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
