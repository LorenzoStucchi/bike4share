# Bike4Share
This repository contains the project of the course *Software Enginnering for GeoInformatics* teached by Professor Elisabetta Di Nitto in the academic year 2018/2019.

The project, including documentation, is in English.

## Getting Started

### Prerequisites

For running the *bike4share* is needed to have the following packages, tested with that raccomanded version:

* Pandas 0.24.2
* Geopandas 0.4.1
* Psycopg2 2.8.1
* Sqlalchemy 1.3.2
* Geoalchemy2 0.6.1
* GeoJSON 2.4.1
* Bokeh 1.1.0
* Flask 1.0.2
* Werkzeug 0.14.1
* Psycopg2 2.8.1

To start the execution of the code is needed to have installed a server with PostgreSQL, and create a database called bike4share.

### Installing

Select a folder and download the code and the documentation

```
git clone https://github.com/LorenzoStucchi/bike4share.git
```

Check into *code* the file *dbConfig.txt* and set the database name, the user and the password as in the example:

```
dbname=bike4share user=postgres password=postgres
```

Move into the folder code, into the terminal with the following code

```
cd code
```

Run the file *createSchema.py* for create the database needed with the web application:

```
python createSchema.py
```

The code create into the *code* folder a file *secret_key.txt* this key are needed for the registration of the technician.

### Running

For starting the webpage application you need to run:
```
python main.py
```

The page for the technician registration is not visible and directly accessibile, but you need to go to the page */tec_reg*.
The technician can access to a page with a summary and different statics about the usage of the bike stalls.

## Documentation

In the folder *RelaesedDocs* there is the documentation describing the code divide in 3 main documents:

* Design Document (DD.pdf)
* Requirement Analysis and Specification Document (RASD.pdf)
* Test Plan Document (TPD.pdf)

## Authors
| Name and Surname  | Matricola   | Email                                  |
|-------------------|:-----------:|----------------------------------------|
| Sara Maffioli   | 905432 | sara.maffioli@mail.polimi.it        |
| Lorenzo Giuliano Papale |  905795  | lorenzogiuliano.papale@mail.polimi.it |
| Lorenzo Stucchi   | 899072 | lorenzo.stucchi@mail.polimi.it |
| Federica Vaghi | 905531 | federica.vaghi@mail.polimi.it | 

## License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE.md file for details
