# This script converts the parsed judge data from long to wide format.

rm(list=ls())
setwd("~/GitHub/Parser-for-Lexis-Nexus-State-Supreme-Court-Cases")

library(reshape2)

# Read in wide-format .csv from python script parsing judges
y <- read.csv("C:/Users/sum410/Dropbox/PSU2018-2019/RA/Scraper/Final_Scrapes/GRPost1990_final.csv", 
              header = T, na.strings=c("", "NA"))
y$panel_state <- as.character(y$panel_state)
y$Judge1_Vote <- as.character(y$Judge1_Vote)
y$Judge2_Vote <- as.character(y$Judge2_Vote)
y$Judge3_Vote <- as.character(y$Judge3_Vote)
y$Judge4_Vote <- as.character(y$Judge4_Vote)
y$Judge5_Vote <- as.character(y$Judge5_Vote)
y$Judge6_Vote <- as.character(y$Judge6_Vote)
y$Judge7_Vote <- as.character(y$Judge7_Vote)
y$Judge8_Vote <- as.character(y$Judge8_Vote)
y$Judge9_Vote <- as.character(y$Judge9_Vote)
y$Judge10_Vote <- as.character(y$Judge10_Vote)
molten1 <- melt(y, id = c("Judge1_Last_Name", "Judge2_Last_Name", "Judge3_Last_Name", "Judge4_Last_Name",
                          "Judge5_Last_Name", "Judge6_Last_Name", "Judge7_Last_Name", "Judge7_Last_Name", 
                          "Judge8_Last_Name", "Judge9_Last_Name", "Judge10_Last_Name", "LexisCite", "Judge1_Vote",
                          "Judge2_Vote", "Judge3_Vote", "Judge4_Vote", "Judge5_Vote", "Judge6_Vote", "Judge7_Vote"
                          , "Judge8_Vote", "Judge9_Vote", "Judge10_Vote", "Judge1_code", "Judge2_code", "Judge3_code"
                          , "Judge4_code", "Judge5_code", "Judge6_code", "Judge7_code", "Judge8_code", "Judge9_code"
                          , "Judge10_code"))
j1 <- dcast(molten1, formula = Judge1_Last_Name + LexisCite + Judge1_Vote + Judge1_code ~ variable)
j2 <- dcast(molten1, formula = Judge2_Last_Name + LexisCite + Judge2_Vote + Judge2_code ~ variable)
j3 <- dcast(molten1, formula = Judge3_Last_Name + LexisCite + Judge3_Vote + Judge3_code ~ variable)
j4 <- dcast(molten1, formula = Judge4_Last_Name + LexisCite + Judge4_Vote + Judge4_code ~ variable)
j5 <- dcast(molten1, formula = Judge5_Last_Name + LexisCite + Judge5_Vote + Judge5_code ~ variable)
j6 <- dcast(molten1, formula = Judge6_Last_Name + LexisCite + Judge6_Vote + Judge6_code ~ variable)
j7 <- dcast(molten1, formula = Judge7_Last_Name + LexisCite + Judge7_Vote + Judge7_code ~ variable)
j8 <- dcast(molten1, formula = Judge8_Last_Name + LexisCite + Judge8_Vote + Judge8_code ~ variable)
j9 <- dcast(molten1, formula = Judge9_Last_Name + LexisCite + Judge9_Vote + Judge9_code ~ variable)
j10 <- dcast(molten1, formula = Judge10_Last_Name + LexisCite + Judge10_Vote + Judge10_code ~ variable)

names(j1)[names(j1) == 'Judge1_Last_Name'] <- 'judge_ln'
names(j2)[names(j2) == 'Judge2_Last_Name'] <- 'judge_ln'
names(j3)[names(j3) == 'Judge3_Last_Name'] <- 'judge_ln'
names(j4)[names(j4) == 'Judge4_Last_Name'] <- 'judge_ln'
names(j5)[names(j5) == 'Judge5_Last_Name'] <- 'judge_ln'
names(j6)[names(j6) == 'Judge6_Last_Name'] <- 'judge_ln'
names(j7)[names(j7) == 'Judge7_Last_Name'] <- 'judge_ln'
names(j8)[names(j8) == 'Judge8_Last_Name'] <- 'judge_ln'
names(j9)[names(j9) == 'Judge9_Last_Name'] <- 'judge_ln'
names(j10)[names(j10) == 'Judge10_Last_Name'] <- 'judge_ln'

names(j1)[names(j1) == 'Judge1_Vote'] <- 'judge_vote'
names(j2)[names(j2) == 'Judge2_Vote'] <- 'judge_vote'
names(j3)[names(j3) == 'Judge3_Vote'] <- 'judge_vote'
names(j4)[names(j4) == 'Judge4_Vote'] <- 'judge_vote'
names(j5)[names(j5) == 'Judge5_Vote'] <- 'judge_vote'
names(j6)[names(j6) == 'Judge6_Vote'] <- 'judge_vote'
names(j7)[names(j7) == 'Judge7_Vote'] <- 'judge_vote'
names(j8)[names(j8) == 'Judge8_Vote'] <- 'judge_vote'
names(j9)[names(j9) == 'Judge9_Vote'] <- 'judge_vote'
names(j10)[names(j10) == 'Judge10_Vote'] <- 'judge_vote'

names(j1)[names(j1) == 'Judge1_code'] <- 'judge_code'
names(j2)[names(j2) == 'Judge2_code'] <- 'judge_code'
names(j3)[names(j3) == 'Judge3_code'] <- 'judge_code'
names(j4)[names(j4) == 'Judge4_code'] <- 'judge_code'
names(j5)[names(j5) == 'Judge5_code'] <- 'judge_code'
names(j6)[names(j6) == 'Judge6_code'] <- 'judge_code'
names(j7)[names(j7) == 'Judge7_code'] <- 'judge_code'
names(j8)[names(j8) == 'Judge8_code'] <- 'judge_code'
names(j9)[names(j9) == 'Judge9_code'] <- 'judge_code'
names(j10)[names(j10) == 'Judge10_code'] <- 'judge_code'

new <- rbind(j1, j2, j3, j4, j5, j6, j7, j8, j9, j10)

completeFun <- function(data, desiredCols) {
  completeVec <- complete.cases(data[, desiredCols])
  return(data[completeVec, ])
}

new <- completeFun(new, "judge_ln")
sort1.new <- new[order(new$LastName, new$judge_ln) , ]

sort1.new$judgeNP <- NULL
sort1.new$Judge1_code <- NULL
sort1.new$Judge2_code <- NULL
sort1.new$Judge3_code <- NULL
sort1.new$Judge4_code <- NULL
sort1.new$Judge5_code <- NULL
sort1.new$Judge6_code <- NULL
sort1.new$Judge7_code <- NULL
sort1.new$Judge8_code <- NULL
sort1.new$Judge9_code <- NULL
sort1.new$Judge10_code <- NULL
sort1.new$Judge11_code <- NULL
sort1.new$Judge11_Last_Name <- NULL
sort1.new$Judge11_Vote <- NULL
sort1.new$judges <- NULL
sort1.new$dissent_no <- NULL
sort1.new$dissent_name <- NULL
sort1.new$dissent_1 <- NULL
sort1.new$dissent_2 <- NULL
sort1.new$dissent_3 <- NULL
sort1.new$dissent_4 <- NULL
sort1.new$dissent_5 <- NULL
sort1.new$concur_no <- NULL
sort1.new$concur_name <- NULL
sort1.new$dissent_no <- NULL
sort1.new$silent_dissent <- NULL
sort1.new$Email <- NULL

# Merge in Bonica ideal points
ideal <- read.csv("C:/Users/sum410/Dropbox/PSU2018-2019/RA/Scraper/Summer_Work/bonica_ideal_points.csv", 
                  header = T, na.strings=c("", "NA"))
ideal$judge_ln <- toupper(ideal$judge_ln)
ideal$judge_ln <- sub('(?<=\\,).*$', '', ideal$judge_ln, perl=TRUE)
ideal$judge_ln <- sub(',', ' ', ideal$judge_ln)
ideal$judge_ln <- sub('JR', '', ideal$judge_ln)
ideal$judge_ln <- sub(' II', '', ideal$judge_ln)
ideal$state <- sub("OK", "OK-SC", ideal$state)
ideal$state <- sub("OK-SC (crim)", "OK (crim)", ideal$state)
#ideal$state <- sub("TX", "TX-SC", ideal$state)
#my.data$LANDING <- sub('(?<=\\?).*$', '', my.data$LANDING, perl=TRUE)
sort1.new$judge_ln <- as.character(sort1.new$judge_ln)
ideal$judge_ln <- trimws(ideal$judge_ln, which = c("both"))

final <- merge(sort1.new, ideal, by = c("judge_ln", "state"), all.x = T)

# Write long-format data w/ merged ideal points to .csv
write.csv(final, file = "merged_judges_GRPost1990_long.csv",row.names=FALSE)
