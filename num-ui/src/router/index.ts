import { createRouter, createWebHistory } from 'vue-router';
import { METHODS_ALL } from '../constants/methods';

const routes = [
	{
		path: '/',
		component: () => import('./../pages/gauss.vue'),
		meta: { title: 'Gaus method' },
	},
];
Object.keys(METHODS_ALL).forEach(methodKey => {
	let routeName = METHODS_ALL[methodKey].text;
	routeName = routeName.split(' ').join('-');
	routes.push({
		path: `/${routeName}`,
		component: () => import(`./../pages/${routeName}.vue`),
		meta: { title: 'Gaus method' },
	});
});
const router = createRouter({
	history: createWebHistory(),
	routes: routes,
});

export default router;
