*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Main Page

*** Test Cases ***
Click New Citation Link
    Click Button  New Citation
    Click Link  Book
    New Citation Page Should Be Open

Add New Book Citation
    Go To New Book Page
    Input Text  citation_name  robottest book
    Input Text  author  robot testaaja
    Input Text  title  test
    Input Text  publisher  robot testaaja
    Input Text  address  testi osoite
    Input Text  year  2022
    Click Button  Create New
    Go To Citations Page
    Page Should Contain  Citation: robottest book

View New Citation
    Create Book  robottest2  robot testaaja  test2  robot testaaja  testi osoite  2022
    Go To Citations Page
    Click Link  robottest2
    Page Should Contain  author: "robot testaaja" 
    Page Should Contain  title: "test2"
    Page Should Contain  year: "2022"

Add Incorrect Citation
    Go To New Book Page
    Input Text  citation_name  robottest book
    Input Text  author  robot testaaja
    Input Text  title  test
    Input Text  publisher  robot testaaja
    Input Text  address  testi osoite
    Input Text  year  test
    Click Button  Create New
    Page Should Contain  Error

#Delete New Citation
#    Create Book  robottest3  robot testaaja  test2  robot testaaja  testi osoite  2022
#    Go To Citations Page
#    Click Button  Remove robottest3 citation
#    Page Should Not Contain  Citation: robottest3