import requestService from './requestService';

export default {

	async gauss(payload) {
		const response = await requestService.post('gauss', payload);
		return response?.data;
	},
	async simpleItarations(payload) {
		const response = await requestService.post('simple-iterations', payload);
		return response?.data;
	},
	async leastSquares(payload) {
		const response = await requestService.post('least-squares', payload);
		return response?.data;
	},
};
