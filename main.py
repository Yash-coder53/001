import asyncio
import time
from telethon import TelegramClient, events
from telethon.tl.types import Message
from config import Config
from blackboxai import BlackboxAI

class TelegramAutoChat:
    def __init__(self):
        self.client = TelegramClient(
            Config.SESSION_NAME,
            Config.API_ID,
            Config.API_HASH
        )
        self.blackbox = BlackboxAI()
        self.last_response_time = {}
        self.active_chats = set()
        
        # Register event handlers
        self.client.on(events.NewMessage)(self.handle_message)
        
    async def start(self):
        """Start the auto-chat client"""
        await self.client.start()
        print("Auto-chat bot started!")
        print("Logged in as:", (await self.client.get_me()).first_name)
        
        # Get all dialogs and print them
        async for dialog in self.client.iter_dialogs():
            print(f"{dialog.name} (ID: {dialog.id})")
        
        await self.client.run_until_disconnected()
    
    async def handle_message(self, event):
        """Handle incoming messages"""
        try:
            # Ignore messages from ourselves
            if event.message.out:
                return
            
            # Get chat ID and sender info
            chat_id = event.chat_id
            sender = await event.get_sender()
            message_text = event.message.text or ""
            
            # Ignore empty messages or commands
            if not message_text.strip() or message_text.startswith('/'):
                return
            
            print(f"Received message in {chat_id} from {sender.first_name}: {message_text[:50]}...")
            
            # Rate limiting: Only respond once every 30 seconds per chat
            current_time = time.time()
            last_time = self.last_response_time.get(chat_id, 0)
            
            if current_time - last_time < 30:
                return
            
            # Generate response using Blackbox AI
            response = self.blackbox.generate_response(message_text)
            
            if response and not response.startswith("Error:"):
                # Send the response
                await event.reply(response[:Config.MAX_MESSAGE_LENGTH])
                print(f"Sent response: {response[:100]}...")
                
                # Update last response time
                self.last_response_time[chat_id] = current_time
                
                # Add delay between responses
                await asyncio.sleep(Config.RESPONSE_DELAY)
                
        except Exception as e:
            print(f"Error handling message: {e}")

async def main():
    """Main function to start the bot"""
    bot = TelegramAutoChat()
    await bot.start()

if __name__ == "__main__":
    asyncio.run(main())
