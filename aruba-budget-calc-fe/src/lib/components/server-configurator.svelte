<script lang="ts">
	import type { Selections } from '../../types';
	import Button from './button.svelte';

	interface Props {
		onGoBack: () => void;
	}

	let { onGoBack }: Props = $props();

	const selections: Selections = {
		os: ['Windows', 'Linux'],
		cpu: ['2', '4', '8', '16'],
		ram: ['8', '16', '32'],
		disk: ['100GB', '240GB', '500GB'],
		reservation: ['10', '50', '100']
	};

	let selectedOptions: Record<keyof Selections, string | null> = $state({
		os: null,
		cpu: null,
		ram: null,
		disk: null,
		reservation: null
	});

	function updateSelection(category: keyof Selections, value: string | null) {
		selectedOptions[category] = value;
	}
</script>

<div class="configuration">
	<h2 class="mb-8 text-center text-2xl font-bold text-primary">Configure Your Resource</h2>
	<div class="grid gap-4 md:grid-cols-5">
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
									updateSelection(category as keyof Selections, null);
									return;
								}
								updateSelection(category as keyof Selections, option);
							}}
						>
							{option}
						</button>
					{/each}
				</div>
			</div>
		{/each}
	</div>
	<Button onClick={onGoBack} label="Back" class="mt-4" />
</div>
