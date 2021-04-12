# Guide for updating data and exporting it from Airtable to NKH

1.	At this [link](https://airtable.com/tbl6O0Dq4Kviezxod/viw3d0VXsRDvR5xVH?blocks=bipEd3VUUUDaj4CEr), go to services and select “School Meals View CSV”  
2.	Click on the circled three dots below and select “Download CSV”  
    ![alt text](https://media.discordapp.net/attachments/694640403739050074/828111042110029844/unknown.png "Guide Airtable to NKH")
3.	Put the file in your desired folder (the default in the code is your downloads folder)
4.	Then open the file called **Airtable to NKH** that is in the GitHub folder in R (VSCode or Rstudio). You might have to just copy and paste the code if it doesn't open up. Sorry about that :(
5.	**DO THIS ONCE:**
 You need certain packages to run this code so the first time you open R in the console copy and paste: 
      1. `install.packages(c(“googlesheets4”, “lubridate”, “tidyverse”))`
      2. if this doesn't run, you might have to install the packages separately:
          1. `install.packages("googlesheets4")`
          2. `install.packages("lubridate")`
          3. `install.packages("tidyverse")`
          4. you might have to change the quotes to single quotes if it doesn’t work
      3. then you have to link your google account, so just follow the directions in VSCode/Rstudio, and you will have to copy and paste the confirmation link from linking your google account into your terminal

6.	All you have to do is hit Run on the top right R, as pictured below and it will upload to this [link](https://docs.google.com/spreadsheets/d/1INYFlE7gIjQCXbouNK9STncdXLVgSDNcMj6mXjxrahY/edit#gid=0) in google drive.
  ![alt text](https://media.discordapp.net/attachments/694640403739050074/828116224990511114/unknown.png "Run in RStudio")
8.	Delete the School Meals CSV from your computer/downloads (you must do this each time)
9.	You should rerun this process every two weeks, preferably around the time of our biweekly Bay Area Community meeting!
