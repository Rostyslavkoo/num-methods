<template>
	<v-card>
		<v-card-title> Least Squares method </v-card-title>
		<v-divider class="mx-3"></v-divider>
		<v-card-text>
			<v-sheet :height="120 * rowSize" class="pl-1">
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
					<v-btn @click="addRow" color="success" :disabled="rowSize >= 5">
						<v-icon>mdi-plus</v-icon>
						row
					</v-btn>
				</v-col>
				<v-col cols="auto">
					<v-btn @click="removeRow" color="error" :disabled="rowSize <= 2">
						<v-icon>mdi-minus</v-icon>
						row
					</v-btn>
				</v-col>
				<v-col cols="auto">
					<v-btn @click="addCol" color="success" :disabled="matrixSize >= 5">
						<v-icon>mdi-plus</v-icon>
						col
					</v-btn>
				</v-col>
				<v-col cols="auto">
					<v-btn @click="removeCol" color="error" :disabled="matrixSize <= 2">
						<v-icon>mdi-minus</v-icon>
						col
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
			<div v-if="result !== undefined">
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
			matrixSize: 3,
			matrixSizes: [2, 3, 4, 5],
			matrixData: this.initializeMatrixData(3),
			matrixB: Array.from({ length: 3 }, () => Array(1).fill('')),
			result: undefined,
			rowSize: 3,
			loading:false
		};
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
		initializeMatrixData(size) {
			return Array.from({ length: size }, () => Array(size).fill(''));
		},
		addRow() {
			this.matrix.push(Array(this.matrixSize).fill(''));
			this.matrixB.push(Array(1).fill(''));
			this.rowSize++;
		},
		removeRow() {
			if (this.matrix.length > 1) {
				this.matrix.pop();
			}
			if (this.matrixB.length > 1) {
				this.matrixB.pop();
			}
			this.rowSize--;
		},
		addCol() {
			this.matrix.forEach(row => row.push(''));
			this.matrixSize++;
		},
		removeCol() {
			if (this.matrixSize > 1) {
				this.matrix.forEach(row => row.pop());
				this.matrixSize--;
			}
		},
		clearMatrix() {
            this.rowSize = 3
            this.matrixSize = 3,
			this.matrixData = this.initializeMatrixData(3);
			this.matrixB = Array.from({ length: 3 }, () =>
				Array(1).fill('')
			);
			this.result = undefined;
		},
		async submitMatrix() {
			try {
				this.loading = true
				this.result = await methods.leastSquares({
					A: this.matrix.map(row => row.map(Number)),
					b: this.matrixB.map(Number),
				});
			} catch (e) {
				this.result = e?.response?.data?.detail;
			}finally{
				this.loading = false
			}
		},
	},
};
</script>
