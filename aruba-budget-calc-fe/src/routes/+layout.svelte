<script lang="ts">
	import { goto } from '$app/navigation';
	import '../app.css';
	let { children } = $props();
</script>

<header class="absolute top-0 w-full bg-white shadow-lg">
	<div class="mx-auto flex items-center gap-4 px-8 py-2">
		<button onclick={() => goto('/calculation/cart')}>
			<img src="/aruba-logo-light.svg" alt="Aruba Logo" class="h-12" />
		</button>
		<h1 class="text-2xl font-bold text-gray-800">Budget Calculator</h1>
	</div>
</header>

{@render children()}
