<script lang="ts">
	import Button from './button.svelte';
	import { resourceCreation, resourceCreationActions } from '$lib/stores/resource-creation';
	import { goto } from '$app/navigation';

	interface Props {
		onGoNext: () => void;
	}

	let { onGoNext }: Props = $props();

	let name: string = $state($resourceCreation.projectName || '');

	$effect(() => {
		resourceCreationActions.setProjectName(name);
	});
</script>

<h2 class="text-primary mb-8 text-center text-2xl font-bold">Insert the Project Name</h2>
<input
	type="string"
	bind:value={name}
	class="rounded-custom shadow-custom focus:border-primary focus:ring-primary mt-1 block w-full border border-gray-300 px-3 py-2 focus:outline-none"
/>

<div class="mt-4 flex justify-between">
	<Button onClick={() => goto('/calculation/cart')} label="Cancel" />
	<Button onClick={onGoNext} label="Next" disabled={!name} />
</div>
