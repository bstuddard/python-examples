<!-- src/components/chat/MessageInput.svelte -->
<script lang="ts">
    import Button from "$lib/components/ui/button/button.svelte";

    export let userInput: string = '';
    export let isStreaming: boolean = false;
    export let onSend: ((message: string) => void) | undefined = undefined;

    function handleKeydown(event: KeyboardEvent) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            handleSend();
        }
    }

    function handleSend() {
        if (userInput.trim() && onSend) {
            onSend(userInput);
            userInput = '';
        }
    }
</script>

<div class="px-6 pb-6 sticky bottom-0 bg-emerald-950">
    <div class="flex items-end gap-2 bg-emerald-900 rounded-2xl shadow-xl p-2 focus-within:ring-2 focus-within:ring-emerald-300">
        <textarea
            bind:value={userInput}
            placeholder="Ask a question" 
            class="flex-1 px-3 py-2 bg-transparent rounded-xl resize-none focus:outline-none text-emerald-50 placeholder:text-emerald-300 min-h-[44px] max-h-32"
            onkeydown={handleKeydown}
            disabled={isStreaming}
        ></textarea>
        <Button 
            onclick={handleSend}
            disabled={isStreaming}
            class="bg-emerald-50 text-emerald-950 hover:bg-emerald-200 shrink-0"
        >
            {isStreaming ? 'Sending...' : 'Send'}
        </Button>
    </div>
    <div class="flex items-center justify-center p-1">
        <p class="text-sm text-emerald-100 font-light">Mistakes can be made, check important info.</p>
    </div>
</div>
