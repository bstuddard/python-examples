<script>
    import Button from "$lib/components/ui/button/button.svelte";

	let count = 0;

	function increment() {
		count += 1;
	}
</script>

<div class="flex flex-col items-center justify-center min-h-screen font-sans gap-8">
	<h1 class="text-5xl text-gray-800 m-0">Hello World!</h1>
	<div class="text-center flex flex-col gap-4 items-center">
		<p class="text-2xl text-gray-600 m-0">Count: {count}</p>
		<Button onclick={increment}>
			Increment
        </Button>
	</div>
</div>