
# T-Order mailing system

Ever wonder how T-Order mails when products arrive at the store? We do it by hand ofc.

With this system, "Kha lé" can mails the customer faster and more efficient.

I used Telegram for easy usage




## Features

- Send emails through Telegram
- Can send in bulk


## Installation

Clone this repo to your computer

```bash
  cd torder-mailing-system
pip install requirements.txt
```
Your Outlook email needs to be enabled with SMTP Authentication for this to work.
    
## Environment Variables

To run this project, you will need to create .env file and add the following environment variables:

`TELEGRAM_BOT_TOKEN`

`OUTLOOK_PASSWORD`

`TELEGRAM_GROUP_ID`

`OUTLOOK_MAIL`


## Deployment

To deploy this project run

```
py mail.py
```


## Usage
```
/send "product" "mail1@gmail.com" "mail2@gmail.com"
```


## Screenshots

![App Screenshot](https://media.discordapp.net/attachments/1040945390079455244/1351589298784309408/image.png?ex=67daed20&is=67d99ba0&hm=a588d6d34cef81a52d57bf5690863b949327ad578f153778642d823c673fcdf5&=&format=webp&quality=lossless)


## Support


The group id can be get by "to be filled" (im too lazy to add in, just ask the ai).


## Related

I also included files to be built on Docker, just remember to protect your .env if you use any public host.



## Authors

- [@whoismaiko](https://www.github.com/whoismaiko)
- DeepSeek for all the hardwork.
