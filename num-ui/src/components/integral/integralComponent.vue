<template>
	<v-card>
		<v-card-title> Integral method </v-card-title>
		<v-divider class="mx-3"></v-divider>
		<v-card-text>
			<v-sheet height="100" class="pl-1">
				<v-row>
					<v-col cols="4">
						<v-text-field
							v-model="functionQuery"
							label="function"
							density="compact"
						></v-text-field>
					</v-col>
					<v-col cols="1">
						<v-text-field
							v-model="aQuery"
							label="a"
							density="compact"
						></v-text-field>
					</v-col>
					<v-col cols="1">
						<v-text-field
							v-model="bQuery"
							label="b"
							density="compact"
						></v-text-field>
					</v-col>
					<v-col cols="1">
						<v-text-field
							v-model="nQuery"
							label="n"
							density="compact"
						></v-text-field>
					</v-col>
				</v-row>
			</v-sheet>
			<v-row class="">
				<v-col cols="auto">
					<v-btn @click="clearMatrix" color="grey">
						<v-icon>mdi-close</v-icon>
					</v-btn>
				</v-col>
				<v-col cols="3">
					<v-btn
						btn
						@click="submitMatrix"
						color="primary"
						:disabled="!functionQuery || !aQuery || !bQuery || !nQuery"
						:loading="loading"
						>Submit Matrix</v-btn
					>
				</v-col>
			</v-row>
			<div v-if="result !== undefined">
				<v-divider class="mt-5"></v-divider>
				<v-row justify="start" align="center" class="mt-4 mb-1 mx-3">
					<span class="text-h5">Result: </span>
					
					<div v-if="'result_rectangles' in result">
						<v-col> Rectangles: {{ result.result_rectangles }} </v-col>
						<v-col> Trapezium: {{ result.result_trapezium }} </v-col>
						<v-col> Simpsons: {{ result.result_simpsons }} </v-col>
					</div>
					<span class="ml-3" v-else>{{ result }}</span>
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
			aQuery: '',
			bQuery: '',
			nQuery: '',
			result: undefined,
			loading: false,
		};
	},

	methods: {
		clearMatrix() {
			this.functionQuery = '';
			this.result = undefined;
			this.aQuery = '';
			this.bQuery = '';
			this.nQuery = '';
		},
		async submitMatrix() {
			try {
				this.loading = true;
				this.result = await methods.integral({
					function: this.functionQuery,
					a: this.aQuery,
					b: this.bQuery,
					n: this.nQuery,
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
