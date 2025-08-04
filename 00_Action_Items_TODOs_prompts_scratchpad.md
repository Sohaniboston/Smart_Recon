
#############################################################
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


        **********************************

        Rearrange existing menu in the following order:
        1.List the available data files
        2.Process bank data
        3.Generate sample data
        4.Check environment
        5. Test basic functionality
        6. Run simple test
        0.Exit
       

# PROJECT CLEANUP & FINALIZATION

## TODO: clean up files in root folder. 
- Move all files that don't belong in the root folder to a good LOGICAL location.  - Delete only the ones you are sure you do not need for any future version of hte program.  

- Some files have object references that will break, i.e. links to objects in other files in folders.  So you need to move the file, test it from the new location to verify that it still works.  If it does not work, then interpret the error message(s) and change the code so it WILL work from its new location.  


## UPDATE README.md file so that it accurately reflects the project folder structure, and has correct instrucrtions for users.  

- TODO: Update README.md to show an accurate folder and file structure for the FINAL working version of the project files.   For example run_smartrecon.bat and run_smartrecon.py should be shown in the 

    ## Project Structure

    ***smartrecon/ is the PROJECT ROOT FOLDER***
    
    TODO: THINGS TO CHECK 
    ***?? is main.py still the main  entry point??***
    *** is setup/ still the primary setup folder? ***

    TODO: **GO THROUGH THE LIST BELOW TO VERIFY EVERY FILE FOLDER AND ARE IN THEIR CORRECTION LOCATION AS SPECIFIED: ***
    ```
    smartrecon/
    ├── src/                          # Source code
    │   ├── modules/                  # Core functional modules
    │   │   ├── data_ingestion.py     # File loading and validation
    │   │   ├── data_cleaning.py      # Data standardization
    │   │   ├── matching_engine.py    # Transaction matching algorithms
    │   │   ├── exception_handler.py  # Exception management
    │   │   └── reporting.py          # Report generation
    │   ├── utils/                    # Utility functions
    │   │   ├── logger.py             # Logging configuration
    │   │   ├── exceptions.py         # Custom exceptions
    │   │   ├── validators.py         # Data validation
    │   │   └── helpers.py            # Helper functions
    │   ├── main.py                   # CLI entry point    
    │   └── config.py                 # Configuration management
    ├── config/                       # Configuration files
    │   └── default_config.json       # Default configuration
    ├── tests/                        # Test suite
    ├── examples/                     # Example data and configurations
    ├── docs/                         # Documentation, User Guides, 
    ├── requirements.txt              # Python dependencies
    ├── run_smartrecon.bat            # Main Windows Batch script to START the application
    ├── run_smartrecon.py             # Main Python script to START the application
    └── setup.py                      # Package installation
    ```

# IMPROVE THE FOLDER STRUCTURE FOR DATA FILE HANDLING to be more logical
- MAKE IT INTO A FOLDER "PIPELINE" SO IT REFLECTS DATA PROCESSING WORKFLOW . 
- CHOOSE LOGICAL FOLDER NAMES
- UPDATE THE FILE PROCESSING CODE TO USE THE UPDATED FOLDER NAMES FOR:
    - 01 - INPUT (FILES TO BE RECONCILED)  
    - 02 - OUTPUT FILES (RECONCILED)
    - 03 - PROCESSED FILES (for archiving)  
            03_processed_files 

