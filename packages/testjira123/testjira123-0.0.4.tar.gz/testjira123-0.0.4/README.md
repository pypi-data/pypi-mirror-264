# Jira Personal Bug tracker

The goal of this project is to help quality engineers to create/manage the status of their bug tickets

In the first part of the project, your goal will be to create a terminal program to manage bug tickets for the bug you found out.
To start, just save the bug ticket in a list (the list will only be active when the program is running).

In the second part, we integrate our program with the JIRA REST API.
So that, you can create JIRA bug tickets using your terminal program.
You will have to explore the Jira Rest API Documentation to find which endpoints to use in order to perform the following operations:
create a bug ticket, edit a bug ticket, delete a bug ticket, list bug tickets I created.

I have already setup a JIRA instance for us.
I will provide you the api/organisation key by email directly.

The project will contain the following terminal screens.

#### Main Menu

```
****************************
Welcome to MyBugTracker v1.0
****************************

Select the option of your choice to start
[1] - Print my bug tickets
[2] - Create a bug ticket
[3] - Edit a bug ticket
[4] - Delete a bug ticket
[5] - Exit

```

#### Print my bug tickets

```
::::::::::::::::
Print my bug tickets
****************

Select 5 to return to the menu
_______________________________________________________________________
| ID | Title          | Created Date  | Status             | Assignee |         |
-----------------------------------------------------------------------
| ...| ...............| ..............|...................|...........|
| ...| ...............| ..............|...................|...........|
|____|________________|_______________|___________________|___________|
```

#### Add a bug ticket
 
```
::::::::::::::::
Add a client
****************

Select 5 to return to the menu

Title:
>> Jenkins build pipeline not working
Description :
>> Jenkins build pipeline not triggered when pushing to the repository of SuperImportant project
Priority :
>> High

!! Bug ticket added !!

```

#### Edit a bug ticket
 
```
::::::::::::::::
Edit a bug ticket
****************

Select 5 to return to the menu

Choose an bug ticket ID for updating :
>> 10
[Bug ticket found]
Let blank if no change
Description [Jenkins build pipeline not triggered when pushing to the repository of SuperImportant project] :
>>
Priority [High]:
>> Low

!! Bug ticket updated !!
```

#### Delete a bug ticket

```
::::::::::::::::
Delete a bug ticket
****************

ID of the bug ticket to remove :
>> 10
Bug ticket to delete not found
>> 1
Bug ticket deleted
```
