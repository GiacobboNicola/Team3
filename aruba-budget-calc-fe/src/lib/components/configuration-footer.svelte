<script lang="ts">
	import { cart } from '$lib/stores/cart';

	interface Props {
		price: number; // Receive pricing details as a prop
	}

	let { price }: Props = $props();

	const resourceMontlyCost = $derived(price * 24 * 30);

	const totalHourlyCost = $derived($cart.reduce((sum, item) => sum + item.price, 0));

	const totalMonthlyCost = $derived(totalHourlyCost * 24 * 30 + resourceMontlyCost); // Assuming 24 hours in a day for 30 days
</script>

<div
	class="fixed bottom-0 left-0 flex w-full items-center border-t bg-white px-8 py-4 font-bold shadow-lg"
>
	<div class="mr-8">
		<div>
			Resource Hourly Cost: <span class="text-primary font-bold">{price.toFixed(2)}€</span>
		</div>
		<div>
			Resource Monthly Cost: <span class="text-primary font-bold"
				>{resourceMontlyCost.toFixed(2)}€</span
			>
		</div>
	</div>
	<div class="border-l border-gray-500 pl-8">
		<div>
			Total Hourly Cost: <span class="text-primary font-bold"
				>{(totalHourlyCost + price).toFixed(2)} €</span
			>
		</div>
		<div>
			Total Monthly Cost: <span class="text-primary font-bold">{totalMonthlyCost.toFixed(2)} €</span
			>
		</div>
	</div>
</div>
