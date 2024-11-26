<script lang="ts">
	import Button from './button.svelte';
	import { resourceCreation, resourceCreationActions } from '$lib/stores/resource-creation';

	interface Props {
		onGoBack: () => void;
		onGoNext: () => void;
	}

	let { onGoBack, onGoNext }: Props = $props();

	const MINIMUM_QUANTITY = 50;
	let quantity: number = $state($resourceCreation.quantity || MINIMUM_QUANTITY);
	let selectedPeriod: string = $state($resourceCreation.period || '');

	$effect(() => {
		resourceCreationActions.setQuantity(quantity);
		resourceCreationActions.setPeriod(selectedPeriod);
	});

	const periods = [
		{ id: '1month', label: '1 Month' },
		{ id: '1year', label: '1 Year' },
		{ id: '3years', label: '3 Years' }
	];
</script>

<h2 class="mb-8 text-center text-2xl font-bold text-primary">Select The Quantity You Need</h2>
<input
	type="number"
	bind:value={quantity}
	min={MINIMUM_QUANTITY.toString()}
	max="9999"
	class="rounded-custom shadow-custom mt-1 block w-full border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none focus:ring-primary"
/>

<h2 class="mb-4 mt-8 text-center text-2xl font-bold text-primary">Reservation Period</h2>
<div class="grid grid-cols-1 gap-4 md:grid-cols-3">
	{#each periods as period}
		<button
			class="flex cursor-pointer flex-col items-center justify-center rounded-lg border-2 bg-white p-6 transition-all duration-300
            {selectedPeriod !== period.id ? 'hover:shadow-lg' : ''}
            {selectedPeriod === period.id
				? 'border-2 border-primary bg-primary shadow-xl'
				: 'border-gray-200'}"
			onclick={() => (selectedPeriod = selectedPeriod === period.id ? '' : period.id)}
		>
			<span class="text-lg font-semibold">{period.label}</span>
		</button>
	{/each}
</div>

<div class="mt-4 flex justify-between">
	<Button onClick={onGoBack} label="Back" />
	<Button onClick={onGoNext} label="Next" disabled={!selectedPeriod} />
</div>
