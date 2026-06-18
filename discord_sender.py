from discord_webhook import DiscordWebhook

WEBHOOK_URL = "https://discord.com/api/webhooks/1517223073131004054/wrPjn2VPPMqtqwA49P2r1nr8N4X51iriPWEOk_Rwr2VLy2Z1pSo4YI55i5aLfdtSGM1M"

def send_message(msg):
    webhook = DiscordWebhook(
        url=WEBHOOK_URL,
        content=msg
    )
    webhook.execute()
