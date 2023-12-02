<template>
	<v-card>
		<router-view></router-view>
	</v-card>
</template>

<script>
import layoutComponent from './components/layout/layoutComponent.vue';
export default {
	components: {
		layoutComponent,
	},
};
</script>
