# About HydroDB

`HydroDB` can be a non-relational or a relational database library for Python, designed to be easy to use and agile. It allows you to create `JSON` files and store data in them with desired keys. Additionally, it enables searching, updating, and deleting data within the `JSON` file.

## Why HydroDB exists?

The idea for HydroDB emerged during my college days when I had to use TinyDB in one of my classes. While TinyDB is a good library for non-relational databases, I felt that something was missing. After studying the subject, I decided to create my own non-relational database library.

## Setting Up

### Requirements (for versions 1.#.#)

- [Python 3](https://www.python.org/downloads/) version 3.12.2 or above.

```bash
pip install hydrodb
```


## Data structure

On HydroDB all `JSON` files has an shered base struct:

```json
{
  "TABLE NAME": "tables-name",
  "META DATA": "tables-meta-data",
  "TABLE COLUMNS": [
    "columns_1",
    "columns_2",
    "...",
  ],
  "PK": "tables-primary-key",
  "ROWS": [
        {
          "id": 1,
          "values": {
              "column_1": "x",
              "columns_2": null,
          }
        }
  ]
}
```

> - "TABLE TABME": string -> Is the name of the table.
>
> - "META DATA": string -> Here goes the descriptions of the data tha goes into the table. 
>
> - "TABLE COLUMNS":array/list -> The columns tha goes into the table.
>
> - "PK": string -> Is the columns that represents the primary key of the table.
>
> - "ROWS": array/list of dictionaries -> Here goes the rows of the table. Is important to remember that every single row has an id and the values of the row associeted with the table's columns.

## Observable functions
Those functions are made to lookup the table, for general porpose


# Get Started

Here is a simple guide on how to use the `HydroDB` module.

## Calling HydroDB in the program

### Default creation
To use the module, simply use:
```python
from hydrodb import HydroDB

hydro = HydroDB()
```
In this case, a directory `db/` will be created at your project folder level:
```
your-project-folder
    |--> db/ 
    |--> hydrodb/
    |--> main.py
```

### Optional dirpath
`HydroDB` allows you to choose a folder to create the database directory.

To do that, use:
```python
from hydrodb import HydroDB

hydro = HydroDB(optional_path='any_dir_name')
```

In this case, a directory `db/` will be created at your project folder level:
```
your-project-folder
    |--> any_dir_name
        |--> db/
    |--> hydrodb/
    |--> main.py
```

## Commands list

Designed to be a very user-friendly module, `HydroDB` only has 6 **operational** functions and 3 **observable** functions to be called.

## Operational Functions

The opearional functions are thesigned to execute the CRUD 

- C : create
- R : read
- U : update
- D : delete

1 of them are to `create`, 1 for `reade`, 3 for `update` and 1 for `delete`.

    
### create_table() --> `create`

The create() function is designed for the creation of tables, along with the columns that each table possesses.

```python 
hydro.create_table(
    tables="Table_1", 
    columns=["name", "age"],
    pk="name"
)
```

```json
// Expected table structure
{
  "TABLE NAME": "TABLE_1",
  "META DATA": null,
  "TABLE COLUMNS": [
    "name",
    "age"
  ],
  "PK": "name",
  "ROWS": []
}
```
- `tables`: str --> Na name of the table to be created. (Learn more about [strings](https://www.w3schools.com/python/python_strings.asp))

- `columns`: Lists --> The columns for the table. (Learn more about [lists](https://www.w3schools.com/python/python_lists.asp))

- `pk`: str --> Defines the primary key of the table. If no values are passed, the primary-key will be the  `id`


### add_row() --> `update`

To add values to table's columns, uses the add() function.

```python
hydro.add_rows(
    table_name="Table_1",
    into_columns=["name", "age"],
    values=["James", 34]
)
```
```json
// Expected result
{
  "TABLE NAME": "TABLE_1",
  "META DATA": null,
  "TABLE COLUMNS": [
    "name",
    "age"
  ],
  "PK": "name",
  "ROWS": [
    {
        "id": 1,
        "values":{
            "name": "James",
            "age": 34
        }
    }
  ]
}
```

- `tables_names`: str --> Receives the table that you want to add values.

- `into`: list --> These are the columns of the table that will have a value added.

- `values`: list --> These are the values for each column selected.


### query() --> `search`

This function is used to get values from a table.


```python
hydro.query(
    from_="Table_1",
    columns=["name", "age"],
    where="age = 34"
)
```

```bash
# expected output: [{"id" : 1, "values" :{"name":"James", "age":34}}]
```
**NOTE:** A string is returned

- `table_name`: str --> Is the name of the table to be querried.

- `columns`: list --> Here, is the values you want to receve. If None, the entire row is returned.

- `filter`: str --> Is the parameter to querry a specific group of elements or a single element. If non filter parameter is passed, the entire table will be returned.


### update() --> `update`

The update funcions serves to update values from rows, or a single row.
If you want to update a single row, uses the element `id` as the filter parameter.

```python
hydro.update(
    from_="Table_1",
    columns=["name", "age"],
    where="name = James",
    with_values=["Caio", 19],
)
```
```json
// Expectd result
{
  "TABLE NAME": "TABLE_1",
  "META DATA": null,
  "TABLE COLUMNS": [
    "name",
    "age"
  ],
  "PK": "name",
  "ROWS": [
    {
        "id": 1,
        "values":{
            "name": "Caio",
            "age": 19
        }
    }
  ]
}
```

- `table_name`:str --> Is the table to update a row, or a group of rows.

- `columns`:list --> These are the list you want to change of each row querried.

- `where`:str --> Specifies the groupe of elements or a single element to be updated.

- `with_values`:list --> The values to be updated to the current row data.


### delete() --> `delete`

This function removes an entire row from the table that has the specified value passed in.

```python
hydro.delete(
    from_="Table_1",
    where="id = 1"
)
```
```json
// Expected result
{
  "TABLE NAME": "TABLE_1",
  "META DATA": null,
  "TABLE COLUMNS": [
    "name",
    "age"
  ],
  "PK": "name",
  "ROWS": []
}
```

- `from_`: str --> Is the table to search the row.

- `where`: str --> pecifies the groupe of elements or a single element to be updated.


## Observable Functions
Those are mede to access general data fro the table, like the entire table structure, or the table's rows

### read_table()
This function returns the entire table structure. To use this functions just pass the table name.
```python
hydro.read_table(table_name="TABLE_1")
```
```bash
#Expected output

'{"TABLE NAME": "TABLE_1", "META DATA": null, "TABLE COLUMNS": ["name", "age"], "PK": "name", "ROWS": [{"id": 1, "values":{ "name": "Caio","age": 19}}]}'
```

- `table_name`:str -->Inte the table's name to me readed


### read_rows()
This function returns the entire list of rows in the table, to use, just pass the table's name.

```python
hydro.read_rows(table_name="TABLE_1")
```
```bash
# Expected output as the 'TABLE_1' only has this row
'[{"id": 1, "values":{"name": "Caio","age": 19}}]'
```

- `table_name`:str -->Inte the table's name to me readed


### read_columns()
Used to get the columns in the table. Important to say that ir does not returns data from the rows, just the name of the columns in the table.


```python
hydro.read_columns(table_name="TABLE_1")
```
```bash
# Expected output as the 'TABLE_1' only has those columns
'["name", "age"]'

```
- `table_name`:str -->Inte the table's name to me readed
