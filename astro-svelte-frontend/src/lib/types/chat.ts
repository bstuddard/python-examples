export interface ChatMessage {
    role: 'user' | 'assistant';
    message: string;
    timestamp: Date;
}

export interface ChatInputPayload {
    chat_input_list: ChatMessage[];
} 