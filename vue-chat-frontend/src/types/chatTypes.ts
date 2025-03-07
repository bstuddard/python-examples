interface ChatMessage {
    role: string;
    message: string;
}

interface ChatInputPayload {
    chat_input_list: ChatMessage[];
}


export type { ChatMessage, ChatInputPayload };