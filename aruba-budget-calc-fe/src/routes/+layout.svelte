<script lang="ts">
	import { goto } from '$app/navigation';
	import { projectName, userName } from '$lib/stores';
	import '../app.css';
	let { children } = $props();
</script>

<header class="fixed top-0 flex w-full items-center justify-between bg-white shadow-lg">
	<div class="flex items-center gap-4 px-8 py-2">
		<button onclick={() => goto('/calculation/cart')}>
			<img src="/abc-logo.png" alt="Aruba Logo" class="h-12" />
		</button>
		<h1 class="text-2xl font-bold text-gray-800">Aruba Budget Calculator</h1>
	</div>
	{#if $userName}
		<div class="flex items-center justify-center px-8 py-2 text-black">
			<div class="mr-4 flex flex-col items-end">
				<div class="text-primary font-bold uppercase">
					{$userName}
					{#if $projectName}<span> / {$projectName}</span>{/if}
				</div>
				<div class="flex flex-col items-end">
					<div class="ml-2 font-bold">Partner</div>
				</div>
			</div>
			<img src="/images/user.png" alt="user" width="48" height="48" />
		</div>
	{/if}
</header>

{@render children()}
