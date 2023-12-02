<template>
	<v-layout>
		<v-app-bar color="info" prominent>
			<v-app-bar-nav-icon
				variant="text"
				@click.stop="drawer = !drawer"
			></v-app-bar-nav-icon>

			<v-toolbar-title class="font-weight-bold"
				>Numerical Methods</v-toolbar-title
			>
			<v-spacer></v-spacer>

			<v-btn variant="text" icon="mdi-magnify"></v-btn>
			<v-btn variant="text" icon="mdi-bell"></v-btn>
			<v-btn variant="text" icon="mdi-dots-vertical"></v-btn>
		</v-app-bar>

		<navigation-draver :drawer="drawer"></navigation-draver>

		<v-main>
			<v-card-text>
				<slot></slot>
			</v-card-text>
		</v-main>
	</v-layout>
</template>

<script>
import navigationDraver from './navigationDraver.vue';
const MENU_OPEN_DEFAULT_STATE = true;

export default {
	data: () => ({
		drawer: MENU_OPEN_DEFAULT_STATE,
	}),
	components: {
		navigationDraver,
	},
};
</script>

<style></style>
