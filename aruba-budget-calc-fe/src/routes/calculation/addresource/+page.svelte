<script lang="ts">
	import QuantityReservationForm from '$lib/components/quantity-reservation-form.svelte';
	import ResourceTypeSelector from '$lib/components/resource-type-selector.svelte';
	import ServerConfigurator from '$lib/components/server-configurator.svelte';
	import { resourceCreation, resourceCreationActions } from '$lib/stores/resource-creation';
	import { ResourceName, StepName } from '../../../types';
	import { goto } from '$app/navigation';

	const selectedResource = $derived($resourceCreation.selectedResource);

	function goToNextStep() {
		if ($resourceCreation.currentStep === StepName.RESOURCETYPESELECTOR) {
			if (selectedResource) {
				if (
					selectedResource === ResourceName.CONTAINER ||
					selectedResource === ResourceName.COMPUTING
				) {
					resourceCreationActions.setStep(StepName.SERVERCONFIGURATOR);
				} else {
					resourceCreationActions.setStep(StepName.QUANTITYRESERVATIONFORM);
				}
			}
		} else if ($resourceCreation.currentStep === StepName.SERVERCONFIGURATOR) {
			resourceCreationActions.setStep(StepName.QUANTITYRESERVATIONFORM);
		} else if ($resourceCreation.currentStep === StepName.QUANTITYRESERVATIONFORM) {
			resourceCreationActions.reset(); // Reset for the next resource
			goto('/calculation/cart'); // Redirect to cart
		}
	}

	const goToPreviousStep = () => {
		if ($resourceCreation.currentStep === StepName.QUANTITYRESERVATIONFORM) {
			if (
				$resourceCreation.selectedResource === ResourceName.CONTAINER ||
				$resourceCreation.selectedResource === ResourceName.COMPUTING
			) {
				resourceCreationActions.setStep(StepName.SERVERCONFIGURATOR);
			} else {
				resourceCreationActions.setStep(StepName.RESOURCETYPESELECTOR);
			}
		} else if ($resourceCreation.currentStep === StepName.SERVERCONFIGURATOR) {
			resourceCreationActions.setStep(StepName.RESOURCETYPESELECTOR);
		}
	};
</script>

<main class="container mx-auto mt-16 max-w-7xl px-8 pt-16 pb-32">
	{#if $resourceCreation.currentStep === StepName.RESOURCETYPESELECTOR}
		<ResourceTypeSelector onGoNext={goToNextStep} />
	{:else if $resourceCreation.currentStep === StepName.SERVERCONFIGURATOR && ($resourceCreation.selectedResource === ResourceName.CONTAINER || $resourceCreation.selectedResource === ResourceName.COMPUTING)}
		<ServerConfigurator onGoBack={goToPreviousStep} onGoNext={goToNextStep} />
	{:else if $resourceCreation.currentStep === StepName.QUANTITYRESERVATIONFORM}
		<QuantityReservationForm onGoBack={goToPreviousStep} onGoNext={goToNextStep} />
	{/if}
</main>
