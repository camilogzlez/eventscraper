<template>
  <v-app>
    <v-main>
      <ActivityList />
    </v-main>
  </v-app>
</template>

<script>
import ActivityList from './components/ActivityList.vue';

export default {
  components: {
    ActivityList,
  },
};
</script>
