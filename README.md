# 刷 VFS 签证预约名额的脚本

Fork 的项目，并根据我的需求进行修改：
+ 增加时间限制，只在有早于特定日期的名额时才通知（config.ini 里设置）
+ 增加了系统通知功能（目前只实现了 macOS 系统通知，其他系统如有需要可修改 vfs_appointment_bot/_SystemNotificationClient.py 中 show_notification 函数的相关部分）

我的一些经验：
+ 查询周期可以设得长一些，否则频繁访问可能被 ban
+ 程序经常出错退出，可以在命令行设置死循环等方式保证退出后自动重启
+ 可以先约一个时间比较靠后但能约到的，然后在刷到更早的名额后再修改时间，这样免去了重新填写信息的麻烦，速度更快
+ VFS 系统似乎有延迟，有时候刷到的名额已经被别人抢走了但显示还有。如果在最后一步付款或修改预约时间时显示遇到错误，大概就是已经被别人抢走了
+ 可以停留在修改预约时间的页面以便刷到名额后迅速操作。此外，为了保活，可以用自动点击类的工具定期在此页面点击
+ VFS 似乎会不定期放号，有些号的时间会很早，所以不要放弃，坚持刷，很可能刷到的

祝大家都能顺利拿到签证！
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
