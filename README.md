<h1 align="center"">Adsgram analytics parser</h1>
<p align="center">
  <img width="1000" height="400" src="https://i.ibb.co/gFGYzYT/ADSGRAM.jpg">
</p>


#### How the software works:

1. Log in to the site traffic.adsgram.ai .
2. Get active active campaigns for yesterday 
3. Get utm-link and csv data for each active campaign for yesterday. The data is taken by country. 
4. Processes the data, compiles and sends it as a single file to PostgreSQL.
5. Also sends an alert to you via telegram about the results of the work.
---
> _If you have any questions about installation and modification, or you just want to express respect to the author, then you can write directly to telegram: [@anmendel]_

---

## Installing the code:
#### 1. Download the repository and install requirements:
```sh
git clone https://github.com/czbag/starknet.git

cd starknet

pip install -r requirements.txt

# Before you start, configure the required modules in /auth_data/...

python main.py
```
#### 2. Configure an adsgram username and password:

```
2.1. Open /auth_data/adsgram.py
2.2. Change the login and password variables to your own
```
#### 3. Configure an PostgreSQL params:

```
3.1. Open /auth_data/postgresql.py
3.2. The "connect" block is responsible for connecting to the Postresql database
3.3. The "table" block is responsible for the path to the table where the results of the work will be saved. You don't have to change anything here.
```
---
## Advanced Settings (if you need):

#### 4. Create and configure a telegram bot for convenient alerts:


##### 4.1 Create a bot:

```
4.1.1. Open https://t.me/BotFathe
4.1.2. Send a command /newbot
4.1.3. Choose a name for your bot
4.1.4. Choose a @username_bot for your bot
4.1.5. Copy and Save "Token to access the HTTP API". Example: "754618664071:AsdFn-safasfSFAFASFsda-ScM_QE8WNasdf59"
```
##### 4.2 Create and configure a telegram chat for alerts:

```
4.2.1. Create a telegram chat for alerts
4.2.2. Add your @username_bot to the chat 
4.2.3. Add @myidbot to the chat 
4.2.4. Send a chat command /getgroupid
4.2.5. Copy and Save "You group ID". Example: "-2145124124"
```
##### 4.3 Connecting the bot to our parser:

```
4.3.1. Open /auth_data/tg_alert_bot.py
4.3.2. Turn on the telegram bot: is_tg_alert_enabled = True. 
4.3.3. tg_access_token = "Token to access the HTTP API" (Paragraph 4.1.5)
4.3.4. tg_chat_id = "You group ID" (Paragraph 4.2.5)
4.3.5. tg_support_account = your telegram username 
```
##### 5. Setting up UTM Copying:

```
1. Open /parse_url.py
2. The function takes the utm-link in the format: 'https://t.me/Bcoin2048bot/app?startapp=utm_adsgram_tele40'. You need to write your own function that will parse 'utm_adsgram_tele40' from the link.
```

[//]: # 
   [@anmendel]: <https://t.me/anmendelr>
   [@BotFather]: <https://t.me/BotFather>
