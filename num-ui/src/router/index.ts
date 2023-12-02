import { createRouter, createWebHistory } from 'vue-router';

const routes = [
	{
		path: '/',
		component: () => import('./../pages/Gaus.vue'),
		meta: { title: 'Gaus method' },
	},
];
const router = createRouter({
	history: createWebHistory(),
	routes: routes,
});

export default router;
