<script lang="ts">
	import Button from './button.svelte';
	import { goto } from '$app/navigation';
	import { projectName, setProjectName } from '$lib/stores';

	let name: string = $state($projectName || '');

	const onConfirm = () => {
		setProjectName(name);
	};
</script>

<h2 class="text-primary mb-8 text-center text-2xl font-bold">Insert the Project Name</h2>
<input
	type="string"
	bind:value={name}
	class="rounded-custom shadow-custom focus:border-primary focus:ring-primary mt-1 block w-full border border-gray-300 px-3 py-2 focus:outline-none"
/>

<div class="mt-4 flex justify-end">
	<Button onClick={onConfirm} label="Confirm" disabled={!name} />
</div>
