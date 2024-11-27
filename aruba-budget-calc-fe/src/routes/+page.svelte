<script>
	import { goto } from '$app/navigation';
	import { setUserName } from '$lib/stores';

	let userName = $state('');
</script>

<div class="flex min-h-screen items-center justify-center bg-primary">
	<div class="w-full max-w-md space-y-6 rounded-lg bg-white p-8 shadow-lg">
		<!-- Header -->
		<div class="text-center">
			<h2 class="text-3xl font-bold text-gray-900">Welcome!</h2>
			<p class="mt-2 text-sm text-gray-600">Please sign in to your account</p>
		</div>

		<!-- Login Form -->
		<form class="space-y-4">
			<!-- Username Field -->
			<div>
				<label for="username" class="block text-sm font-medium text-gray-700">Username</label>
				<input
					bind:value={userName}
					type="text"
					id="username"
					name="username"
					class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-input focus:outline-none focus:ring-indigo-500"
					required
				/>
			</div>

			<!-- Password Field -->
			<div>
				<label for="password" class="block text-sm font-medium text-gray-700">Password</label>
				<input
					type="password"
					id="password"
					name="password"
					class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-input focus:outline-none focus:ring-indigo-500"
					required
				/>
			</div>

			<!-- Remember Me & Forgot Password -->
			<div class="flex items-center justify-between">
				<div class="flex items-center">
					<input
						type="checkbox"
						id="remember-me"
						class="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
					/>
					<label for="remember-me" class="ml-2 block text-sm text-gray-900">Remember me</label>
				</div>
				<div class="text-sm">
					<a href="/" class="font-medium text-input hover:text-indigo-500">Forgot password?</a>
				</div>
			</div>

			<!-- Submit Button -->
			<div>
				<button
					onclick={(e) => {
						e.preventDefault();
						setUserName(userName);
						goto('/calculation/cart');
					}}
					class="flex w-full justify-center rounded-md border border-transparent bg-input px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
				>
					Sign in
				</button>
			</div>
		</form>
	</div>
</div>
