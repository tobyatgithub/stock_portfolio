# stock_portfolio

**Author**: Toby  
**Version**: 1.0.0  

## Overview
<!-- Provide a high level overview of what this application is and why you are building it, beyond the fact that it's an assignment for a Code Fellows 401 class. (i.e. What's your problem domain?) -->
In this project, I build an application that consumes data from a 3rd party API and provides our users with the ability to create stock portfolios. Once I’ve built the basic functionality of the application, I’ll introduce data analysis and visualizations into the application so I can analyze based on historical data!  

## Getting Started
<!-- What are the steps that a user must take in order to build this app on their own machine and get it running? -->
First, build a virtual environment for python 3.6 and install Flask, and request.  
Go to the directory and run
```bash
flask run
```
to activate server. Go to the address showed on screen after server gets activated.  

## Architecture
<!-- Provide a detailed description of the application design. What technologies (languages, libraries, etc) you're using, and any other relevant design information. This is also an area which you can include any visuals; flow charts, example usage gifs, screen captures, etc.-->
You will need flask, requests, and python 3.6 to run the code.  


## API
<!-- Provide detailed instructions for your applications usage. This should include any methods or endpoints available to the user/client/developer. Each section should be formatted to provide clear syntax for usage, example calls including input data requirements and options, and example responses or return values. -->
Right now we are using API from iextrading (https://iextrading.com/developer/docs/#collections)  
To get company detail info, the format is https://api.iextrading.com/1.0/stock/ + {stock name} + /company   

## Change Log
<!-- Use this are to document the iterative changes made to your application as each feature is successfully implemented. Use time stamps. Here's an example:-->

12/5/18 5pm, first function on.
12/5/18 8pm  committed....but stucked on second function. A bit confused /..\
