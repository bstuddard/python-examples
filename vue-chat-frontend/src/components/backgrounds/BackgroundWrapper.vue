<template>
    <div class="w-screen h-screen relative select-none max-h-screen overflow-y-auto overflow-x-hidden bg-emerald-950 text-white">
        
        <!-- Header -->
        <header class="sticky top-0 bg-emerald-950 w-full p-4 flex justify-between items-center">
            <h1 class="text-lg font-bold text-emerald-50">Chat AI</h1>
            <nav>
                <button class="text-emerald-50 cursor-pointer sm:hover:text-emerald-300 sm:transition">Settings</button>
            </nav>
        </header>

        <!--Content-->
        <div class="flex flex-col items-center justify-center" id="contentWrapper">
                <slot></slot>
        </div>
    </div>
</template>