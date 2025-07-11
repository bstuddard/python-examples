<!-- src/components/chat/ChatHeader.svelte -->
<script lang="ts">
    export let title: string = 'Chat AI';
    export let onSettings: (() => void) | undefined = undefined;
</script>

<header class="sticky top-0 bg-emerald-950 w-full p-4 flex justify-between items-center border-b border-emerald-900">
    <h1 class="text-lg font-bold text-emerald-50">{title}</h1>
    <nav>
        <button 
            onclick={() => onSettings?.()}
            class="text-emerald-50 cursor-pointer sm:hover:text-emerald-300 sm:transition"
        >
            Settings
        </button>
    </nav>
</header> 