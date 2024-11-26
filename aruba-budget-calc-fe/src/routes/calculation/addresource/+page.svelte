<script lang="ts">
	import QuantityReservationForm from '$lib/components/quantity-reservation-form.svelte';
	import ResourceTypeSelector from '$lib/components/resource-type-selector.svelte';
	import ServerConfigurator from '$lib/components/server-configurator.svelte';
	import ProjectNameForm from '$lib/components/project-name-form.svelte';
	import { resourceCreation, resourceCreationActions } from '$lib/stores/resource-creation';
	import { ResourceName, StepName } from '../../../types';

	function goToNextStep(resource: ResourceName | undefined) {
		if ($resourceCreation.currentStep === StepName.PROJECTNAMEFORM) {
			resourceCreationActions.setStep(StepName.RESOURCETYPESELECTOR);
		} else if ($resourceCreation.currentStep === StepName.RESOURCETYPESELECTOR) {
			resourceCreationActions.setResource(resource!);
			if (resource === ResourceName.CONTAINER || resource === ResourceName.COMPUTING) {
				resourceCreationActions.setStep(StepName.SERVERCONFIGURATOR);
			} else {
				resourceCreationActions.setStep(StepName.QUANTITYRESERVATIONFORM);
			}
		} else if ($resourceCreation.currentStep === StepName.SERVERCONFIGURATOR) {
			resourceCreationActions.setStep(StepName.QUANTITYRESERVATIONFORM);
		}
	}

	const goToPreviousStep = () => {
		if ($resourceCreation.currentStep === StepName.RESOURCETYPESELECTOR) {
			resourceCreationActions.setStep(StepName.PROJECTNAMEFORM);
		} else if ($resourceCreation.currentStep === StepName.QUANTITYRESERVATIONFORM) {
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

	// Reset store when component is mounted
	$: {
		resourceCreationActions.reset();
	}
</script>

<main class="container mx-auto mt-16 max-w-7xl px-8 py-16">
	{#if $resourceCreation.currentStep === StepName.PROJECTNAMEFORM}
		<ProjectNameForm
			selectedResource={$resourceCreation.selectedResource}
			onGoNext={goToNextStep}
		/>
	{:else if $resourceCreation.currentStep === StepName.RESOURCETYPESELECTOR}
		<ResourceTypeSelector
			selectedResource={$resourceCreation.selectedResource}
			onGoBack={goToPreviousStep}
			onGoNext={goToNextStep}
		/>
	{:else if $resourceCreation.currentStep === StepName.SERVERCONFIGURATOR && ($resourceCreation.selectedResource === ResourceName.CONTAINER || $resourceCreation.selectedResource === ResourceName.COMPUTING)}
		<ServerConfigurator
			onGoBack={goToPreviousStep}
			onGoNext={() => goToNextStep($resourceCreation.selectedResource)}
		/>
	{:else if $resourceCreation.currentStep === StepName.QUANTITYRESERVATIONFORM}
		<QuantityReservationForm
			onGoBack={goToPreviousStep}
			onGoNext={() => goToNextStep($resourceCreation.selectedResource)}
		/>
	{/if}
</main>
