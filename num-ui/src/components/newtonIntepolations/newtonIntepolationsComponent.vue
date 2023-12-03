<template>
	<v-card>
		<v-card-title> Newton Interpolation method </v-card-title>
		<v-divider class="mx-3"></v-divider>
		<v-card-text>
			<v-sheet :height="120 * rowSize" class="pl-1">
				<v-row justify="start" align="center">
				
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
                                    hide-details
								></v-text-field>
							</v-col>
						</v-row>
					</v-col>
					<v-row justify="start" align="center" class="pl-10">
						<span class="text-h5">x =</span>
						<v-col cols="6">
							<v-row>
								<v-col cols="3">
									<v-text-field
										v-model="xQuery"
										label=""
										variant="solo-filled"
										density="compact"
                                        hide-details
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
					<span class="ml-3">Y = {{ result }}</span>
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
			matrixSize: 2,
			matrixData: this.initializeMatrixData(2),
			result: undefined,
			rowSize: 3,
			loading:false,
            xQuery:'',
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
			return Array.from({ length: size +1}, () => Array(size).fill(''));
		},
		addRow() {
			this.matrix.push(Array(this.matrixSize).fill(''));
			this.rowSize++;
		},
		removeRow() {
			if (this.matrix.length > 1) {
				this.matrix.pop();
			}
			this.rowSize--;
		},
		clearMatrix() {
            this.rowSize = 3
            this.matrixSize = 2,
			this.matrixData = this.initializeMatrixData(2);
			this.result = undefined;
            this.xQuery =''
		},
		async submitMatrix() {
			try {
				this.loading = true
				this.result = await methods.newtonInter({
					matrix: this.matrix.map(row => row.map(Number)),
					x:+this.xQuery
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
