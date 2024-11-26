<script lang="ts">
	let { children } = $props();
</script>

{@render children()}

<footer
	class="absolute bottom-0 flex w-full items-center justify-between border-t bg-white px-8 py-4 font-bold shadow-lg"
>
	<div class="flex gap-4">
		<div>
			Hourly Cost: <span class="text-primary">0.0 USD</span>
		</div>
		<div>
			Monthly Cost: <span class="text-primary">0.0 USD</span>
		</div>
	</div>

	<button
		class="cursor-pointer rounded-2xl border-none bg-input px-8 py-4 text-lg text-white transition-all duration-300 hover:bg-opacity-80"
	>
		Ordina ora
	</button>
</footer>
