import asyncio

async def delete_message_after_delay(message, delay):
    await asyncio.sleep(delay)
    await message.delete()