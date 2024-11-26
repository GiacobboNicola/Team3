<script lang="ts">
	import Button from '$lib/components/button.svelte';
	import { cart } from '$lib/stores/cart';

	let { children } = $props();
</script>

{@render children()}

<footer
	class="fixed bottom-0 flex w-full items-center justify-between border-t bg-white px-8 py-4 font-bold shadow-lg"
>
	<div class="flex gap-4">
		<div>
			Hourly Cost: <span class="text-primary">0.0 USD</span>
		</div>
		<div>
			Monthly Cost: <span class="text-primary">0.0 USD</span>
		</div>
	</div>

	<Button onClick={() => null} disabled={!$cart.length} label="Ordina ora" class="rounded-xl" />
</footer>
