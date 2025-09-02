
from telethon import TelegramClient, functions
import asyncio
import time
import os

async def main():
    os.system("clear")
    print("====================================")
    print("   TELEGRAM GROUP CREATOR TOOL")
    print("   Developed by Captain")
    print("   Telegram: @inbox62")
    print("====================================\n")

   
    while True:
        api_id_input = input("Enter your API ID: ").strip()
        if api_id_input.isdigit():
            api_id = int(api_id_input)
            break
        print("⚠️ Invalid input! API ID must be a number.")

    api_hash = input("Enter your API Hash: ").strip()
    session_name = input("Enter session name (e.g., myaccount): ").strip()

    client = TelegramClient(session_name, api_id, api_hash)
    await client.start()

   
    while True:
        total_groups = input("How many groups to create today? (max 50): ").strip()
        if total_groups.isdigit() and 1 <= int(total_groups) <= 50:
            total_groups = int(total_groups)
            break
        print("⚠️ Enter a number between 1 and 50.")

    while True:
        messages_per_group = input("How many messages per group? (e.g., 5): ").strip()
        if messages_per_group.isdigit() and int(messages_per_group) > 0:
            messages_per_group = int(messages_per_group)
            break
        print("⚠️ Enter a valid number of messages.")

    while True:
        delay_min = input("Minimum delay between groups in minutes (min 5): ").strip()
        if delay_min.isdigit() and int(delay_min) >= 5:
            delay_min = int(delay_min)
            break
        print("⚠️ Delay must be at least 5 minutes!")

    group_prefix = input("Enter group name prefix (default 'CaptainGroup'): ").strip()
    if group_prefix == "":
        group_prefix = "CaptainGroup"

    message_template = input("Enter message template (use {i} for group name, {j} for message number):\n").strip()
    if message_template == "":
        message_template = "Auto message {j} in {i}"

    delay_seconds = delay_min * 60

    print(f"\nStarting creation of {total_groups} groups with {messages_per_group} messages each...")
    print(f"Delay between groups: {delay_min} minutes\n")

    
    for i in range(1, total_groups + 1):
        group_name = f"{group_prefix} {i}"

    
        try:
            result = await client(functions.messages.CreateChatRequest(
                users=["me"],
                title=group_name
            ))
        except Exception as e:
            print(f"❌ Failed to create {group_name}: {e}")
            continue

        
        group = None
        if hasattr(result, "chats") and len(result.chats) > 0:
            group = result.chats[0]
        else:
            dialogs = await client.get_dialogs()
            for d in dialogs:
                if d.name == group_name:
                    group = d.entity
                    break
        if group is None:
            print(f"❌ Could not find the created group {group_name}, skipping...")
            continue

        print(f"✅ Created {group_name}")

        
        try:
            invite = await client(functions.messages.ExportChatInviteRequest(peer=group))
            invite_link = invite.link
            print(f"🔗 Invite link for {group_name}: {invite_link}")
        except Exception as e:
            print(f"❌ Could not create invite link for {group_name}: {e}")

        for j in range(1, messages_per_group + 1):
            msg = message_template.replace("{i}", group_name).replace("{j}", str(j))
            await client.send_message(group, msg)
            time.sleep(1)  

        print(f"📩 Sent {messages_per_group} messages in {group_name}")

        
        if i != total_groups:
            print(f"⏳ Waiting {delay_min} minutes before next group...\n")
            time.sleep(delay_seconds)

    print("\n🎉 Finished! All groups created successfully.")
    print("====================================")
    print("   Tool by Captain (@inbox62)")
    print("====================================")

if __name__ == "__main__":
    asyncio.run(main())
