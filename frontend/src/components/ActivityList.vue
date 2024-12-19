<template>
  <v-container fluid class="justify-center align-center text-center pa-0 fill-height">
    <!-- Header Section -->
    <v-col cols="12" class="justify-center align-center text-center">
      <v-img src="/logoeventsfinder.png" height="200" width="auto" class="mx-auto"></v-img>
      <v-btn color="primary" @click="startScraping" class="mt-4 mb-4" large>
        Scrape activities in Montpellier
      </v-btn>

<v-progress-linear
  v-if="loading"
  indeterminate
  color="#f9c904"
  class="mt-2"
  height="32"
>
  <template v-slot:default>
    <span class="text-white">Loading, please wait...</span>
  </template>
</v-progress-linear>

      <v-alert v-if="message" :type="messageType" class="mt-3 justify-center">
      {{ message }}
    </v-alert>
    </v-col>


    <!-- Toggle Buttons for Filters and Map -->
    <v-row class="justify-center" v-if="activities.length > 0">
      <!-- Filters Toggle -->
      <v-btn
        color="#9d2f38"
        text
        small
        @click="showFilters = !showFilters"
        class="my-2 mx-2"
        outlined
        style="color: white;"
      >
        <v-icon left>
          {{ showFilters ? 'mdi-chevron-up' : 'mdi-chevron-down' }}
        </v-icon>
        {{ showFilters ? 'Hide Filters' : 'Show Filters' }}
      </v-btn>

      <!-- Map Toggle -->
      <v-btn
        color="#25798b"
        text
        small
        @click="showMap = !showMap"
        class="my-2 mx-2"
        outlined
        style="color: white;"
      >
        <v-icon left>
          {{ showMap ? 'mdi-map-marker-off' : 'mdi-map-marker' }}
        </v-icon>
        {{ showMap ? 'Hide Map' : 'Show Map' }}
      </v-btn>
       <!-- AI Assistant Toggle -->
      <v-btn
        color="#72a9fe"
        text
        small
        @click="toggleAssistantModal"
        class="my-2 mx-2"
        outlined
        style="color: white;"
      >
        🤟 AI Assistant(Beta)
      </v-btn>
    </v-row>

    <!-- Filters Section -->
    <v-expand-transition>
      <v-col cols="12" v-if="showFilters" class="text-center">
        <v-row class="justify-center">
          <!-- Search Bar -->
          <v-col cols="12" sm="3">
            <v-text-field
              v-model="searchQuery"
              label="Search Activities"
              outlined
              dense
              hide-details
            />
          </v-col>

          <!-- Filter by Source -->
          <v-col cols="12" sm="2">
            <v-select
              v-model="selectedSource"
              :items="sources"
              label="Filter by Source"
              outlined
              dense
              hide-details
            />
          </v-col>

          <!-- Start Date -->
          <v-col cols="12" sm="2">
            <v-menu v-model="startDatePicker" :close-on-content-click="false" offset-y>
              <template v-slot:activator="{ on, attrs }">
                <v-text-field
                  v-model="startDate"
                  label="Start Date"
                  readonly
                  outlined
                  dense
                  v-bind="attrs"
                  v-on="on"
                  hide-details
                />
              </template>
              <v-date-picker v-model="startDate" @input="startDatePicker = false" />
            </v-menu>
          </v-col>

          <!-- End Date -->
          <v-col cols="12" sm="2">
            <v-menu v-model="endDatePicker" :close-on-content-click="false" offset-y>
              <template v-slot:activator="{ on, attrs }">
                <v-text-field
                  v-model="endDate"
                  label="End Date"
                  readonly
                  outlined
                  dense
                  v-bind="attrs"
                  v-on="on"
                  hide-details
                />
              </template>
              <v-date-picker v-model="endDate" @input="endDatePicker = false" />
            </v-menu>
          </v-col>

          <!-- Sort By -->
          <v-col cols="12" sm="2">
            <v-select
              v-model="sortOption"
              :items="sortOptions"
              label="Sort By"
              outlined
              dense
              hide-details
            />
          </v-col>

          <!-- Clear Filters Button -->
          <v-col cols="12" sm="1" class="d-flex align-center">
            <v-btn color="#25798b" @click="clearFilters" dense outlined block>
              Clear
            </v-btn>
          </v-col>
        </v-row>
      </v-col>
    </v-expand-transition>

    <!-- Alert Message -->


    <!-- Main Content Section -->
<v-row class="pa-4">
  <!-- Activities Grid -->
  <v-col :cols="showMap ? 6 : 12">
    <activities-grid :activities="filteredActivities" :showMap="showMap" />
  </v-col>

  <!-- Map Component (Only visible when toggled on) -->
<v-col v-if="showMap" cols="6" class="map-col">
  <map-activities :activities="filteredActivities" />
</v-col>
</v-row>
    <v-dialog v-model="showAssistantModal" max-width="2400" max-height="1500">
      <IAAssistant @close="toggleAssistantModal" />
    </v-dialog>

  </v-container>
</template>

<script>
import api from "../services/api";
import ActivitiesGrid from "./ActivitiesGrid.vue";
import MapActivities from "./MapActivities.vue";
import IAAssistant from "./IAAssistant.vue";

export default {
  components: {
    ActivitiesGrid,
    MapActivities,
    IAAssistant,
  },
  data() {
    return {
      loading: false,
      showFilters: false, // Show/hide filters
      showMap: false, // Show/hide map
      activities: [],
      filteredActivities: [],
      mapKey: 0,
      message: "",
      messageType: "success",
      searchQuery: "",
      selectedSource: null,
      startDate: null,
      endDate: null,
      startDatePicker: false,
      endDatePicker: false,
      sortOption: null,
      sources: ["eventbrite", "tripadvisor", "facebook"],
      sortOptions: ["Name", "Date"],
      showAssistantModal: false,
    };
  },
  methods: {
    async startScraping() {
       this.loading = true;
      try {
        const response = await api.post("/scrape");
        if (response.data.success) {
          this.message = response.data.message;
          this.messageType = "success";
          setTimeout(() => {
        this.message = "";
      }, 2000);
          this.fetchActivities();
        }
      } catch (error) {
        this.message = "Failed to start scraping: " + error.response.data.message;
        this.messageType = "error";
      }
    },
    async fetchActivities() {
       this.loading = false;
      try {
        const response = await api.get("/scraped-data");
        this.activities = response.data;
        this.filteredActivities = [...this.activities];
        this.applyFilters();
      } catch (error) {
        this.message = "Failed to fetch activities: " + error.message;
        this.messageType = "error";
      }
    },
    applyFilters() {
      this.filteredActivities = this.activities
        .filter((activity) => {
          if (!this.searchQuery) return true;
          return (
            activity.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
            activity.location.toLowerCase().includes(this.searchQuery.toLowerCase())
          );
        })
        .filter((activity) => {
          if (!this.selectedSource) return true;
          return activity.source.toLowerCase() === this.selectedSource.toLowerCase();
        })
        .filter((activity) => {
          if (!this.startDate && !this.endDate) return true;
          const activityDate = new Date(activity.date);
          const start = this.startDate ? new Date(this.startDate) : null;
          const end = this.endDate ? new Date(this.endDate) : null;
          return (!start || activityDate >= start) && (!end || activityDate <= end);
        })
        .sort((a, b) => {
          if (this.sortOption === "Name") {
            return a.name.localeCompare(b.name);
          } else if (this.sortOption === "Date") {
            return new Date(a.date) - new Date(b.date);
          }
          return 0;
        });
      this.mapKey += 1;
    },
    clearFilters() {
      this.searchQuery = "";
      this.selectedSource = null;
      this.startDate = null;
      this.endDate = null;
      this.sortOption = null;
      this.applyFilters();
    },
    toggleAssistantModal() {
      this.showAssistantModal = !this.showAssistantModal;
    },
  },
  watch: {
    searchQuery: "applyFilters",
    selectedSource: "applyFilters",
    startDate: "applyFilters",
    endDate: "applyFilters",
    sortOption: "applyFilters",
  },
  mounted() {
    this.fetchActivities();
  },
};
</script>
final

<style scoped>
.v-btn {
  min-height: 36px;
}

@media (max-width: 960px) {
  /* Stack map and cards vertically with the map on top */
  .V-container {
    justify-content: center;
    align-content: center;
    display: flex;
    flex-direction: column;
  }

  /* Ensure map is displayed first */
  .map-col {
    order: -1;
  }

  /* Set the map to take full width on mobile */
  .v-col {
    width: 100%;
  }
}


</style>