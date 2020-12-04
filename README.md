# Bocconi Library Group Room
Automatic script to reserve a group studyroom with a week of advance.

First, run `pip install -r requirements.txt` to install selenium.

Second, create a _credentials_bb.json_ file in the folder with two parameters, "username" and "password", to login into Blackboard.

Then by running `python library_room.py`
you will book a room for the following week on the same weekday and at the same time of the run. More options will come out soon.

If the reservation is successful, you'll receive an email, otherwise a failure message is dislayed.
