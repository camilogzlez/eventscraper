<template>
  <v-container  fluid class="pa-0">
    <v-row dense justify="center">
      <!-- Paginated Activities -->
      <v-col
        v-for="activity in paginatedActivities"
        :key="activity.id"
        cols="12"
        :sm="showMap ? 6 : 6"
        :md="showMap ? 6 : 4"
        :lg="showMap ? 6 : 3"
        class="pa-3"
      >
        <v-hover>
          <template v-slot:default="{ isHovering }">
            <v-card
              :href="activity.url"
              target="_blank"
              class="mx-auto transition-card"
              max-width="500"
              :elevation="isHovering ? 8 : 2"
              ripple
              :style="{ border: `1px solid ${getRandomColor()}` }"
              elevation="0"
            >
              <v-img
                :src="activity.image_url"
                class="align-end"
                gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"
                height="200px"
                cover
              ></v-img>

              <!-- Card Actions Section -->
              <v-card-actions class="d-flex flex-column justify-start align-start pa-4">
                <div class="text-black text-h6 font-weight-bold mb-2">
                  {{ activity.name }}
                </div>

                <div class="d-flex flex-row align-center mb-1">
                  <v-icon color="blue" class="mr-2">mdi-map-marker</v-icon>
                  <span>{{ activity.location }}</span>
                </div>

                <div class="d-flex flex-row align-center mb-1">
                  <v-icon color="orange" class="mr-2">mdi-calendar</v-icon>
                  <span>{{ activity.date }}</span>
                </div>

                <div class="d-flex flex-row align-center mb-1">
                  <v-icon color="green" class="mr-2">mdi-currency-usd</v-icon>
                  <span>{{ activity.price }}</span>
                </div>

                <div class="d-flex flex-row align-center">
                  <v-icon :color="sourceIconColor(activity.source)" class="mr-2">
                    {{ sourceIcon(activity.source) }}
                  </v-icon>
                  <span>{{ activity.source }}</span>
                </div>
              </v-card-actions>
            </v-card>
          </template>
        </v-hover>
      </v-col>
    </v-row>

    <!-- Pagination Controls -->
    <div
      v-if="activities.length > 0"
      class="tw-flex tw-justify-center tw-mt-6 tw-space-x-2"
    >
      <v-pagination
        v-model="currentPage"
        :length="totalPages"
        :total-visible="7"
        color="primary"
      ></v-pagination>
    </div>
  </v-container>
</template>

<script>
export default {
  props: {
    activities: Array,
    showMap: Boolean,
  },
  data() {
    return {
      currentPage: 1,
      itemsPerPage: 8,
    };
  },
  computed: {
    paginatedActivities() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      return this.activities.slice(start, start + this.itemsPerPage);
    },
    totalPages() {
      return Math.ceil(this.activities.length / this.itemsPerPage);
    },
  },
  methods: {
    getRandomColor() {
      const colors = ["#9d2f38", "#25798b", "#72a9fe", "#f9c904", "#323f46"];
      return colors[Math.floor(Math.random() * colors.length)];
    },
    sourceIconColor(source) {
      return source === "eventbrite" ? "red" : "blue";
    },
    sourceIcon(source) {
      return source === "eventbrite" ? "mdi-ticket" : "mdi-web";
    },
  },
};
</script>

<style scoped>

@media (max-width: 400px) {
  .v-col {
    width: 100% !important;
    margin: 10px 0 !important; }
}

</style>
