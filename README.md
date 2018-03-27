# wunderlist-sample

Basic API that allows users to create and modify lists in Wunderlist.

## Important

This was developed using Python 3.6.4 and the latest version of Flask. Compatibility with earlier versions of Flask is not guaranteed. More importantly, **COMPATIBILITY WITH PYTHON 2.x IS NOT GUARANTEED**.

## Installation
1. Set up a python virtual environment.

```
pip install virtualenv
virtualenv env_app (replace with whatever you want to name it)

EITHER
source env_app/bin/activate
OR
. env_app/bin/activate

python -m pip install -r requirements.txt
```

2. Obtain a Client ID and Client secret by signing up for a [Wunderlist developer account](https://developer.wunderlist.com) and creating an app there. 

3. Set the App URL to 'http://127.0.0.1:5000/' and the Auth Callback URL to 'http://127.0.0.1:5000/callback/wunderlist'.

4. In config.json, replace the strings in Client ID and Client secret with the values you got.

5. Run the script, fire up your web browser and enter 'http://127.0.0.1:5000'.
```
python wunderlist_sample.py
```

6. Available end-points:  
    * **GET** /user_info: Information about current user.
    * **GET** /user_lists: Current user's lists.
    * **POST** /user_lists: Create a new list.
    * **GET** /tasks/list_id=<list_id>&completed=<completed>: Get tasks in a list with id <list_id> that are either completed (<completed>=True) or not (<completed>=False).
    * **POST** /tasks/list_id=<list_id>&completed=<completed>: Create a new task. See [Wunderlist API](https://developer.wunderlist.com/documentation/endpoints/task) for required fields.


