<template>
  <v-container fluid class="pa-0">
    <v-row dense justify="center">
      <!-- Paginated Activities -->
      <v-col
        v-for="activity in paginatedActivities"
        :key="activity.id"
        cols="12"
        sm="6"
        md="4"
        lg="3"
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
    <div class="tw-flex tw-justify-center tw-mt-6 tw-space-x-2">
      <button
        @click="goToPage(currentPage - 1)"
        :disabled="currentPage === 1"
        class="tw-px-3 tw-py-2 tw-text-white tw-bg-gray-500 tw-rounded tw-hover:bg-gray-700 tw-disabled:bg-gray-300"
      >
        Previous
      </button>

      <button
        v-for="page in totalPages"
        :key="page"
        @click="goToPage(page)"
        class="tw-px-3 tw-py-2 tw-rounded"
        :class="{
          'tw-bg-blue-500 tw-text-white': currentPage === page,
          'tw-bg-gray-200 tw-hover:bg-gray-300': currentPage !== page,
        }"
      >
        {{ page }}
      </button>

      <button
        @click="goToPage(currentPage + 1)"
        :disabled="currentPage === totalPages"
        class="tw-px-3 tw-py-2 tw-text-white tw-bg-gray-500 tw-rounded tw-hover:bg-gray-700 tw-disabled:bg-gray-300"
      >
        Next
      </button>
    </div>
  </v-container>
</template>

<script>
export default {
  props: {
    activities: Array, // Array of activities
  },
  data() {
    return {
      currentPage: 1, // Current page number
      itemsPerPage: 8, // Items per page
    };
  },
  computed: {
    // Calculate total pages based on activities length and itemsPerPage
    totalPages() {
      return Math.ceil(this.activities.length / this.itemsPerPage);
    },
    // Paginated activities based on current page
    paginatedActivities() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.activities.slice(start, end);
    },
  },
  methods: {
    // Navigate to a specific page
    goToPage(page) {
      if (page > 0 && page <= this.totalPages) {
        this.currentPage = page;
      }
    },
    getRandomColor() {
      const colors = ["#9d2f38", "#25798b", "#72a9fe", "#f9c904", "#323f46"];
      return colors[Math.floor(Math.random() * colors.length)];
    },
    sourceIcon(source) {
      switch (source.toLowerCase()) {
        case "eventbrite":
          return "mdi-calendar-star";
        case "tripadvisor":
          return "mdi-map-outline";
        case "facebook":
          return "mdi-facebook";
        default:
          return "mdi-help-circle";
      }
    },
    sourceIconColor(source) {
      switch (source.toLowerCase()) {
        case "eventbrite":
          return "orange";
        case "tripadvisor":
          return "green";
        case "facebook":
          return "blue";
        default:
          return "gray";
      }
    },
  },
};
</script>

<style scoped>
.transition-card {
  transition: box-shadow 0.3s ease-in-out, transform 0.3s ease-in-out;
}
.transition-card:hover {
  transform: scale(1.02); /* Slight zoom on hover */
}
</style>
