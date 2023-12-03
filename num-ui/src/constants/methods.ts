export const METHODS_TREE = {
	LINEAR: {
		GAUSS: 'Gauss',
		SIMPLE_ITARATIONS: 'Simple iterations',
		NEWTON_LINEAR: 'Newton',
	},
	NON_LINEAR: {
		CHORD: 'Chord',
		NEWTON_NON_LINEAR: 'Newton',
	},
	INTERPOLATIONS: {
		NEWTON_INTERPOLATIONS: 'Newton',
		LAGRANGE: 'Lagrange',
	},
	INTEGRATION: {
		INTEGRAL: 'Integral',
	},
};
export const TOPICS = {
	LINEAR: 'Linear',
	NON_LINEAR: 'Non Linear',
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
	},
};
