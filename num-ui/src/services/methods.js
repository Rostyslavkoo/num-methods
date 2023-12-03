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
	async chord(payload) {
		const response = await requestService.post('chord', payload);
		return response?.data;
	},
	async newton(payload) {
		const response = await requestService.post('newton', payload);
		return response?.data;
	},
	async newtonInter(payload) {
		const response = await requestService.post('newton-inter', payload);
		return response?.data;
	},
	async lagrange(payload) {
		const response = await requestService.post('lagrange', payload);
		return response?.data;
	},
};
