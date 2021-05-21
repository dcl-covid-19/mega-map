# Summary
This directory contains scripts that are meant to run in Airtable, in the Scripting App. The scripts are written as JavsScript and hence the .js suffix.  

# Requirements
Must have a version of Airtable that allows Apps, for example the PRO Plan. BAC production and test bases are on the PRO Plan already. Your individual free account has access to the Apps and therefore Scripting for the first 30 days only.


# Setup and Running the Project
A one-time manual setup is required in Airtable. 
1. Select the base you want to run the scripts against. For BAC, please experiment only using the TEST base, colored grey.
2. At the top right, click the APPS icon
3. At the top right again, select '+ Add an app'
4. In the search box, type 'script'
5. Click the 'Add' button next to the 'Scripting' app
6. Click the small upside down triangle next to the text 'Scripting' at the top left
7. Select 'Rename app' and give it the same name as the file name in this repo, without the '.js' suffix
8. Paste the entire contents from the script file in the repo to Airtable script editing area.  
9. Read the instructions, if any, near the beginning of the scripts for further setup requirements.

Note: you can modify and enhance the scripts in Airtabel or create new ones. Please remember to apply the same changes in this repo as well in order to keep the code in sync for better collaboration. 

# Other Notes
Scripts that invokes external APIs usually require some sort of API KEY. You may need to register one yourself and paste it in the script before you can run the script. It's probably a good idea NOT to check your personal API KEY into the repo. If rwquired, add instructions in the scripts on how to obtain the API KEY and where to paste it in the scripts. 

  




