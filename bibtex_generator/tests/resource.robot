*** Settings ***
Library  SeleniumLibrary
Library  ../AppLibrary.py

*** Variables ***
${SERVER}  localhost:5000
${BROWSER}  headlesschrome
${DELAY}  0 seconds
${HOME URL}  http://${SERVER}
${NEW CITATION URL}  http://${SERVER}/new_citation
${CITATIONS URL}  http://${SERVER}/citations

*** Keywords ***
Open And Configure Browser
    Open Browser  browser=${BROWSER}
    Maximize Browser Window
    Set Selenium Speed  ${DELAY}

Main Page Should Be Open
    Title Should Be  BibteX Generator

New Citation Page Should Be Open
    Title Should Be  New citation

Go To Main Page
    Go To  ${HOME URL}

Go To New Citation Page
    Go To  ${NEW CITATION URL}

Go To Citations Page
    Go To  ${CITATIONS URL}
