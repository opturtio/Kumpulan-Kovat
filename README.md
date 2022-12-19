# Kumpulan kovat
![workflow](https://github.com/opturtio/Kumpulan-Kovat/actions/workflows/main.yml/badge.svg)
[![codecov](https://codecov.io/gh/opturtio/Kumpulan-Kovat/branch/main/graph/badge.svg)](https://codecov.io/gh/opturtio/Kumpulan-Kovat)  
[Deployed product](https://bibtex-generator.fly.dev/)\
[Backlog](https://docs.google.com/spreadsheets/d/1yvGNC3GYo8Uez8AEf1WDs8b2HU5dlRqFfppQ7lEhM3Y/edit?usp=sharing)  
[Retrospektiivit](/documents/RETRO.md)\
**[Loppuraportti](https://docs.google.com/document/d/1Dcc5sjZWAT9LhuBdga6roPLIJyquHs_foNhIr7RgoMw/edit?usp=sharing)**
## Definition of Done

The acceptance criteria of the user story have been implemented.\
All code written follows the pylint-guidelines of the project.\
Unittest coverage is atleast 70%.\
There is fair amount of e2e tests.

## Invoke komennot

Käynnistä ohjelma
```bash
poetry run invoke start
```

Pylint
```bash
poetry run invoke lint
```

Pep8
```bash
poetry run invoke format
```

Coverage report
```bash
poetry run invoke coverage-report
```
