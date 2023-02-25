# VFS Germany Appointment Bot

A script to check the appointment slots.

By default, it runs every 2 minutes and check for visa slots at VFS website and notifies the user by SMS/call/Telegram. <br/>
The interval can be changed in the config.

## How to use
1. Clone the repo <br/>
2. Move into the repo: `cd vfs_appointment_bot` <br/>
3. Update the config file (`config/config.ini`) with VFS, Twilio, Telegram credentials. Note that you can use either telegram, or twilio, or both. This can be specified with `use_telegram` and `use_twilio` config flags in same file.
3. Create a new virtual environment: `python3 -m venv venv` or by using conda `conda create --name venv python=3.8`<br/>
4. Activate the environment (might differ a bit for windows and MacOS): `source venv/bin/activate` / `conda activate venv` <br/>
5. Install the dependencies: `pip install -r requirements.txt` <br/>
6. Run the script:

`python vfs_appointment_bot/vfs_appointment_bot.py '<vfs_centre>' '<visa_category>' '<visa_subcategory>'`

OR

`python vfs_appointment_bot/vfs_appointment_bot.py`

It will take the values as input from the user

** Please refer to the screenshot for more details regarding the inputs.

![VFS Appointment Form Screenshot](./assets/vfs-appointment-form.png)

## Dependency

1. Install Chrome Browser on your machine if not already installed.
2. `chromedriver`
3. Setup client for Twilio/Telegram or both:
    - Create an account on Twilio to get text and call alerts. Sign up [here](https://www.twilio.com/try-twilio) for a trial account to get credits upto worth $10, OR
    - Create a new bot via Telegram and add it to a chat group where you want it to post messages to notify you. Check [this simple tutorial out](https://medium.com/codex/using-python-to-send-telegram-messages-in-3-simple-steps-419a8b5e5e2) if you don't know how to create a new bot and get its credentials. Once bot is created you need to add its credentials in `config/config.ini` file.
