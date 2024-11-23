<script lang="ts">
	import ResourceTypeSelector from '$lib/components/resource-type-selector.svelte';
	import ServerConfigurator from '$lib/components/server-configurator.svelte';
	import type { PricingOption } from '../../types';

	const pricingOptions: PricingOption[] = [
		{ name: 'Standard', discount: 0, minUnits: 0 },
		{ name: 'Base', discount: 5, minUnits: 10 },
		{ name: 'Partner', discount: 10, minUnits: 50 },
		{ name: 'Premium', discount: 15, minUnits: 100 }
	];

	let currentStep = $state(1);

	function goToNextStep() {
		currentStep = currentStep + 1;
	}
	const goToPreviousStep = () => {
		currentStep = currentStep - 1;
	};
</script>

<main class="container mx-auto mt-16 max-w-7xl px-8 py-16">
	{#if currentStep === 1}
		<ResourceTypeSelector onGoNext={goToNextStep} />
	{:else}
		<ServerConfigurator onGoBack={goToPreviousStep} />
	{/if}
</main>
