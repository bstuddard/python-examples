<script lang="ts">
    import ChatHeader from './chat/ChatHeader.svelte';
    import Message from './chat/Message.svelte';
    import TypingIndicator from './chat/TypingIndicator.svelte';
    import MessageInput from './chat/MessageInput.svelte';
    import { Badge } from "$lib/components/ui/badge/index.js";
    import { messages, isStreaming, streamData, streamError, fetchStream } from '$lib/stores/chatStore';

    let userInput = '';

    async function handleSendMessage(messageText: string) {
        // Add user message
        messages.update(msgs => [...msgs, {
            role: "user",
            message: messageText,
            timestamp: new Date()
        }]);

        // Get AI response
        const response = await fetchStream({ chat_input_list: $messages });
        
        if (response.successful) {
            messages.update(msgs => [...msgs, {
                role: 'assistant',
                message: $streamData,
                timestamp: new Date()
            }]);
            streamData.set('');
        }
    }

    function handleSettings() {
        console.log('Settings clicked');
    }
</script>

<div class="w-screen h-screen relative select-none max-h-screen overflow-y-auto overflow-x-hidden bg-emerald-950 text-white">
    
    <ChatHeader onSettings={handleSettings} />

    <div class="flex flex-col items-center justify-center" id="contentWrapper">
        <div class="min-h-[calc(100vh-80px)] flex flex-col max-w-3xl w-full sm:min-w-[600px]">
            
            <!-- Messages Container -->
            <div class="flex-1 overflow-y-auto px-4 py-2" id="chatContainer">
                {#if $messages.length}
                    <div class="space-y-3">
                        {#each $messages as message, index (index)}
                            <Message {message} />
                        {/each}
                        
                        {#if $isStreaming}
                            <TypingIndicator streamData={$streamData} />
                        {/if}
                    </div>
                {:else}
                    <div class="flex items-center justify-center h-full">
                        <p class="text-6xl text-emerald-100 opacity-10 font-bold select-none">Chat AI</p>
                    </div>
                {/if}

                {#if $streamError}
                    <div class="mt-4">
                        <Badge variant="destructive" class="p-4 w-full">
                            <div>
                                <p class="font-semibold italic">Error occurred during AI conversation</p>
                                <p>{$streamError}</p>
                            </div>
                        </Badge>
                    </div>
                {/if}
            </div>

            <MessageInput 
                bind:userInput 
                isStreaming={$isStreaming} 
                onSend={handleSendMessage} 
            />
            
        </div>
    </div>
</div>