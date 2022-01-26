# Softdesk REST API

This project is Django REST API an issue tracking app for all three platforms (website, Android and iOS apps).
The app allow users to create various projects, add users to specific projects, create issues within projects, and assign labels to those issues based on their priorities, tags, etc and to add comments on the issues.

![alt text](https://images.unsplash.com/photo-1512758017271-d7b84c2113f1?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1470&q=80)

### Download

Download the project from github
```bash
  git clone https://github.com/NathanBnvn/Projet_10_Softdesk_API.git

```

### Prerequisites

Create a virtual environment
on Mac & Linux :
```bash
    $ python -m venv env
    $ source env/bin/activate

```
under Windows :
```bash
    py -m venv env
    .\env\Scripts\activate

```


To make it easier, install the necessary modules:
```bash
  pip install requirement.txt
```


### Launching

```bash
  $ python manage.py runserver
```

The API is not hosted and runs locally.
Once the server is launched, enter in Postman or likewise program, the generated url in the terminal:
http://127.0.0.1:8000/
