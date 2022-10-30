from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError, ChatAdminRequiredError, ChatWriteForbiddenError
from time import sleep
from os import listdir
from datetime import datetime
from os.path import isfile, join
print(datetime.now().timestamp())
api_id = 6043455  # mm
api_hash = 'f22b604a9dcd2e139737bdd9a76f09ca'  # mm

print('All rights reserved, created by Telegram - @razentyler10\n')
print('there must be group_list.txt file where you can write every group that must receive the message'
      '\nif the account not a member of some group the message won\'t be sent'
      '\nwrite groups like this @group_username every new group in new line\n')
phone = input('Enter your phone number: ')
client = TelegramClient(phone, api_id, api_hash)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))

time = int(input('Input interval in second: '))

onlyfiles = [f for f in listdir('.') if isfile(join('.', f))]


if (str(phone)+'.txt') not in onlyfiles:
    with open(str(phone)+'.txt', 'w', encoding='utf-8') as f:
        f.write('Enter your message here')
        f.close()


if ('group_list.txt') not in onlyfiles:
    with open('group_list.txt', 'w') as f:
        f.write('@group_usename')
        f.close()

with open(str(phone)+'.txt','r', encoding='utf-8') as fr:
    message = fr.read()
    fr.close()


print('\ncheck the group_list.txt if its correct\nand be sure that correct message in '+str(phone)+f'.txt\nthe message is:  {message}\n\npress Enter to continue\nif not, change it and press Enter')
input()

print('Great, the script is working....')
while True:
    with open(str(phone) + '.txt', 'r', encoding='utf-8') as fr:
        message = fr.read()
        fr.close()
    with open('group_list.txt','r') as groups:
        for group in groups.readlines():
            try:
                client.send_message(group,message)
            except PeerFloodError as p:
                print("Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
                print('sleep 120 second')
                sleep(120)
            except UserPrivacyRestrictedError:
                print("The user's privacy settings do not allow you to do this. Skipping.")

            except ChatWriteForbiddenError:
                try:
                    client(JoinChannelRequest(group))
                    client.send_message(group, message)
                    print('sleep 300 second after joining the group')
                    sleep(300)
                except:
                    pass
            except ChatAdminRequiredError:
                pass
            except ValueError:
                pass
            except:
                pass

    sleep(time)