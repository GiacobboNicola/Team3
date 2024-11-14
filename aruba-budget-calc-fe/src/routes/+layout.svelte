<script lang="ts">
	import '../app.css';
	let { children } = $props();
</script>

<header class="absolute w-full bg-white shadow-lg">
	<div class="mx-auto flex items-center gap-4 px-8 py-2">
		<img src="/aruba-logo-light.svg" alt="Aruba Logo" class="h-12" />
		<h1 class="text-2xl font-bold text-gray-800">Budget Calculator</h1>
	</div>
</header>

{@render children()}
