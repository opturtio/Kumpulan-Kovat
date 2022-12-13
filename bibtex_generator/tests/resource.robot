*** Settings ***
Library  SeleniumLibrary
Library  ../AppLibrary.py

*** Variables ***
${SERVER}  localhost:5000
${BROWSER}  headlesschrome
${DELAY}  0.1 seconds
${HOME URL}  http://${SERVER}
${NEW BOOK URL}  http://${SERVER}/new_book
${CITATIONS URL}  http://${SERVER}/citations
${DOI URL}  http://${SERVER}/doi

*** Keywords ***
Open And Configure Browser
    Open Browser  browser=${BROWSER}
    # Maximize Browser Window
    Set Window Size  ${1920}  ${1080}
    Set Selenium Speed  ${DELAY}

Main Page Should Be Open
    Title Should Be  BibteX Generator

New Citation Page Should Be Open
    Title Should Be  New citation

DOI Page Should Be Open
    Title Should Be  DOI

Go To Main Page
    Go To  ${HOME URL}

Go To New Book Page
    Go To  ${NEW BOOK URL}

Go To Citations Page
    Go To  ${CITATIONS URL}

Go To DOI Page
    Go To  ${DOI URL}
