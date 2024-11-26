<script lang="ts">
	import QuantityReservationForm from '$lib/components/quantity-reservation-form.svelte';
	import ResourceTypeSelector from '$lib/components/resource-type-selector.svelte';
	import ServerConfigurator from '$lib/components/server-configurator.svelte';
	import { resourceCreation, resourceCreationActions } from '$lib/stores/resource-creation';
	import { ResourceName } from '../../../types';

	function goToNextStep(resource: ResourceName | undefined) {
		if ($resourceCreation.currentStep === 1) {
			resourceCreationActions.setResource(resource!);
			if (resource === ResourceName.CONTAINER || resource === ResourceName.COMPUTING) {
				resourceCreationActions.setStep(2);
			} else {
				resourceCreationActions.setStep(3);
			}
		} else if ($resourceCreation.currentStep === 2) {
			resourceCreationActions.setStep(3);
		}
	}

	const goToPreviousStep = () => {
		if ($resourceCreation.currentStep === 3) {
			if ($resourceCreation.selectedResource === ResourceName.CONTAINER || 
				$resourceCreation.selectedResource === ResourceName.COMPUTING) {
				resourceCreationActions.setStep(2);
			} else {
				resourceCreationActions.setStep(1);
			}
		} else if ($resourceCreation.currentStep === 2) {
			resourceCreationActions.setStep(1);
		}
	};

	// Reset store when component is mounted
	$: {
		resourceCreationActions.reset();
	}
</script>

<main class="container mx-auto mt-16 max-w-7xl px-8 py-16">
	{#if $resourceCreation.currentStep === 1}
		<ResourceTypeSelector 
			selectedResource={$resourceCreation.selectedResource} 
			onGoNext={goToNextStep} 
		/>
	{:else if $resourceCreation.currentStep === 2 && 
			($resourceCreation.selectedResource === ResourceName.CONTAINER || 
			 $resourceCreation.selectedResource === ResourceName.COMPUTING)}
		<ServerConfigurator 
			onGoBack={goToPreviousStep} 
			onGoNext={() => goToNextStep($resourceCreation.selectedResource)} 
		/>
	{:else if $resourceCreation.currentStep === 3}
		<QuantityReservationForm 
			onGoBack={goToPreviousStep} 
			onGoNext={() => goToNextStep($resourceCreation.selectedResource)} 
		/>
	{/if}
</main>
