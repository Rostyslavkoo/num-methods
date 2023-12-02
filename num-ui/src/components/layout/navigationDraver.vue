<template>
	<v-navigation-drawer :model-value="drawer" permanent>
		<v-list :items="items"></v-list>
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

export default {
	props: {
		drawer: {
			require: true,
		},
	},
	data: () => ({
		group: null,
		AppVersion: version,
		items: [
			{
				title: 'Foo',
				value: 'foo',
			},
			{
				title: 'Bar',
				value: 'bar',
			},
			{
				title: 'Fizz',
				value: 'fizz',
			},
			{
				title: 'Buzz',
				value: 'buzz',
			},
		],
	}),

	watch: {
		group() {
			this.drawer = false;
		},
	},
};
</script>

<style></style>
