*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Main Page

*** Test Cases ***
Click New Citation Link
    Click Link  New citation
    New Citation Page Should Be Open

Add New Citation
    Go To New Citation Page
    Input Text  citation_name  robottest
    Input Text  title  test
    Input Text  year  2022
    Input Text  author  robot testaaja
    Click Button  Create new
    Go To Citations Page
    Page Should Contain  Citation: robottest

View New Citation
    Create Citation  robottest2  test2  2022  robot testaaja
    Go To Citations Page
    Click Link  robottest2
    Page Should Contain  author: "robot testaaja" 
    Page Should Contain  title: "test2"
    Page Should Contain  year: "2022"

Add Incorrect Citation
    Go To New Citation Page
    Input Text  citation_name  robottest
    Input Text  title  test
    Input Text  year  test year
    Input Text  author  robot testaaja
    Click Button  Create new
    Page Should Contain  Error
