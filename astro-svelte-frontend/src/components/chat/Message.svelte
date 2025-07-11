<!-- src/components/chat/Message.svelte -->
<script lang="ts">
    import { User, Bot } from "@lucide/svelte/icons";
    import type { ChatMessage } from "$lib/types/chat";
    
    export let message: ChatMessage;
    export let isUser: boolean = message.role === 'user';
    
    function formatTime(date: Date): string {
        return date.toLocaleTimeString([], { 
            hour: '2-digit', 
            minute: '2-digit',
            hour12: true 
        });
    }
</script>

<div class="flex items-start gap-3 {isUser ? 'justify-end' : 'justify-start'}">
    <!-- Icon for assistant (left side) -->
    {#if !isUser}
        <div class="flex-shrink-0 w-8 h-8 bg-emerald-700 rounded-full flex items-center justify-center mt-1">
            <Bot class="w-4 h-4 text-emerald-50" />
        </div>
    {/if}

    <!-- Message bubble with timestamp -->
    <div class="flex flex-col {isUser ? 'items-end' : 'items-start'} max-w-[80%]">
        <div class="{isUser ? 'bg-emerald-900' : 'bg-emerald-800'} rounded-xl p-4">
            <p class="text-emerald-50 whitespace-pre-wrap">{message.message}</p>
        </div>
        <div class="text-xs text-emerald-400 mt-1 opacity-70 px-2">
            {formatTime(message.timestamp)}
        </div>
    </div>

    <!-- Icon for user (right side) -->
    {#if isUser}
        <div class="flex-shrink-0 w-8 h-8 bg-emerald-600 rounded-full flex items-center justify-center mt-1">
            <User class="w-4 h-4 text-emerald-50" />
        </div>
    {/if}
</div>