import os
import io
from datetime import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from billing.utils import generate_daily_billing_summary
import asyncio
import threading

from billing.Telegram import send_document_async




class Command(BaseCommand):
    help = 'Sends the daily billing summary to a specific Telegram user'


    def handle(self, *args, **kwargs):
        buffer = generate_daily_billing_summary()
        filename = f"billing_summary_{timezone.now().strftime('%d-%m-%Y')}.pdf"
        caption = f"Billing Summary for {timezone.now().strftime('%d-%m-%Y')}"

        def run_async_task():
            asyncio.run(send_document_async(buffer, filename, caption))

        # Run the async task in a separate thread
        thread = threading.Thread(target=run_async_task)
        thread.start()
        thread.join()

        self.stdout.write(self.style.SUCCESS('Successfully sent the summary to the Telegram user.'))
