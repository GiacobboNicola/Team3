<script lang="ts">
	import Button from '$lib/components/button.svelte';
	import { cart } from '$lib/stores/cart';
	import { derived } from 'svelte/store';

	let { children } = $props();

	// Calculate total hourly and monthly costs
	const totalHourlyCost = derived(cart, ($cart) => {
		return $cart.reduce((sum, item) => sum + item.price, 0);
	});

	const totalMonthlyCost = derived(totalHourlyCost, ($totalHourlyCost) => {
		return $totalHourlyCost * 24 * 30; // Assuming 24 hours in a day for 30 days
	});
</script>

{@render children()}

<footer
	class="fixed bottom-0 flex w-full items-center justify-between border-t bg-white px-8 py-4 font-bold shadow-lg"
>
	<div class="">
		<div>
			Hourly Cost: <span class="text-primary {$totalHourlyCost > 0 && 'text-black line-through'}"
				>{$totalHourlyCost.toFixed(2)} USD</span
			>
			{#if $totalHourlyCost > 0}<span class="text-primary ml-1"
					>{($totalHourlyCost - (15 / 100) * $totalHourlyCost).toFixed(2)} €</span
				>{/if}
		</div>
		<div>
			Monthly Cost: <span class="text-primary {$totalMonthlyCost > 0 && 'text-black line-through'}"
				>{$totalMonthlyCost.toFixed(2)} USD</span
			>{#if $totalMonthlyCost > 0}<span class="text-primary ml-1"
					>{($totalMonthlyCost - (15 / 100) * $totalMonthlyCost).toFixed(2)} €</span
				>{/if}
		</div>
	</div>

	{#if $totalHourlyCost > 0}
		<p class="text-red-600">As a Partner you enjoy a 15% discount!</p>
	{/if}
	<Button onClick={() => null} disabled={!$cart.length} label="Ordina ora" class="rounded-xl" />
</footer>
