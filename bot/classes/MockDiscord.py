import asyncio

class MockDiscordMsg:
    def __init__(self, content, *, author, channel, guild):
        self.content = content
        self.author = MockAuthor(author.nick, author.id)
        self.channel = MockChannel( channel.name, channel.id )
        self.guild = MockGuild(guild.name, guild.id)

class MockAuthor:
    def __init__(self, name, id):
        self.name = name
        self.id = id  # Mock user ID

class MockChannel:
    def __init__(self, name, id):
        self.name = name
        self.id = id  # Mock channel ID

    async def send(self, content):
        print(f"Mock Channel Send: {content}")  # Simulating bot message

class MockGuild:
    def __init__(self, name, id):
        self.name = name
        self.id = id  # Mock server IDa