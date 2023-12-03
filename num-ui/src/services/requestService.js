// eslint-disable-next-line import/no-cycle
import axios from 'axios';

const API_ENDPOINT = 'http://127.0.0.1:3000/'

export default {
	get(url, params = {}, headers = {}, errorNotify = true) {
		return axios
			.get(API_ENDPOINT + url, {
				params,
				headers,
			})
			.catch(error => {
				return Promise.reject(error);
			});
	},
	post(url, body = {}, config = {}, errorNotify = true) {
		return axios
			.post(API_ENDPOINT + url, body, { header: config })
			.catch(error => {
				return Promise.reject(error);
			});
	},
};
