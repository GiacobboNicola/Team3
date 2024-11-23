<script lang="ts">
	import Button from './button.svelte';
	import { addResource } from '$lib/stores';
	import { ResourceName } from '../../types';

	interface Props {
		onGoNext: () => void;
	}

	let { onGoNext }: Props = $props();

	type ResourceButton = {
		id: ResourceName;
		name: string;
		description: string;
		image: string;
	};

	let resources: ResourceButton[] = [
		{
			id: ResourceName.CONTAINER,
			name: 'Aruba Managed Kubernetes',
			description:
				"Effortlessly create and manage Kubernetes clusters with Aruba's developer-friendly platform. With an intuitive control panel, you can deploy containerized applications quickly and at scale, while ensuring robust security every step of the way.",
			image: '/images/kube.svg'
		},
		{
			id: ResourceName.DISK,
			name: 'Block Storage',
			description:
				'Efficiently store and manage data with our highly scalable Block Storage system. Designed for speed, secure access, and fast recovery, it ensures your data is always protected and available when you need it.',
			image: '/images/storage.svg'
		},
		{
			id: ResourceName.COMPUTING,
			name: 'Cloud Server',
			description:
				'Tailor your Cloud Server to your needs with flexible hourly, monthly, or yearly plans. Connect seamlessly with other Cloud Servers using Virtual Switches, and enjoy the reliability of redundant hardware. Customize components to fit your workload, and choose from multiple Hypervisor technologies to optimize your performance.',
			image: '/images/cloud.svg'
		},
		{
			id: ResourceName.NETWORKING,
			name: 'Networking',
			description:
				'Manage your cloud infrastructure with flexible networking options. Purchase dynamic IP addresses and assign them across multiple resources to ensure secure, seamless connectivity. Create isolated Virtual Private Cloud (VPC) networks to organize your cloud resources, and use custom subnets and security groups to control traffic flow and enhance network security.',
			image: '/images/network.svg'
		}
	];

	let selectedResource: string | undefined = $state();

	function selectResource(resource: ResourceButton) {
		selectedResource = selectedResource === resource.name ? undefined : resource.name;
		addResource({
			id: '123',
			name: resource.id
		});
	}
</script>

<div class="text-center">
	<h2 class="mb-8 text-center text-2xl font-bold text-primary">Select Your Resource</h2>
	<div class="grid grid-cols-1 gap-4 md:grid-cols-2">
		{#each resources as resource}
			<button
				class="flex cursor-pointer flex-col items-center justify-center rounded-lg border border-2 bg-white p-6 transition-all duration-300
             {selectedResource !== resource.name ? 'hover:shadow-lg' : ''}
             {selectedResource === resource.name
					? 'border-2 border-primary bg-primary text-white shadow-xl'
					: 'border-gray-200'}"
				onclick={() => selectResource(resource)}
			>
				<img
					src={resource.image}
					alt="resource"
					style:height="85px"
					style:width="85px"
					class="mb-4"
				/>
				<h2 class="mb-2 text-lg font-semibold text-primary">{resource.name}</h2>
				<p class="text-gray-700">{resource.description}</p>
			</button>
		{/each}
	</div>
	<div class="mt-4 flex justify-end">
		<Button onClick={onGoNext} label="Next" disabled={!selectedResource} />
	</div>
</div>
