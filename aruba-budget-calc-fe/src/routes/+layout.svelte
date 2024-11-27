<script lang="ts">
	import { goto } from '$app/navigation';
	import { projectName, userName } from '$lib/stores';
	import '../app.css';
	let { children } = $props();
</script>

<header class="fixed top-0 flex w-full items-center justify-between bg-white shadow-lg">
	<div class="flex items-center gap-4 px-8 py-2">
		<button onclick={() => goto('/calculation/cart')}>
			<img src="/aruba-logo-light.svg" alt="Aruba Logo" class="h-12" />
		</button>
		<h1 class="text-2xl font-bold text-gray-800">Budget Calculator</h1>
	</div>
	{#if $userName}
		<div class="flex items-center justify-center px-8 py-2 text-black">
			<div class="mr-4 flex flex-col items-end">
				<div class="font-bold uppercase text-primary">{$userName}</div>
				<div class="flex flex-col items-end">
					<!-- <img src="/images/partner.png" alt="user" width="24" height="24" /> -->
					<div class="ml-2 font-bold">Partner</div>
					{#if $projectName}
						<div>{$projectName}</div>
					{/if}
				</div>
			</div>
			<img src="/images/user.png" alt="user" width="60" height="60" />
		</div>
	{/if}
</header>

{@render children()}
