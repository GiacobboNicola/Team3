<script lang="ts">
	import type { ServerOptions } from '../../types';
	import Button from './button.svelte';
	import { resourceCreation, resourceCreationActions } from '$lib/stores/resource-creation';

	interface Props {
		onGoBack: () => void;
		onGoNext: () => void;
	}

	let { onGoBack, onGoNext }: Props = $props();

	const selections: ServerOptions = {
		os: ['Windows', 'Linux'],
		cpu: ['2', '4', '8', '16'],
		ram: ['8', '16', '32'],
		disk: ['100GB', '240GB', '500GB']
	};

	let selectedOptions: Record<keyof ServerOptions, string | null> = $state(
		$resourceCreation.serverConfig || {
			os: null,
			cpu: null,
			ram: null,
			disk: null
		}
	);

	function updateSelection(category: keyof ServerOptions, value: string | null) {
		selectedOptions[category] = value;
		resourceCreationActions.setServerConfig(selectedOptions);
	}

	function allOptionsSelected(): boolean {
		return Object.values(selectedOptions).every((option) => option !== null);
	}
</script>

<div class="configuration">
	<h2 class="mb-8 text-center text-2xl font-bold text-primary">Configure Your Resource</h2>
	<div class="grid gap-4 md:grid-cols-4">
		{#each Object.entries(selections) as [category, options]}
			<div class="rounded-lg bg-white p-4 shadow-md">
				<h3 class="mb-4 text-center text-blue-600">{category.toUpperCase()}</h3>
				<div class="flex flex-col gap-2">
					{#each options as option}
						<button
							class="{selectedOptions[category as keyof typeof selectedOptions] === option
								? 'bg-primary text-white'
								: 'bg-white text-primary'} cursor-pointer rounded border border-primary p-2 transition-all duration-300 hover:bg-primary hover:text-white"
							onclick={() => {
								if (selectedOptions[category as keyof typeof selectedOptions] === option) {
									updateSelection(category as keyof ServerOptions, null);
									return;
								}
								updateSelection(category as keyof ServerOptions, option);
							}}
						>
							{option}
						</button>
					{/each}
				</div>
			</div>
		{/each}
	</div>
	<div class="mt-4 flex justify-between">
		<Button onClick={onGoBack} label="Back" />
		<Button onClick={onGoNext} label="Next" disabled={!allOptionsSelected()} />
	</div>
</div>
