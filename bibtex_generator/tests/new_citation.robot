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
    Go To New Book Page
    Input Text  citation_name  robottest2
    Input Text  author  robot testaaja
    Input Text  title  test2
    Input Text  publisher  robot testaaja
    Input Text  address  testi osoite
    Input Text  year  2022
    Click Button  Create New
    Go To Citations Page
    Wait Until Page Contains  Current citation amount:
    Sleep  1s
    Run Keyword And Ignore Error  Scroll Element Into View  link:robottest2
    Wait Until Element Is Visible  link:robottest2
    Click Link  robottest2
    Page Should Contain  author: "robot testaaja" 
    Page Should Contain  title: "test2"
    Page Should Contain  year: "2022"

