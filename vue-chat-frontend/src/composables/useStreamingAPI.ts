// Library
import { ref } from 'vue';

// Types
import type { Ref } from 'vue';
import type { ChatInputPayload } from '@/types/chatTypes';

// Local Files
import { devlog } from '@/devlogger/devlogger';



// Base URL setup based on env
const baseURLChoice: string = process.env.NODE_ENV !== 'production' ? 'http://localhost:8000/stream/' : 'http://localhost:8000/stream/';

// Parsed response interface (slightly adjusted for streaming)
interface StreamingParsedResponse {
    successful: boolean;
    status?: number;
    data: string;
    error?: string;
}

export type { StreamingParsedResponse };
export default function useStreamingAxios() {
    const streamData: Ref<string> = ref(''); // Accumulated streamed response
    const isStreaming: Ref<boolean> = ref(false); // Streaming state
    const streamError: Ref<string> = ref(''); // Error message

    /**
     * Fetch a streaming response from the API
     * @param chatInputPayload List of ChatMessage objects
     */
    async function fetchStream(chatInputPayload: ChatInputPayload): Promise<StreamingParsedResponse> {
        try {
            // Reset state
            streamData.value = '';
            streamError.value = '';
            isStreaming.value = true;

            // Build URL
            const url: string = baseURLChoice;

            // Make call and start response
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Accept': 'text/event-stream',
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(chatInputPayload)
            });
            if (!response.ok) {
                throw new Error(`HTTP error ${response.status}: ${response.statusText}`);
            }
            if (!response.body) {
                throw new Error('No response body available for streaming');
            }

            // Chunk reading
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            while (true) {
                const { done, value } = await reader.read();
                if (done) break;
                const chunk = decoder.decode(value, { stream: true });
                streamData.value += chunk; // Append chunk reactively
                devlog(`Received chunk: ${chunk}`);
            }
            isStreaming.value = false;

            return { successful: true, data: streamData.value };

        } catch (error: unknown) {
            let errorMessage = "An unknown error has occured."

            if (error instanceof Error) {
                errorMessage = error.message;
            }

            streamError.value = errorMessage;
            isStreaming.value = false;

            return { successful: false, data: '', error: errorMessage };
        }
    }
    
    return {
        fetchStream,
        streamData,
        isStreaming,
        streamError
    }

}