class BotConfig:
    def __init__(self, recipient_id=None, sender_id=None, current_status='Off', model='gpt-3.5-turbo', in_voice=False, voice_client=None, tts=False, tts_service='google', moderation=False):
        self.recipient_id = recipient_id
        self.sender_id = sender_id
        self.current_status = current_status
        self.model = model
        self.in_voice = in_voice
        self.voice_client = voice_client
        self.tts = tts
        self.tts_service = tts_service
        self.moderation = moderation
    
    def __str__(self):
        return f'BotConfig(recipient_id={self.recipient_id}, sender_id={self.sender_id}, current_status={self.current_status}, model={self.model}, in_voice={self.in_voice}, voice_client={self.voice_client}, tts={self.tts}, tts_service={self.tts_service}, moderation={self.moderation})'

    def __dict__(self):
        return {'recipient_id': self.recipient_id, 'sender_id': self.sender_id, 'current_status': self.current_status, 'model': self.model, 'in_voice': self.in_voice, 'voice_client': self.voice_client, 'tts': self.tts, 'tts_service': self.tts_service, 'moderation': self.moderation}
    
    def create_from_dict(d):
        return BotConfig(d['recipient_id'], d['sender_id'], d['current_status'], d['model'], d['in_voice'], d['voice_client'], d['tts'], d['tts_service'], d['moderation'])