from astro.client.openai import AsyncAstroClient, AstroClient
from astro.types import BaseMessage, StreamingChatResponse
from openai.types.chat import ChatCompletion


class TestStreaming:
    def test_chat(self):
        buffer = []
        client = AstroClient()
        response = client.generate_chat(
            messages=[BaseMessage(role="user", content="Hello!")],
            stream=True,
            stream_callback=lambda response: buffer.append(response),
        )
        assert isinstance(response, ChatCompletion)
        assert len(buffer) > 1
        assert all(isinstance(c, StreamingChatResponse) for c in buffer)
        assert buffer[-1].completion is response

    def test_providing_callback_turns_on_streaming(self):
        buffer = []
        client = AstroClient()
        response = client.generate_chat(
            messages=[BaseMessage(role="user", content="Hello!")],
            stream_callback=lambda response: buffer.append(response),
        )
        assert isinstance(response, ChatCompletion)
        assert len(buffer) > 1

    def test_can_turn_off_streaming_even_if_callback_provided(self):
        buffer = []
        client = AstroClient()
        response = client.generate_chat(
            messages=[BaseMessage(role="user", content="Hello!")],
            stream=False,
            stream_callback=lambda response: buffer.append(response),
        )
        assert isinstance(response, ChatCompletion)
        assert len(buffer) == 0


class TestStreamingAsync:
    async def test_chat(self):
        buffer = []
        client = AsyncAstroClient()
        response = await client.generate_chat(
            messages=[BaseMessage(role="user", content="Hello!")],
            stream=True,
            stream_callback=lambda response: buffer.append(response),
        )
        assert isinstance(response, ChatCompletion)
        assert len(buffer) > 1
        assert all(isinstance(c, StreamingChatResponse) for c in buffer)
        assert buffer[-1].completion is response

    async def test_providing_callback_turns_on_streaming(self):
        buffer = []
        client = AsyncAstroClient()
        response = await client.generate_chat(
            messages=[BaseMessage(role="user", content="Hello!")],
            stream_callback=lambda response: buffer.append(response),
        )
        assert isinstance(response, ChatCompletion)
        assert len(buffer) > 1

    async def test_can_turn_off_streaming_even_if_callback_provided(self):
        buffer = []
        client = AsyncAstroClient()
        response = await client.generate_chat(
            messages=[BaseMessage(role="user", content="Hello!")],
            stream=False,
            stream_callback=lambda response: buffer.append(response),
        )
        assert isinstance(response, ChatCompletion)
        assert len(buffer) == 0
