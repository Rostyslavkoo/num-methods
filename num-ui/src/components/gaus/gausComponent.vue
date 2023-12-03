<template>
	<v-card>
		<v-card-title> Gauss method </v-card-title>
		<v-divider class="mx-3"></v-divider>
		<v-card-text>
			<v-sheet :height="120 * matrixSize" class="pl-1">
				<v-row>
					<v-col cols="12" class="pl-5">
						<v-chip-group v-model="matrixSize" color="primary" mandatory>
							<v-chip v-for="size in matrixSizes" :key="size" :value="size">
								{{ size }}x{{ size }}
							</v-chip>
						</v-chip-group>
					</v-col>
				</v-row>
				<v-row justify="start" align="center">
					<span class="text-h5">A =</span>
					<v-col cols="4">
						<v-row v-for="(row, rowIndex) in matrix" :key="rowIndex">
							<v-col
								v-for="(value, colIndex) in row"
								:key="colIndex"
								:cols="12 / matrixSize"
							>
								<v-text-field
									v-model="matrix[rowIndex][colIndex]"
									label=""
									variant="solo-filled"
									density="compact"
								></v-text-field>
							</v-col>
						</v-row>
					</v-col>
					<v-row justify="start" align="center" class="pl-10">
						<span class="text-h5">b =</span>
						<v-col cols="6">
							<v-row v-for="(row, rowIndex) in matrixB" :key="rowIndex">
								<v-col :cols="12 / matrixSize">
									<v-text-field
										v-model="matrixB[rowIndex]"
										label=""
										variant="solo-filled"
										density="compact"
									></v-text-field>
								</v-col>
							</v-row>
						</v-col>
					</v-row>
				</v-row>
			</v-sheet>
			<v-row class="pl-9">
				<v-col cols="auto">
					<v-btn @click="addRow" color="success" :disabled="matrixSize >= 5">
						<v-icon>mdi-plus</v-icon>
					</v-btn>
				</v-col>
				<v-col cols="auto">
					<v-btn @click="removeRow" color="error" :disabled="matrixSize <= 2">
						<v-icon>mdi-minus</v-icon>
					</v-btn>
				</v-col>
				<v-col cols="auto">
					<v-btn @click="clearMatrix" color="red">
						<v-icon>mdi-close</v-icon>
					</v-btn>
				</v-col>
				<v-col cols="3">
					<v-btn btn @click="submitMatrix" :loading="loading" color="primary">Submit Matrix</v-btn>
				</v-col>
			</v-row>
			<div v-if="result">
				<v-divider class="mt-5"></v-divider>
				<v-row justify="start" align="center" class="mt-4 mb-1 mx-3">
					<span class="text-h5">Result: </span>
					<span class="ml-3">
						{{ result }}
					</span>
				</v-row>
			</div>
		</v-card-text>
	</v-card>
</template>

<script>
import axios from 'axios';
import methods from './../../services/methods.js';

export default {
	data() {
		return {
			matrixSize: 3,
			matrixSizes: [2, 3, 4, 5],
			matrixData: this.initializeMatrixData(3),
			matrixB: Array.from({ length: 3 }, () => Array(1).fill('')), // Initialize with numeric values
			result: '',
			loading:false
		};
	},
	watch: {
		matrixSize(e) {
			this.matrixData = this.initializeMatrixData(e);
			this.matrixB = Array.from({ length: this.matrixSize }, () =>
				Array(1).fill('')
			);
		},
	},
	computed: {
		matrix: {
			get() {
				return this.matrixData;
			},
			set(newMatrix) {
				this.matrixData = newMatrix;
			},
		},
	},
	methods: {
		clearMatrix() {
			this.matrixData = this.initializeMatrixData(this.matrixSize);
			this.matrixB = Array.from({ length: this.matrixSize }, () =>
				Array(1).fill()
			);
			this.matrixSize = 3;
			this.result = '';
		},
		initializeMatrixData(size) {
			return Array.from({ length: size }, () => Array(size).fill(''));
		},
		addRow() {
			this.matrix.push(Array(this.matrixSize).fill(''));
			this.matrixB.push(Array(1).fill(''));
			this.matrix.forEach(row => row.push());
			this.matrixSize++;
		},
		removeRow() {
			if (this.matrix.length > 1) {
				this.matrix.pop();
			}
			if (this.matrixB.length > 1) {
				this.matrixB.pop();
			}
			if (this.matrixSize > 1) {
				this.matrix.forEach(row => row.pop());
				this.matrixSize--;
			}
		},

		async submitMatrix() {
			try {
				this.loading = true
				this.result = await methods.gauss({
					A: this.matrix.map(row => row.map(Number)),
					b: this.matrixB.map(Number),
				});
			} catch (e) {
				this.result = e?.response?.data?.detail;
			}
			finally{
				this.loading = false
			}
		},
	},
};
</script>

<style scoped>
/* Add styles as needed */
</style>
