<!-- src/components/chat/TypingIndicator.svelte -->
<script lang="ts">
    import { Bot } from "@lucide/svelte/icons";

    export let streamData: string = '';
</script>

<div class="flex items-start gap-3 justify-start">
    <div class="flex-shrink-0 w-8 h-8 bg-emerald-700 rounded-full flex items-center justify-center mt-1">
        <Bot class="w-4 h-4 text-emerald-50" />
    </div>
    <div class="flex flex-col items-start max-w-[80%]">
        {#if streamData}
            <!-- Streaming message content -->
            <div class="bg-emerald-800 rounded-xl p-4">
                <p class="text-emerald-50 whitespace-pre-wrap">{streamData}<span class="animate-pulse">|</span></p>
            </div>
        {:else}
            <!-- Typing dots -->
            <div class="bg-emerald-800 rounded-xl p-4 flex items-center gap-2">
                <div class="flex gap-1 items-center">
                    <div class="w-2 h-2 bg-emerald-400 rounded-full animate-bounce"></div>
                    <div class="w-2 h-2 bg-emerald-400 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
                    <div class="w-2 h-2 bg-emerald-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                </div>
                <span class="text-sm text-emerald-400 ml-2">AI is thinking...</span>
            </div>
        {/if}
    </div>
</div> 