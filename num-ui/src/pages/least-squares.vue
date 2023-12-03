<template>
	<layout-component
		><least-squares-component></least-squares-component
	></layout-component>
</template>

<script>
import LeastSquaresComponent from '../components/leastSquares/leastSquaresComponent.vue';
import layoutComponent from '../components/layout/layoutComponent.vue';

export default {
	components: { layoutComponent, LeastSquaresComponent },
};
</script>

<style></style>
