import json

class BotConfig:
    def __init__(self, conversee=None, last_sender=None, current_status='Off', model='gpt-3.5-turbo', in_voice=False, voice_client=None, tts=False, tts_upgrade=False, moderation=False):
        self.conversee = conversee
        self.last_sender = last_sender
        self.current_status = current_status
        self.model = model
        self.in_voice = in_voice
        self.voice_client = voice_client
        self.tts = tts
        self.tts_upgrade = tts_upgrade
        self.moderation = moderation
    
    def __str__(self):
        return f'BotConfig(conversee={self.conversee}, last_sender={self.last_sender}, current_status={self.current_status}, model={self.model}, in_voice={self.in_voice}, voice_client={self.voice_client}, tts={self.tts}, tts_upgrade={self.tts_upgrade}, moderation={self.moderation})'

    def __dict__(self):
        return {'conversee': self.conversee, 'last_sender': self.last_sender, 'current_status': self.current_status, 'model': self.model, 'in_voice': self.in_voice, 'voice_client': self.voice_client, 'tts': self.tts, 'tts_upgrade': self.tts_upgrade, 'moderation': self.moderation}
    
    def create_from_dict(d):
        return BotConfig(d['conversee'], d['last_sender'], d['current_status'], d['model'], d['in_voice'], d['voice_client'], d['tts'], d['tts_upgrade'], d['moderation'])
