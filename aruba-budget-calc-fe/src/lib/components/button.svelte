<script lang="ts">
	interface Props {
		label: string;
		disabled?: boolean;
		onClick: () => void;
		class?: string;
	}

	let { label, class: className, disabled, onClick }: Props = $props();
</script>

<button
	class="{className} cursor-pointer rounded border-none bg-input px-8 py-4 text-lg text-white transition-all duration-300 hover:bg-opacity-80 disabled:cursor-not-allowed disabled:bg-opacity-40"
	{disabled}
	onclick={onClick}
>
	{label}
</button>
