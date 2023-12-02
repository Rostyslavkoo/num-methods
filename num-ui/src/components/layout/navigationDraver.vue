<template>
	<v-navigation-drawer :model-value="drawer" permanent>
		<v-list color="info">
			<div v-for="item in Object.keys(METHODS_ALL)" :key="item" :value="item">
				<v-list-subheader v-if="'type' in METHODS_ALL[item]">{{
					METHODS_ALL[item].type
				}}</v-list-subheader>
				<v-list-item
					:to="{ path: `/${METHODS_ALL[item].text.split(' ').join('-')}` }"
				>
					<template v-slot:prepend>
						<v-icon icon="mdi-math-integral"></v-icon>
					</template>

					<v-list-item-title
						style="text-transform: capitalize"
						v-text="METHODS_ALL[item].text"
					>
					</v-list-item-title>
				</v-list-item>
			</div>
		</v-list>

		<template v-slot:append>
			<v-footer height="15" class="ma-0 pa-0">
				<div
					class="bg-grey-lighten-4 text-grey-lighten-1 text-right w-100 text-caption font-weight-light"
				>
					<strong>v{{ AppVersion }}</strong>
				</div>
			</v-footer>
		</template>
	</v-navigation-drawer>
</template>

<script>
import { version } from './../../../package.json';
import { METHODS_TREE, TOPICS, METHODS_ALL } from './../../constants/methods';

export default {
	props: {
		drawer: {
			require: true,
		},
	},
	data: () => ({
		METHODS_ALL: METHODS_ALL,
		TOPICS: TOPICS,
		group: null,
		AppVersion: version,
	}),
	computed: {},

	watch: {
		group() {
			this.drawer = false;
		},
	},
};
</script>

<style></style>
