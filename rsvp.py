# RSVP
#
# Who's invited? In alphabetical order,
# or in order of who registered first.
#
# For each person, details: have they RSVP'd?
# Do they have a +1?
#
# Be able to add a person to a blacklist,
# and when somebody tries to add them, they
# should not be allowed to.
#
# Were they present? And automatically track time
# of arrival and departure.
#
# First point in time when at least 50% were present.
#
# After the event is over, say who didn't show up.

import datetime
from flask import Flask, render_template

app = Flask(__name__)

class Guest:
    def __init__(self, _name, _age, _gender, _check_in):
        self.name = _name
        self.age = _age
        self.gender = _gender
        self.check_in = _check_in
        self.plus_one = None

    def add_plus_one(self, _plus_one):
        self.plus_one = _plus_one


guests = [
    Guest(_name="Artyom", _age=23, _gender="m", _check_in=datetime.datetime.now()),
    Guest(_name="Jason", _age=90, _gender="m", _check_in=datetime.datetime.now()),
]
plus_ones = []


# Add a new guest to the list
def request_add():
    name = input("Name? ")
    age = int(input("Age? "))
    gender = input("Gender? ")
    if gender in {"m", "f"}:
        guests.append(Guest(_name=name, _age=age, _gender=gender, _check_in=datetime.datetime.now()))
    else:
        print("Gender has to be 'm' or 'f'")


# Print the list of all guests
def request_list():
    for guest in guests:
        if guest.plus_one is None:
            print(guest.name, str(guest.age) + "y.o.", guest.gender, "{:%H:%M}".format(guest.check_in))
        else:
            print(guest.name, str(guest.age) + "y.o.", guest.gender, "{:%H:%M}".format(guest.check_in),
                  "+" + guest.plus_one)


# Add a +1 to a guest
def request_plus1():
    guest_name = input("Who gets the +1?")
    inviters = [x for x in guests if x.name == guest_name]
    if len(inviters) == 0:
        print("Guest not found")
    elif len(inviters) > 1:
        print("Ambiguous guest :/")
    else:
        inviter = inviters[0]
        name = input("+1's name? ")
        age = int(input("+1's age? "))
        gender = input("+1's gender? ")
        inviter.add_plus_one(name)
        plus_ones.append(Guest(_name=name, _age=age, _gender=gender, _check_in=None))

@app.route("/")
def template_test():
    return render_template('template.html', guests=guests)

# while True:
#     command = input("Command? ")
#     if command == "add":
#         request_add()
#     elif command == "list":
#         request_list()
#     elif command == "+1":
#         request_plus1()
#     else:
#         print("Unknown command", command)

"""
> help
Guest list:
    * guests by name
    * guest by status
    * no-shows
    
Guest status:
    * add [guest name]
    * remove [guest name]
    * rsvp [guest name]
    * check in [guest name]
    * check out [guest name]

> add Jenny
+1: no

> rsvp Jenny
Done

> guests by status
    * Bob                -
    * Candy (+1)         -
    * Jenny              RSVP'd
    * Charles (+1)       checked in (18:23)
    * Alice              checked out (17:10 - 19:30)

> guests by name
    * Alice              checked out (17:10 - 19:30)
    * Bob                -
    * Candy (+1)         -
    * Charles (+1)       checked in (18:23)
    * Jenny              RSVP'd

> rsvp Freddie
Freddie is not on the guest list

> check in Jenny
OK

> check out Jenny
OK

> no-shows
    * Bob
    * Candy
"""
