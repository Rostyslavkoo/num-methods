<template>
	<v-card>
		<v-card-title> Newton method </v-card-title>
		<v-divider class="mx-3"></v-divider>
		<v-card-text>
			<v-sheet height="100" class="pl-1">
				<v-row>
					<v-col cols="5">
						<v-text-field
							v-model="functionQuery"
							label="function"
							density="compact"
						></v-text-field>
					</v-col>
				</v-row>
			</v-sheet>
			<v-row class="">
				<v-col cols="auto">
					<v-btn @click="clearMatrix" color="red">
						<v-icon>mdi-close</v-icon>
					</v-btn>
				</v-col>
				<v-col cols="3">
					<v-btn
						btn
						@click="submitMatrix"
						color="primary"
						:disabled="!functionQuery"
						:loading="loading"
						>Submit Matrix</v-btn
					>
				</v-col>
			</v-row>
			<div v-if="result !== null">
				<v-divider class="mt-5"></v-divider>
				<v-row justify="start" align="center" class="mt-4 mb-1 mx-3">
					<span class="text-h5">Result: </span>
					<span class="ml-3">{{ result }}</span>
				</v-row>
			</div>
		</v-card-text>
	</v-card>
</template>

<script>
import methods from './../../services/methods';

export default {
	data() {
		return {
			functionQuery: 'x**3-13*x-1',
			result: null,
			loading: false,
		};
	},

	methods: {
		clearMatrix() {
			this.functionQuery = '';
			this.result = null;
		},
		async submitMatrix() {
			try {
				this.loading = true;
				this.result = await methods.newton({
					function: this.functionQuery,
				});
			} catch (e) {
				this.result = e?.response?.data?.detail;
			} finally {
				this.loading = false;
			}
		},
	},
};
</script>
