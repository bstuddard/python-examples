from pydantic import BaseModel


class ChatInput(BaseModel):
    chat_input_list: list

    class Config:
        json_schema_extra = {
            "example": {
                "chat_input_list": [
                    {
                        "role": "user",
                        "message": "What is your name?"
                    },
                    {
                        "role": "assistant",
                        "message": "My name is Claude"
                    }
                ]
            }
        }