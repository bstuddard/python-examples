<template>
    <div class="min-h-screen flex flex-col max-w-3xl min-w-screen sm:min-w-[600px]">

        <!-- Chat Messages Container -->
        <div class="flex-1 overflow-y-auto px-4 py-4 space-y-4" id="chatContainer">

            <!-- Displaying messages -->
            <div v-if="messages.length" class="space-y-4">
                <div v-for="(message, index) in messages" :key="index" :class="{
                    'bg-emerald-900 p-4 rounded-xl ml-1/2': message.role === 'user',
                    'p-4 rounded-xl': message.role !== 'user'
                }">
                    <p class="text-emerald-50 whitespace-pre-wrap">{{ message.message }}</p>
                </div>
                <div v-if="isStreaming" class="p-2 rounded-xl">
                    <p class="text-emerald-50 whitespace-pre-wrap">{{ streamData }}</p>
                </div>
            </div>
            <div v-else>
                <!-- Watermark (only if messages empty) -->
                <div class="absolute inset-0 flex items-center justify-center pointer-events-none">
                    <p class="text-6xl text-emerald-100 opacity-10 font-bold select-none">
                        Chat AI
                    </p>
                </div>
            </div>

            <!--Display errors, if any-->
            <div v-if="streamError" class="p-4 rounded-xl bg-red-300 text-red-900">
                <p class="font-semibold italic">Error occurred during AI conversation</p>
                <p>{{ streamError }}</p>
            </div>

        </div>

        <!-- Input Box -->
        <div class="px-6 pb-6 sticky bottom-0 bg-emerald-950">
            <div class="flex items-center gap-2 bg-emerald-900 rounded-2xl shadow-xl p-2 focus-within:ring-2 focus-within:ring-emerald-300">
                <textarea
                    v-model="userInput"
                    type="text"
                    placeholder="Ask a question" 
                    class="flex-1 px-2 pt-1 pb-4 rounded-2xl resize-none focus:outline-none text-emerald-50"
                    @keydown.enter="handleSendMessage"
                    :disabled="isStreaming"
                ></textarea>
                <button 
                    @click="handleSendMessage"
                    class="button bg-emerald-50 text-emerald-950 font-semibold mx-2 py-2 px-4 shadow-md rounded-md cursor-pointer sm:hover:bg-emerald-200 sm:transition"
                    :disabled="isStreaming"
                >
                    Send
                </button>
            </div>
            <div class="flex items-center justify-center p-1">
                <p class="text-sm text-emerald-100 font-light">Mistakes can be made, check important info.</p>
            </div>
        </div>

    </div>
</template>

<script setup lang="ts">
// Library
import { ref } from 'vue';

// Types
import type { Ref } from 'vue';
import type { StreamingParsedResponse } from '@/composables/useStreamingAPI';
import type { ChatMessage, ChatInputPayload } from '@/types/chatTypes';

// Local file
import useStreamingAPI from '@/composables/useStreamingAPI';

const { fetchStream, streamData, isStreaming, streamError } = useStreamingAPI();
const userInput: Ref<string> = ref('');
const messages: Ref<ChatMessage[]> = ref([]);

async function handleSendMessage() {
    if (userInput.value.trim()) {

        // Add to combined queue
        messages.value.push({role: "user", message: userInput.value});

        // Get AI Response
        const chatInputPayload: ChatInputPayload = { chat_input_list: messages.value};
        const response: StreamingParsedResponse = await fetchStream(chatInputPayload);

        // Append AI response once the stream is finished
        if (response.successful) {
            messages.value.push({role: 'assistant', message: streamData.value});
        } else {
            // TODO: Add error handling
        }
    
        // Reset user field
        userInput.value = '';
    }
}

</script>