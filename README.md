# README

## Quick-Start :rocket:

This repo contains two scripts:

- [`bot.py`](./bot.py): to be used on discord to check-in a user manually.
- [`bulk-assign.py`](./bot.py): to be used locally, to bulk check-in a list of users.

First install the requirements, with: 

```
pip install -r requirements.txt
```

Then create an environment variable for your BOT token with:

```
EXPORT BOT=[REPLACE THIS WITH YOUR DISCORD BOT TOKEN]
```

Choose your script, and run it.

### bot.py

Run:
```
python bot.py
```

On #staff-chat, check-in users with:

```
!assignrole "joana9321" "Attendee"
```

### bulk-assign.py

Create a csv list of discord usernames that you want to check-in: [usernames.csv](./usernames.csv)

Run:
```
python bulk-assign.py
```

Users will be assign the `Attendee` role, if they don't have it already. Then they will receive a DM stating they have been checked-in.

## License

This project is released under an [MIT License](./LICENSE)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
(dev-exercise-template)
