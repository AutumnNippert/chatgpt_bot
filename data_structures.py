import json

class BotConfig:
    def __init__(self, conversee=None, last_sender=None, current_status='Off', model='gpt-3.5-turbo', in_voice=False, voice_client=None, tts=False, tts_upgrade=False):
        self.conversee = conversee
        self.last_sender = last_sender
        self.current_status = current_status
        self.model = model
        self.in_voice = in_voice
        self.voice_client = voice_client
        self.tts = tts
        self.tts_upgrade = tts_upgrade
    
    def __str__(self):
        return f'BotConfig(conversee={self.conversee}, last_sender={self.last_sender}, current_status={self.current_status}, model={self.model}, in_voice={self.in_voice}, voice_client={self.voice_client}, tts={self.tts}, tts_upgrade={self.tts_upgrade})'

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)