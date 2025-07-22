

Give me Python functions to generate fake data for:

# General Ledger and Bank Statements

## General Ledger CSV file with these columns: 

    CSV File Headers:
        transaction_date,posting_date,reference,description,debit,credit,account_code,account_name

Save files with a unique filename {datetime}_gl_data.csv

## Bank Statement (save as `{datetime}_bank_data.csv`):

    CSV File Headers:
        date,description,withdrawal,deposit,balance


####################################################

Generate a 10-lesson tutorial on Faker with complete code examples and detailed ELI5 explanations of each example.  Save this tutorial into a Jupyter Notebook.  

####################################################

Generate a 10-lesson tutorial on {Python f-strings} Faker with complete code examples and detailed ELI5 explanations of each example.  Save this tutorial into a Jupyter Notebook.  

####################################################

tutorial_topic = "Python functions with all types of arguments"

Generate a 10-lesson tutorial on {tutorial_topic} Faker with complete code examples and detailed ELI5 explanations of each example.  Save this tutorial into a Jupyter Notebook.  

###############################################
modify generate_financial_data.py to create two folders one name GL_data and another bank_data and move generated file into the appropiate folder

###############################################
Generate a visual diagram in mermaid.js format from attached workflow outline. Explain to me how to display it and what are my options.

 our next task is to generate PRD document for this project from "00_Data_Recon_Project_Description_v1" and use the "Nexus_Agents_PRD_Copilot_GGem_v2" as a template for structure and content style.

 ******************************************************
 I think option B is safer and more reliable approach. Do the next 3 phases in an incremental ordered and very safe way. 
 
 Follow the instructions below:

 1. Add new incremental functionlity.
 2. Stop and save the file to the file system.Confirm the file is saved in the file system.
 3. Test the functionality.
 4. Fix it if doesn't work.
 5. Implement the next step.
 6. Continue step by step with your updated plan until all the new functionality has been added back and tested and vertified to work correctly. Do not stop until you need my input.

 Give me your updated plan to review and wait for me to confirm.  

 ***************************************
 I want you to execute the plan without stopping and only stop if you have a problem that you need me to give you feedback and directions. Are you clear about this approach?


 #################################################


 Create folders for 

    files_input
        bank_data
        gl_data

    files_output
        reconciled

