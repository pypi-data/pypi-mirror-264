import os

from anthropic import Anthropic
from openai import OpenAI

from PIL import Image

from shanu.ai import prompts


class LLM:
    def __init__(self):
        if not all(
            [
                "OPENAI_API_KEY" in os.environ,
                "ANTHROPIC_API_KEY" in os.environ,
            ]
        ):
            raise Exception(
                "Please set the OPENAI_API_KEY and"
                " ANTHROPIC_API_KEY environment variables."
            )
        self.openai_client = OpenAI()
        self.anthropic_client = Anthropic()

    def text_to_text(
        self,
        prompt,
        system_message="You are a helpful assistant.",
        provider="openai",
        model="gpt-3.5-turbo",
        temperature=0.7,
        max_tokens=4096,
        response_format=None,
    ):
        if provider == "openai":
            response = self.openai_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt},
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                response_format=response_format,
            )
            response = response.choices[0].message.content
        elif provider == "anthropic":
            response = self.anthropic_client.messages.create(
                model=model,
                system=system_message,
                messages=[
                    {"role": "user", "content": prompt},
                ],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            response = response.content[0].text
        return response

    def text_to_audio(self, text, file_path, model="tts-1", voice="onyx"):
        response = self.openai_client.audio.speech.create(
            model=model,
            voice=voice,
            input=text,
        )
        response.stream_to_file(file_path)

    def audio_to_text(self, file_path, model="whisper-1"):
        with open(file_path, "rb") as audio_file:
            transcription = self.openai_client.audio.transcriptions.create(
                model=model, file=audio_file
            )
        return transcription.text

    def text_to_image(
        self,
        text,
        model="dall-e-3",
        image_size="1024x1024",
        image_quality="standard",
        total_images=1,
    ):
        allowed_image_sizes = ["1024x1024", "1024x1792", "1792x1024"]
        if image_size not in allowed_image_sizes:
            raise Exception(
                f"Invalid image size. Please select from {allowed_image_sizes}"
            )
        response = self.openai_client.images.generate(
            model=model,
            prompt=text,
            size=image_size,
            quality=image_quality,
            n=total_images,
        )
        return [response.data[i].url for i in range(total_images)]

    def image_to_text(
        self, text, image_url, model="gpt-4-vision-preview", max_tokens=4096
    ):
        response = self.openai_client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": text},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url,
                            },
                        },
                    ],
                }
            ],
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content

    def image_to_image_via_variation(
        self,
        image_file_path,
        model="dall-e-2",
        image_size="1024x1024",
        total_images=1,
    ):
        allowed_image_sizes = ["1024x1024", "512x512", "256x256"]
        if image_size not in allowed_image_sizes:
            raise Exception(
                f"Invalid image size. Please select from {allowed_image_sizes}"
            )
        with open(image_file_path, "rb") as image_file:
            response = self.openai_client.images.create_variation(
                image=image_file,
                model=model,
                n=total_images,
                size=image_size,
            )
        return [response.data[i].url for i in range(total_images)]

    def image_to_image_via_edit(
        self,
        prompt,
        image_file_path,
        mask_image_file_path=None,
        model="dall-e-2",
        image_size="1024x1024",
        total_images=1,
    ):
        allowed_image_sizes = ["1024x1024", "512x512", "256x256"]
        if image_size not in allowed_image_sizes:
            raise Exception(
                f"Invalid image size. Please select from {allowed_image_sizes}"
            )

        img = Image.open(image_file_path)
        if img.mode == "RGB":
            img.convert("RGBA").save(image_file_path)

        with open(image_file_path, "rb") as main_image:
            if mask_image_file_path:
                with open(mask_image_file_path, "rb") as mask_image:
                    response = self.openai_client.images.edit(
                        image=main_image,
                        prompt=prompt,
                        model=model,
                        mask=mask_image,
                        size=image_size,
                        n=total_images,
                    )
            else:
                response = self.openai_client.images.edit(
                    image=main_image,
                    prompt=prompt,
                    model=model,
                    size=image_size,
                    n=total_images,
                )
        return [response.data[i].url for i in range(total_images)]


class LLMWrapper(LLM):
    def __init__(self):
        super().__init__()

    def image_to_image(
        self, input_image_url, more_freedom=False, print_descriptions=True
    ):
        description = self.image_to_text(
            prompts.DESCRIBE_IMAGE, input_image_url
        )
        if print_descriptions:
            print("Description from I2T\n", description)
        if more_freedom:
            description = self.text_to_text(
                f"{prompts.UPDATE_IMAGE_DESCRIPTION}:\n\n{description}",
                prompts.UPDATE_IMAGE_DESCRIPTION_SYSTEM,
            )
            if print_descriptions:
                print("Description from T2T\n", description)
        return self.text_to_image(description)[0]
