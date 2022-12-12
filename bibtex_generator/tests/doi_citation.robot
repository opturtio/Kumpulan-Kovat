*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Main Page

*** Test Cases ***
Click DOI Page Link
    Click Button  New Citation
    Click Link  DOI
    DOI Page Should Be Open

Correct DOI Code Adds Correct Citation
    Go To DOI Page
    Input Text  citation_name  doitest
    Input Text  doi  10.1093/ajae/aaq063
    Click Button  Create New
    Wait Until Page Contains  Successfully added new
    Go To Citations Page
    Wait Until Page Contains  Current citation amount:
    Sleep  1s
    Run Keyword And Ignore Error  Scroll Element Into View  link:doitest
    Wait Until Element Is Visible  link:doitest
    Click Link  doitest
    Page Should Contain  author: "Guanming Shi"
    Page Should Contain  title: "An Analysis of the Pricing of Traits in the U.S. Corn Seed Market"

Incorrect DOI Code Gives Correct Error
    Go To DOI Page
    Input Text  citation_name  doierror
    Input Text  doi  moi
    Click Button  Create New
    Wait Until Page Contains  Error
    Page Should Contain  Error: Invalid DOI code
