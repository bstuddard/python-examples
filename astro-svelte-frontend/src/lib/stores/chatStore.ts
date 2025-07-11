import { writable } from 'svelte/store';
import type { ChatMessage, ChatInputPayload } from '$lib/types/chat';

export const messages = writable<ChatMessage[]>([]);
export const isStreaming = writable<boolean>(false);
export const streamData = writable<string>('');
export const streamError = writable<string>('');

// API functions
export async function fetchStream(payload: ChatInputPayload) {
    isStreaming.set(true);
    streamError.set('');
    streamData.set('');

    try {
        await new Promise(resolve => setTimeout(resolve, 1000));
    
        const response = "This is a simulated AI response to: " + payload.chat_input_list[payload.chat_input_list.length - 1].message;
    
        for (let i = 0; i < response.length; i++) {
            streamData.update(current => current + response[i]);
            await new Promise(resolve => setTimeout(resolve, 20));
        }
    
        isStreaming.set(false);
        return { successful: true };
    } catch (error) {
        isStreaming.set(false);
        streamError.set('Error occurred during AI conversation');
        return { successful: false };
    }
} 