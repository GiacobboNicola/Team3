<script lang="ts">
	import { goto } from '$app/navigation';
	import '../app.css';
	let { children } = $props();
</script>

<header class="absolute top-0 w-full bg-white shadow-lg">
	<div class="mx-auto flex items-center gap-4 px-8 py-2">
		<button onclick={() => goto('/cart')}>
			<img src="/aruba-logo-light.svg" alt="Aruba Logo" class="h-12" />
		</button>
		<h1 class="text-2xl font-bold text-gray-800">Budget Calculator</h1>
	</div>
</header>

{@render children()}

<footer
	class="absolute bottom-0 flex w-full items-center justify-between border-t bg-white px-8 py-4 font-bold shadow-lg"
>
	<div class="flex gap-4">
		<div>
			Hourly Cost: <span class="text-primary">0.0 USD</span>
		</div>
		<div>
			Monthly Cost: <span class="text-primary">0.0 USD</span>
		</div>
	</div>

	<button
		class="cursor-pointer rounded-2xl border-none bg-input px-8 py-4 text-lg text-white transition-all duration-300 hover:bg-opacity-80"
	>
		Ordina ora
	</button>
</footer>
