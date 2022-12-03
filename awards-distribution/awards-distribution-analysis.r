# Change the default plots size 
options(repr.plot.width=15, repr.plot.height=10)
options(warn=-1)
# Suppress summarise info
options(dplyr.summarise.inform = FALSE)
options(dplyr = FALSE)

# Check if the packages that we need are installed
want = c("dplyr", "ggplot2", "ggthemes", "gghighlight", 
         "grid", "foreign", "scales", "ggpubr", "forcats", 
         "stringr", "lubridate")
have = want %in% rownames(installed.packages())
# Install the packages that we miss
if ( any(!have) ) { install.packages( want[!have] ) }
# Load the packages
junk <- lapply(want, library, character.only = T)
# Remove the objects we created
rm(have, want, junk)

# Importing dataset
sfi.grants <- read.csv('../data/Open-Data-Final.csv')

# Checking dataset's structure
head(sfi.grants)

# Cleaning data
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

sfi.new.grants <- sfi.new.grants %>% mutate(Programme.Name.Clean = str_replace(Programme.Name, "SFI ", ""),
                                           Programme.Name.Clean = str_replace(Programme.Name.Clean, " Programme", ""))

sfi.new.grants$Date <- as.Date(sfi.new.grants$Start.Date, format = "%d/%m/%Y")
sfi.new.grants$Date <- format(sfi.new.grants$Date, "%Y-%m-%d")

allMissing <- is.na(sfi.new.grants)
#get a count for each column
counts <- colSums(allMissing)
counts

paste0("Number of rows in the dataset: ", nrow(sfi.new.grants))

sfi.new.grants %>% mutate(year = year(Date)) %>%
    group_by(year) %>% 
    summarise(total = sum(Revised.Total.Commitment),
        n= n(), average = sum(total)/sum(n)) %>%
    ggplot( aes(x = year, y= total) ) + 
        geom_line( color="#69b3a2", size = 1) +
        geom_point( color="#69b3a2",size=3) +
        labs(x = "Year", y = "",
             title = "Total amount awarded throughout the years",
            subtitle = "Amount awarded (€)") +
        scale_y_continuous(labels = scales::label_number_si(accuracy=0.1)) +
        scale_x_continuous(breaks = seq(from = 2000, to = 2019, by = 1)) +
        scale_fill_brewer(palette='Dark2') +
        theme_minimal() +
        theme(axis.text.x = element_text(face="bold", color="#636363", size=12),
              axis.text.y = element_text(face="bold", color="#636363", size=12),
              plot.title=element_text(vjust=1.5, family='', face='bold', colour='#636363', size=20),
              plot.subtitle=element_text(vjust=1.5, family='', face='bold', colour='#636363', size=15))

# Grouping by Institutes and creating the sum, mean and total number of grants
by_institute <- sfi.new.grants %>% 
  group_by(Research.Body) %>% 
  summarise(total = sum(Revised.Total.Commitment),
            mean = mean(Revised.Total.Commitment),
            n= n()) %>% ungroup()

# Plot the Top 10 Institutes which received the highest grants amount
top10.institutes.value <- by_institute %>% arrange(desc(total)) %>% head(10)

top10.institutes.value %>% 
ggplot( aes(x =reorder(as.factor(Research.Body), total), 
              y= total, fill="") ) + 
    geom_bar(inherit.aes = TRUE, lineend = 'round',
             stat = "identity", width = .5, alpha=.9) +
    scale_y_continuous(labels = scales::label_number_si(accuracy=0.1)) +
    annotate("segment", x = 8, xend = 8, y = 437562222, yend = 749722478,
               arrow = arrow(ends = "both", angle = 90, length = unit(.5,"cm"))) +
    annotate("curve", curvature = -.3, x = 9.7, xend = 8.1, y = 6e+08, yend = 6e+08,
               colour = "#636363", size = 2, arrow = arrow()) +
    annotate("text", x = 7, y = 6e+08, family = "", fontface = 3, size=6,
               label = "Huge gap between \n the most awarded institutions\n Dublin x Outside-Dublin") +
    scale_fill_brewer(palette='Dark2') +
    labs(x = "", y = "",
         title = "Top 10 Granted Institutes - Amount awarded (€)",
        subtitle = "The grants values are in Millions") +
    theme_minimal() + coord_flip() +
    theme(legend.position = "none",
          axis.text.x = element_text(face="bold", color="#636363", size=12),
          axis.text.y = element_text(face="bold", color="#636363", size=12),
          plot.title=element_text(vjust=1.5, family='', face='bold', colour='#636363', size=25),
          plot.subtitle=element_text(vjust=1.5, family='', face='bold', colour='#636363', size=15))

top10.institutes.total <- by_institute %>% arrange(desc(total)) %>% top_n(10)

top10.institutes.total %>% 
ggplot( aes(x =reorder(as.factor(Research.Body), n), 
              y= n) ) + 
    geom_bar(lineend = 'round',
             stat = "identity", width = .5, alpha=.9, fill="steelblue") +
    annotate("segment", x = 8, xend = 8, y = 601, yend = 1150,
               arrow = arrow(ends = "both", angle = 90, length = unit(.5,"cm"))) +
    annotate("curve", curvature = -.3, x = 9.7, xend = 8.1, y = 1100, yend = 1100,
               colour = "#636363", size = 2, arrow = arrow()) +
    annotate("text", x = 7, y = 900, family = "", fontface = 3, size=6,
               label = "Almost 2x gap between \n the most awarded institutions\n Dublin vs Outside-Dublin") +
    scale_fill_brewer(palette='Set2') +
    scale_y_continuous(name="Number of Grants") +
    labs(x = "", y = "",
         title = "Top 10 Granted Institutes - Number of Grants",
        subtitle = "") +
    theme_minimal() + coord_flip() +
    theme(legend.position = "none",
          axis.text.x = element_text(face="bold", color="#636363", size=12),
          axis.text.y = element_text(face="bold", color="#636363", size=12),
          plot.title=element_text(vjust=1.5, family='', face='bold', colour='#636363', size=25),
          plot.subtitle=element_text(vjust=1.5, family='', face='bold', colour='#636363', size=15))

# Grouping by Programmes and creating the sum, mean and total number of grants

by_programme <- sfi.new.grants %>% 
  group_by(Programme.Name.Clean) %>% 
  summarise(total = sum(Revised.Total.Commitment),
            mean = mean(Revised.Total.Commitment),
            n= n()) %>% ungroup()

top10.programmes.value <- by_programme %>% arrange(desc(total)) %>% head(10)

top10.programmes.value %>% 
ggplot( aes(x =reorder(as.factor(Programme.Name.Clean), total), 
              y= total, fill="") ) + 
    geom_bar(lineend = 'round',
             stat = "identity", width = .5, 
             alpha= ifelse(top10.programmes.value$Programme.Name.Clean == "Principal Investigator" | top10.programmes.value$Programme.Name.Clean == "Research Centres", 
                           .9, .4)) +
    scale_fill_brewer(palette='Dark2') +
    scale_y_continuous(labels = scales::label_number_si(accuracy=0.1)) +
    annotate("text", x = 8, y = 4.7e+08, family = "", fontface = 3, size=6,
               label = "Average amount awarded \n Principal Investigator = 1.1M \n Research Centres = 7.5M") +
    labs(x = "", y = "",
         title = "Leading programmes are Principal Investigator and Research Centres",
        subtitle = "Total amount awarded (€)") +
    theme_minimal() + coord_flip() +
    theme(legend.position = "none",
          axis.text.x = element_text(face="bold", color="#636363", size=12),
          axis.text.y = element_text(face="bold", color="#636363", size=12),
          plot.title=element_text(vjust=1.5, family='', face='bold', colour='#636363', size=20),
          plot.subtitle=element_text(vjust=1.5, family='', face='bold', colour='#636363', size=15))

R.version$version.string
