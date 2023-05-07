<script>
	import { Textarea, Label, Button, Spinner } from 'flowbite-svelte';
	import github from '$lib/assets/github.svg';
	import modal from '$lib/assets/modal.svg';

	let schema = JSON.stringify(
		{
			type: 'object',
			properties: {
				car: {
					type: 'object',
					properties: {
						make: {
							type: 'string'
						},
						model: {
							type: 'string'
						},
						year: {
							type: 'number'
						},
						colors: {
							type: 'array',
							items: {
								type: 'string'
							}
						}
					}
				}
			}
		},
		null,
		2
	);

	let prompt =
		'Generate a JSON object for a Maruti Swift 2018 that is available in red and yellow colors';

	let response = JSON.stringify(
		{
			car: {
				make: 'Maruti',
				model: 'Swift',
				year: 2018.0,
				colors: ['red']
			}
		},
		null,
		2
	);

	let isLoading = false;

	async function submitForm() {
		isLoading = true;

		const requestOptions = {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({
				prompt: prompt,
				json_schema: JSON.parse(schema)
			})
		};

		const res = await fetch(
			'https://1rgs--jsonformer-example-3b-web.modal.run/generate',
			requestOptions
		);

		const data = await res.json();
		response = JSON.stringify(data, null, 2);

		isLoading = false;
	}
</script>

<svelte:head>
	<title>Home</title>
	<meta name="description" content="Svelte demo app" />
</svelte:head>

<section>
	<div class="flex justify-center items-center mb-8 gap-3">
		<h1>Jsonformer demo</h1>
		<a href="https://github.com/1rgs/jsonformer" target="_blank" rel="noopener noreferrer">
			<img src={github} alt="github" class="transform translate-y-1 width-6 hover:scale-110" />
		</a>
	</div>

	<div class="response">
		{response}
	</div>
	<form on:submit|preventDefault={submitForm}>
		<Label for="jsonschema" class="mb-2 text-left">JSON Schema</Label>
		<Textarea bind:value={schema} id="jsonschema" rows="4" name="jsonschema" />
		<Label for="prompt" class="mb-2 text-left">Prompt</Label>
		<Textarea bind:value={prompt} id="prompt" rows="4" name="prompt" />
		<div class="submit-btn">
			{#if isLoading}
				<Spinner />
			{:else}
				<Button type="submit">Submit</Button>
			{/if}
		</div>
	</form>

	<div class="flex justify-center items-center flex-col gap-3 mt-8">
		<p class="text-center">Powered by</p>

		<a href="https://modal.com" target="_blank" rel="noopener noreferrer">
			<img
				src={modal}
				alt="modal"
				class="transform translate-y-1 hover:scale-110 transition-all w-28"
			/>
		</a>
	</div>
</section>

<style>
	:root {
		--text-color: #f8f8f8;
		--input-text-color: #ffffff;
		--response-bg-color: #c7efcf;
		--border-color: #444;
	}

	body {
		color: var(--text-color);
	}

	.corner {
		width: 3em;
		height: 3em;
		position: fixed;
		top: 0;
		right: 0;
	}

	form {
		width: 100%;
		max-width: 500px;
		margin-top: 40px;
	}

	section {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		flex: 0.6;
		padding: 1rem;
	}

	h1 {
		width: 100%;
		font-size: 2.5rem;
		text-align: center;
	}

	.response {
		width: 100%;
		max-width: 500px;
		min-height: 150px;
		margin-bottom: 20px;
		white-space: pre-wrap;
		word-wrap: break-word;
		font-family: monospace;

		padding: 10px;
		background-color: var(--response-bg-color);
	}

	textarea {
		background-color: var(--input-bg-color);
		color: var(--input-text-color);
	}

	.submit-btn {
		margin-top: 20px;
	}

	/* Responsive styles */
	@media screen and (max-width: 767px) {
		form,
		.response {
			max-width: 100%;
		}
	}
</style>
