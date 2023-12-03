import requestService from './requestService';

export default {

	async gauss(payload) {
		const response = await requestService.post('gauss', payload);
		return response?.data;
	},
};
