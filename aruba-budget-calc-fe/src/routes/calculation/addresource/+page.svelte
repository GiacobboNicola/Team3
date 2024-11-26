<script lang="ts">
	import QuantityReservationForm from '$lib/components/quantity-reservation-form.svelte';
	import ResourceTypeSelector from '$lib/components/resource-type-selector.svelte';
	import ServerConfigurator from '$lib/components/server-configurator.svelte';
	import { resourceCreation, resourceCreationActions } from '$lib/stores/resource-creation';
	import { ResourceName, StepName } from '../../../types';

	function goToNextStep(resource: ResourceName | undefined) {
		if ($resourceCreation.currentStep === StepName.INITIALGRID) {
			resourceCreationActions.setResource(resource!);
			if (resource === ResourceName.CONTAINER || resource === ResourceName.COMPUTING) {
				resourceCreationActions.setStep(StepName.CONFIGURESERVER);
			} else {
				resourceCreationActions.setStep(StepName.QUANTITY);
			}
		} else if ($resourceCreation.currentStep === StepName.CONFIGURESERVER) {
			resourceCreationActions.setStep(StepName.QUANTITY);
		}
	}

	const goToPreviousStep = () => {
		if ($resourceCreation.currentStep === StepName.QUANTITY) {
			if ($resourceCreation.selectedResource === ResourceName.CONTAINER || 
				$resourceCreation.selectedResource === ResourceName.COMPUTING) {
				resourceCreationActions.setStep(StepName.CONFIGURESERVER);
			} else {
				resourceCreationActions.setStep(StepName.INITIALGRID);
			}
		} else if ($resourceCreation.currentStep === StepName.CONFIGURESERVER) {
			resourceCreationActions.setStep(StepName.INITIALGRID);
		}
	};

	// Reset store when component is mounted
	$: {
		resourceCreationActions.reset();
	}
</script>

<main class="container mx-auto mt-16 max-w-7xl px-8 py-16">
	{#if $resourceCreation.currentStep === StepName.INITIALGRID}
		<ResourceTypeSelector 
			selectedResource={$resourceCreation.selectedResource} 
			onGoNext={goToNextStep} 
		/>
	{:else if $resourceCreation.currentStep === StepName.CONFIGURESERVER && 
			($resourceCreation.selectedResource === ResourceName.CONTAINER || 
			 $resourceCreation.selectedResource === ResourceName.COMPUTING)}
		<ServerConfigurator 
			onGoBack={goToPreviousStep} 
			onGoNext={() => goToNextStep($resourceCreation.selectedResource)} 
		/>
	{:else if $resourceCreation.currentStep === StepName.QUANTITY}
		<QuantityReservationForm 
			onGoBack={goToPreviousStep} 
			onGoNext={() => goToNextStep($resourceCreation.selectedResource)} 
		/>
	{/if}
</main>
