# Time and Information in Bargaining - Experiment 

This repository contains the code for the experiment we are running as part of a paper called "Time and Information and Bargaining."

Corresponding Developer: 
Nicolas Roever (University of Cologne) 
Email: nicoroever@gmail.com 

## Quick Start Guide

If you haven't already cloned the repository, do so with the following command:

```bash
git clone https://github.com/your-username/your-repository.git
cd your-repository
```
Download the environment by navigating to the directory containing your environment.yml file. Then run:
```bash
conda env create -f environment.yml
conda activate bargaining
```

Then you can run the app locally by typing:
```bash
otree devserver
```
Just open any browser and navigate to *http://localhost:8000* to see the app. 



## General Information

The experiment is written using oTree livepages. I consider this code to be a very good example of how to implement a livepage following best practices of functional programming and unit testing. 

The core components of the code are: 

- bargain_live/__init__.py: This file is the standard file for oTree apps and has the standard structure (see the section below)

- bargain_live/Bargain.html: This file has two components: The first part is HTML/CSS code sets the user interface and the seconf part is javascript code which dynamically updates parts in the HTML/CSS (see section below)

## How Dynamic Live Pages with oTree Work 

Live-Pages have two types of code: (1) There is python code which is run by the server. (2) There is HTML, CSS, and JavaScript code, which is run by the client. As proposed in the documentation, all major computations are done on the server side, while the client-code only adapts the user interface.

### The Python Code

There are some functions which have special functionalities when using the oTree library: 

- vars_for_template: This function is triggered when the page is first loaded. It allows to define static variables in python which can be accessed directly in the HTML of the client. 

> With static, I mean variables which are constant over the entire round of the bargainng game.

- js_vars: his function is triggered when the page is first loaded. It allows to define static variables in Python which can be accessed in the javascript code of the client.

- live_method: This function is triggered **on the server** whenever a liveSend() is called in the client javascript code. All information sent from the server is stored and can be accessed from a dictionary called **data** (this is defined in the oTree package). The live method returns a dictionary to the server which I called **broadcast**

### The JavaScript Code

There are also functions here  which have special functionalities when using the oTree library: 

- The liveSend() object sends information from client to server and triggers the live_method function() on the server side

- liveRecv(data) is triggered whenever the server-side live_method() function is executed. It takes the dictionary sent from the live_method() as an argument (which is once again called data in the client-side code). This exact dictionary is called broadcast in the server-side code!


## The file bargain_live/__init__.py

This file is the standard file for oTree apps and follows the proposed structure from the documentation: I define global classes in the first part of the script, which initializes the SQL-database fields (2) I define the function creating_subsessions, which is run whenever two players are matched in a round and (3) I define all pages in the app as classes

## A Note on the Implementation of Functional Programming Principles 

Within the contraints of the oTree packages, I attempted to make the code as functional as possible:
- All javascript functions are written in the file *_static/bargaining_functions.js*. The corresponding unit-tests are in *tests/bargaining_functions.test.js*. I use the jest package to test the javascript functions.

- The python functions are in *bargain_live/bargaining_functions.py* and the corresponding unit-tests are in *tests/test_bargining_functions.py*. I use the pytest package to test the python functions. 

While some of the functions are quite long as they carry special functionalities in oTree (i.e. liveRecv()), I think I did a really good job at writing the code as functional and humanly readable as possible. Let me know what you think!

## Current Open Questions and To-Do's

This section is only for me as a developer. You can ignore it. 

- I need to fix that the total bargaining time is not correctly recorded.

- The final payoffs seem to be incorrect, also make sure that they are stored in the database.

- What is fixed over the entire session and what is changing each round (Player/Seller Role, Valuation)?

- I would recommend not having a valuation of 0 for the seller, because people are confused by that






