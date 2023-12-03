
export const TOPICS = {
	LINEAR: 'System of linear equations',
	NON_LINEAR: 'Nonlinear equations',
	INTERPOLATIONS: 'Interpolations',
	INTEGRATION: 'Integrations',
};
export const METHODS_ALL = {
	GAUSS: {
		text: 'gauss',
		type: TOPICS.LINEAR,
	},
	SIMPLE_ITARATIONS: {
		text: 'simple iterations',
	},
	LEAST_SQUARES: {
		text: 'least squares',
	},
	CHORD: {
		text: 'chord',
		type: TOPICS.NON_LINEAR,
	},
	NEWTON_NON_LINEAR: {
		text: 'newton non linear',
	},
	NEWTON_INTERPOLATIONS: {
		text: 'newton interpolations',
		type: TOPICS.INTERPOLATIONS,
	},
	LAGRANGE: {
		text: 'lagrange',
	},
	INTEGRAL: {
		text: 'integral',
		type: TOPICS.INTEGRATION,
	},
};
