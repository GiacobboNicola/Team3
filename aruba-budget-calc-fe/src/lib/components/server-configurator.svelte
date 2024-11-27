<script lang="ts">
	import type { ServerOptions } from '../../types';
	import Button from './button.svelte';
	import { resourceCreation, resourceCreationActions } from '$lib/stores/resource-creation';
	import { onMount } from 'svelte';
	import { getPricingDetails } from '$lib/utils/calculation';
	import ConfigurationFooter from './configuration-footer.svelte';

	interface Props {
		onGoBack: () => void;
		onGoNext: () => void;
	}

	let { onGoBack, onGoNext }: Props = $props();

	const selections: ServerOptions = {
		osPlatform: ['Linux'],
		cpu: ['8', '12', '16', '32'],
		ram: ['16', '24', '32', '48', '64'],
		disk: ['40', '80', '120']
	};

	let selectedOptions: Record<keyof ServerOptions, string | null> = $state({
		osPlatform: $resourceCreation.serverConfig?.osPlatform || selections.osPlatform[0],
		cpu: $resourceCreation.serverConfig?.cpu || selections.cpu[0],
		ram: $resourceCreation.serverConfig?.ram || selections.ram[0],
		disk: $resourceCreation.serverConfig?.disk || selections.disk[2]
	});

	let price: number = $state(0);

	onMount(() => {
		price = getPricingDetails({
			reservationTerm: '1 Month',
			tierCategory: 'Partner',
			osPlatform: $resourceCreation.serverConfig?.osPlatform || selections.osPlatform[0],
			cpu: $resourceCreation.serverConfig?.cpu || selections.cpu[0],
			ram: $resourceCreation.serverConfig?.ram || selections.ram[0],
			disk: $resourceCreation.serverConfig?.disk || selections.disk[2]
		}).price;
	});

	function updateSelection(category: keyof ServerOptions, value: string | null) {
		// Ensure at least one option is selected for each category
		if (value === null) {
			selectedOptions[category] = selections[category][0]; // Set to the first option if deselected
		} else {
			selectedOptions[category] = value;
		}

		// Enforce combinations of CPU, RAM, and Disk
		if (category === 'cpu') {
			switch (value) {
				case '8':
					selectedOptions.ram =
						selectedOptions.ram === '16' || selectedOptions.ram === '32'
							? selectedOptions.ram
							: '16';
					selectedOptions.disk = '120';
					break;
				case '12':
					selectedOptions.ram = '24';
					selectedOptions.disk = '120';
					break;
				case '16':
					selectedOptions.ram =
						selectedOptions.ram === '32' || selectedOptions.ram === '64'
							? selectedOptions.ram
							: '32';
					selectedOptions.disk = '120';
					break;
				case '32':
					selectedOptions.ram = '64';
					selectedOptions.disk = '120';
					break;
			}
		}

		resourceCreationActions.setServerConfig(selectedOptions);

		price = getPricingDetails({
			reservationTerm: '1 Month',
			tierCategory: 'Partner',
			osPlatform: $resourceCreation.serverConfig?.osPlatform || selections.osPlatform[0],
			cpu: $resourceCreation.serverConfig?.cpu || selections.cpu[0],
			ram: $resourceCreation.serverConfig?.ram || selections.ram[0],
			disk: $resourceCreation.serverConfig?.disk || selections.disk[2]
		}).price;
	}

	function allOptionsSelected(): boolean {
		return Object.values(selectedOptions).every((option) => option !== null);
	}

	function isValidRamOption(cpu: string | null, ram: string): boolean {
		if (cpu === '8') {
			return ram === '16' || ram === '32';
		} else if (cpu === '12') {
			return ram === '24';
		} else if (cpu === '16') {
			return ram === '32' || ram === '64';
		} else if (cpu === '32') {
			return ram === '64';
		}
		return false;
	}
</script>

<div class="configuration">
	<h2 class="text-primary mb-8 text-center text-2xl font-bold">Configure Your Resource</h2>
	<div class="grid gap-4 md:grid-cols-4">
		{#each Object.entries(selections) as [category, options]}
			<div class="rounded-lg bg-white p-4 shadow-md">
				<h3 class="mb-4 text-center text-blue-600">
					{category === 'osPlatform' ? 'OS' : category.toUpperCase()}
				</h3>
				<div class="flex flex-col gap-2">
					{#each options as option}
						<button
							class="{selectedOptions[category as keyof typeof selectedOptions] === option
								? 'bg-primary text-white'
								: 'text-primary bg-white'} border-primary hover:bg-primary cursor-pointer rounded border p-2 transition-all duration-300 hover:text-white disabled:opacity-20"
							onclick={() => {
								if (selectedOptions[category as keyof typeof selectedOptions] === option) {
									return;
								}
								updateSelection(category as keyof ServerOptions, option);
							}}
							disabled={(category === 'ram' && !isValidRamOption(selectedOptions.cpu, option)) ||
								(category === 'disk' && option !== '120')}
						>
							{option}{(category as keyof ServerOptions) === 'disk' ||
							(category as keyof ServerOptions) === 'ram'
								? 'GB'
								: ''}
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
	<ConfigurationFooter {price} />
</div>
