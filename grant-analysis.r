# Importing datasets
sfi.grants <- read.csv('./data/Open-Data-Final.csv')
sfi.grants.gender <- read.csv('./data/SFIGenderDashboard_TableauPublic_2019.csv')

# Checking Grant Commitments dataset
head(sfi.grants)

# Checking SFI Gender dataset

head(sfi.grants.gender)

# Cleaning data

require(dplyr)

sfi.new.grants <- sfi.grants

# Because we are going to analyze new grants from the SFI...
# There are a few grants from funding partners and a few splitting of awards where an award
# was transferred from one institution to another.
# Removing those
sfi.new.grants <- sfi.new.grants[-grep("(N)", sfi.grants$Proposal.ID, fixed = T),]
sfi.new.grants <- sfi.new.grants[-grep("(X)", sfi.grants$Proposal.ID, fixed = T),]
sfi.new.grants <- sfi.new.grants[-grep("(T)", sfi.grants$Proposal.ID, fixed = T),]

# Total of rows from Partners Funds and Splittings - 68
nrow(sfi.grants) - nrow(sfi.new.grants)

# There are 11 "negatives" or 0 grants which will interfere in the analysis
# Decided to remove those (only one will be transform to absolute value)
negatives <- sfi.new.grants %>% filter(Revised.Total.Commitment < 10)

# Remove all negative grants
sfi.new.grants$Revised.Total.Commitment <- abs(sfi.new.grants$Revised.Total.Commitment)
sfi.new.grants <- sfi.new.grants[sfi.new.grants$Revised.Total.Commitment > 10,]


allMissing <- is.na(sfi.new.grants)
#get a count for each column
counts <- colSums(allMissing)
counts

library(Hmisc)
library(psych, warn.conflicts = FALSE)

Hmisc::describe(sfi.new.grants)

require(ggplot2)
require(scales)

# Grouping by Institutes and creating the sum, mean and total number of grants
by_institute <- sfi.new.grants %>% 
  group_by(Research.Body) %>% 
  summarise(total = sum(Revised.Total.Commitment),
            mean = mean(Revised.Total.Commitment),
            n= n()) %>% ungroup()

head(by_institute)

# Change the default plots size 
options(repr.plot.width=15, repr.plot.height=10)

# Plot the Top 10 Institutes which received the highest grants

top10.institutes.value <- by_institute %>% arrange(desc(total)) %>% head(10)

top10.institutes.value %>% 
  ggplot( aes(x =reorder(as.factor(Research.Body), total), 
              y= total) ) +
  geom_bar(stat = "identity", width = .7, show.legend = TRUE, fill="steelblue") +
  ggtitle("Top 10 Institutes - Value of Grants") +
  theme_minimal() +
  xlab("Institutes") + 
  scale_y_continuous(name="Value of the Grant", labels = unit_format(unit = "M", scale = 1e-6)) +
  theme(plot.title = element_text(color = "grey", size = 14, face = "bold", hjust = 0.5)) +
  coord_flip()

top10.institutes.total <- by_institute %>% arrange(desc(total)) %>% top_n(10)

top10.institutes.total %>% 
  ggplot( aes(x =reorder(as.factor(Research.Body), n), 
              y= n) ) +
  geom_bar(stat = "identity", width = .7, show.legend = TRUE, fill="steelblue") +
  ggtitle("Top 10 Institutes - Number of Grants") +
  theme_minimal() +
  xlab("Institutes") + 
  scale_y_continuous(name="Number of Grants") +
  theme(plot.title = element_text(color = "grey", size = 14, face = "bold", hjust = 0.5)) +
  coord_flip()

# Grouping by Programmes and creating the sum, mean and total number of grants

by_programme <- sfi.new.grants %>% 
  group_by(Programme.Name) %>% 
  summarise(total = sum(Revised.Total.Commitment),
            mean = mean(Revised.Total.Commitment),
            n= n()) %>% ungroup()

top10.programmes.value <- by_programme %>% arrange(desc(total)) %>% head(10)

top10.programmes.value %>% 
  ggplot( aes(x =reorder(as.factor(Programme.Name), total), 
              y= total) ) +
  geom_bar(stat = "identity", width = .7, show.legend = TRUE, fill="steelblue") +
  ggtitle("Top 10 Programmes - Value of Grants") +
  theme_minimal() +
  xlab("Programmes") + 
  scale_y_continuous(name="Value of the Grant", labels = unit_format(unit = "M", scale = 1e-6)) +
  theme(plot.title = element_text(color = "grey", size = 14, face = "bold", hjust = 0.5)) +
  coord_flip()

top10.programmes.value %>% head(2)

# Data Exploration - Second Dataset (Grants by Gender)

sfi.grants.gender2 <- sfi.grants.gender
sfi.grants.gender2$Award.Status <- as.factor(sfi.grants.gender2$Award.Status)
sfi.grants.gender2$Applicant.Gender <- as.factor(sfi.grants.gender2$Applicant.Gender)

allMissing <- is.na(sfi.grants.gender2)
#get a count for each column
counts <- colSums(allMissing)

require(Hmisc)
require(psych, warn.conflicts = FALSE)

Hmisc::describe(sfi.grants.gender2)


# By Gender
describeBy(sfi.grants.gender[,c("Amount.Requested", "Amount.funded")], sfi.grants.gender$Applicant.Gender)

# How many applications were submitted each year by Gender?
total.by.year <- sfi.grants.gender2 %>% 
  group_by(Year, Applicant.Gender) %>% 
  summarise(total = n())

total.by.year %>% ggplot( aes(fill=Applicant.Gender, y=total, x=as.factor(Year))) + 
  geom_bar(stat="identity", position="dodge") +
  ggtitle("Frequency of Applicants by Year") +
  theme(plot.title = element_text(color = "grey", size = 16, face = "bold", hjust = 0.5)) +
  xlab("Years")

# Proportion of accepted and denied applications by gender
require(gmodels)
CrossTable(sfi.grants.gender2$Applicant.Gender, sfi.grants.gender2$Award.Status,
          prop.r=TRUE,
          prop.c=FALSE,
          prop.t=FALSE,
          prop.chisq=FALSE,
          digits=2)

# Chi-squared test for variables Gender and Award Status
status.gender.table <- table(sfi.grants.gender2$Applicant.Gender, sfi.grants.gender2$Award.Status)
chisq.test(status.gender.table)

# By Award Status
describeBy(sfi.grants.gender[,c("Amount.Requested", "Amount.funded")], sfi.grants.gender$Award.Status)

# Relationship between Amount Requested x Status (Awarded/Declined)

amount.requested.clean <- filter(sfi.grants.gender2, !is.na(Amount.Requested))

# Creating a category based on quantile to categorize the Amount Requested
total.amount.requested <- amount.requested.clean %>%
  mutate(Category.Amount=cut(Amount.Requested, 
                             breaks=quantile(Amount.Requested, c(0,.25,.50,.75,1), na.rm = TRUE), 
                             labels=c("low","medium","high","very-high")))

total.amount.requested %>% group_by(Category.Amount) %>% summarise(total= n()) %>% ungroup()


CrossTable(total.amount.requested$Award.Status, total.amount.requested$Category.Amount,
          prop.r=TRUE,
          prop.c=FALSE,
          prop.t=FALSE,
          prop.chisq=FALSE,
          digits=2)

# Plot the total of awarded/declined by categories
categories.amount <- total.amount.requested %>%
  group_by(Category.Amount, Award.Status) %>%
  filter(!is.na(Category.Amount)) %>%
  summarise(total = n())

categories.amount %>% ggplot( aes(fill=Award.Status, y=total, x=as.factor(Category.Amount))) + 
  geom_bar(position="dodge", stat="identity") +
  ggtitle("") +
  theme_minimal() +
  theme(plot.title = element_text(color = "grey", size = 14, face = "bold", hjust = 0.5)) +
  xlab("Category")

R.version


