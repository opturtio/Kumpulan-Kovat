*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Main Page

*** Test Cases ***
Edit New Citation
    Create Book  robottest4  robot testaaja  test2  robot testaaja  testi osoite  2022
    Go To Citations Page
    Run Keyword And Ignore Error  Scroll Element Into View  link:robottest4
    Wait Until Element Is Visible  link:robottest4
    Click Link  robottest4
    Run Keyword And Ignore Error  Scroll Element Into View  link:Edit
    Wait Until Element Is Visible  link:Edit
    Click Link  Edit
    Input Text  citation_name  Edited citation
    Run Keyword And Ignore Error  Scroll Element Into View  link:Edit values
    Wait Until Element Is Visible  link:Edit values
    Run Keyword And Ignore Error  Click Link  Edit values
    Page Should Contain  @book{Edited citation
