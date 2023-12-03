<template>
	<div>{{ result }}</div>
</template>

<script>
import axios from 'axios';
import methods from './../../services/methods.js';

export default {
	data: () => ({
		result: '',
	}),
	async mounted() {
		this.result = await methods.gauss({
			A: [
				[1, 2, 3],
				[4, 5, 6],
				[7, 8, 9],
			],
			b: [1, 2, 3],
		});
	},
};
</script>

<style></style>
