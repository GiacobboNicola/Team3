<script lang="ts">
	import { goto } from '$app/navigation';
	import Button from '$lib/components/button.svelte';
	import CartFooter from '$lib/components/cart-footer.svelte';
	import ProjectNameForm from '$lib/components/project-name-form.svelte';
	import { projectName } from '$lib/stores';
	import { cart, cartActions } from '$lib/stores/cart';
	import { resourceCreationActions } from '$lib/stores/resource-creation';
	import { ResourceName } from '../../../types';
	import type { ServerOptions } from '../../../types';

	const pjName: string = $derived($projectName);

	function getResourceContent(resourceType: ResourceName): { name: string; image: string } {
		switch (resourceType) {
			case ResourceName.CONTAINER:
				return { name: 'Aruba Managed Kubernetes', image: '/images/kube.svg' };
			case ResourceName.DISK:
				return { name: 'Block Storage', image: '/images/storage.svg' };
			case ResourceName.COMPUTING:
				return { name: 'Cloud Server', image: '/images/cloud.svg' };
			case ResourceName.NETWORKING:
				return { name: 'Networking', image: '/images/network.svg' };
		}
	}

	function handleModify(itemId: string) {
		const item = $cart.find((i) => i.id === itemId);
		if (item) {
			resourceCreationActions.setResource(item.resourceType);
			if (item.serverConfig) {
				resourceCreationActions.setServerConfig(item.serverConfig);
			}
			resourceCreationActions.setQuantity(item.quantity);
			resourceCreationActions.setPeriod(item.period);
			cartActions.removeItem(itemId);
			goto('/calculation/addresource');
		}
	}
</script>

<main class="container mx-auto my-20 max-w-7xl px-8 py-16">
	{#if !pjName}
		<ProjectNameForm />
	{:else}
		{#if $cart.length === 0}
			<h2 class="text-primary mb-8 text-center text-2xl font-bold">
				Start to add resources to {pjName} Project!
			</h2>
		{:else}
			<h2 class="text-primary mb-8 text-center text-2xl font-bold">Your Selected Resources</h2>
			<div class="space-y-4">
				{#each $cart as item}
					<div class="rounded-lg border border-gray-200 bg-white p-6 shadow-md">
						<div>
							<div class="flex items-center justify-between">
								<div class="flex items-center">
									<img
										width={50}
										height={50}
										src={getResourceContent(item.resourceType).image}
										alt="resource type"
									/>

									<h3 class="text-primary ml-2 text-xl font-semibold">
										{getResourceContent(item.resourceType).name}
									</h3>
								</div>

								<div class="space-x-2">
									<button
										class="rounded-md bg-blue-100 px-3 py-1 text-blue-600 hover:bg-blue-200"
										onclick={() => handleModify(item.id)}
									>
										Modify
									</button>
									<button
										class="rounded-md bg-red-100 px-3 py-1 text-red-600 hover:bg-red-200"
										onclick={() => cartActions.removeItem(item.id)}
									>
										Delete
									</button>
								</div>
							</div>

							<div class="mt-4 grid grid-cols-2 gap-4 text-gray-600 md:grid-cols-4">
								{#if item.serverConfig && (item.resourceType === ResourceName.CONTAINER || item.resourceType === ResourceName.COMPUTING)}
									{#each Object.entries(item.serverConfig) as [key, value]}
										<div>
											<span class="font-medium uppercase">{key === 'osPlatform' ? 'OS' : key}:</span
											>
											{value}{(key as keyof ServerOptions) === 'disk' ||
											(key as keyof ServerOptions) === 'ram'
												? 'GB'
												: ''}
										</div>
									{/each}
								{/if}
								<div>
									<span class="font-medium">Quantity:</span>
									{item.quantity}
								</div>
								<div>
									<span class="font-medium">Period:</span>
									{item.period}
								</div>
							</div>
						</div>
					</div>
				{/each}
			</div>
		{/if}

		<div class="mt-8 flex justify-center">
			<Button label="Add new resource" onClick={() => goto('/calculation/addresource')} />
		</div>
	{/if}
</main>
{#if pjName}
	<CartFooter />
{/if}
