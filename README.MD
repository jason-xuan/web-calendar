# calendar

## team members

* Jason Zhu, 467138
* Zexi Liu, 467319

## Additional Details

project URL:

<http://ec2-52-14-93-16.us-east-2.compute.amazonaws.com:8080/>

## Creative Portion

1. Users can tag an event with a tag and enable/disable those tags in the calendar view.
2. Users can unregister their account, which would automatically delete all events they create
3. All web api and server-side code are completely under unittest

## requirements.txt
1. all packages are listed in requirements.txt, you can create a python virtualenv and install all of them.
2. the python version should be 3.6

## python unittest
* you can run all unittests with command below, and remember the env requirement.
* Since there are a ORM framework as a abstract layer, in unittest we can use sqlite file database instead the product database.
```bash
python3 -m unittest discover -v
```
