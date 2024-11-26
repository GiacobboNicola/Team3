<script>
	import { goto } from '$app/navigation';
	import Button from '$lib/components/button.svelte';
	import { selectedResources } from '$lib/stores';

	const userResources = $selectedResources;
</script>

<main class="container mx-auto mt-16 max-w-7xl px-8 py-16">
	{#if !userResources.length}
		<h2 class="mb-8 text-center text-2xl font-bold text-primary">
			Start to add resources to your Aruba Cloud!
		</h2>
	{:else}
		{#each $selectedResources as res}
			<div class="uppecase mb-2 rounded border p-4 font-bold">{res.name}</div>
		{/each}
	{/if}
	<div class="flex justify-center">
		<Button label="Add new resource" onClick={() => goto('/calculation/addresource')} />
	</div>
</main>
