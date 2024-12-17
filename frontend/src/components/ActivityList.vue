<template>
  <v-container fluid class="12 justify-center align-center text-center pa-0 fill-height">
    <!-- Header Section -->
    <v-col cols="12 justify-center align-center text-center">
        <v-img

          src="/logoeventsfinder.png"
          height="200"
          width="auto"
          class="mx-auto"
        ></v-img>
        <v-btn color="primary" @click="startScraping" class="mt-4 mb-4" large>
          Scrape activities in Montpellier
        </v-btn>

<!-- Toggle Filters Button and Filters Section -->
<v-row class="justify-center">
  <!-- Toggle Button -->
    <v-btn
      color="blue-grey-lighten-1"
      text="true"
      small
      @click="showFilters = !showFilters"
      class="my-2"
      outlined
    >
      <v-icon left>
        {{ showFilters ? 'mdi-chevron-up' : 'mdi-chevron-down' }}
      </v-icon>
      {{ showFilters ? 'Hide Filters' : 'Show Filters' }}
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
          <v-menu
            v-model="startDatePicker"
            :close-on-content-click="false"
            offset-y
          >
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
            <v-date-picker
              v-model="startDate"
              @input="startDatePicker = false"
            />
          </v-menu>
        </v-col>

        <!-- End Date -->
        <v-col cols="12" sm="2">
          <v-menu
            v-model="endDatePicker"
            :close-on-content-click="false"
            offset-y
          >
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
            <v-date-picker
              v-model="endDate"
              @input="endDatePicker = false"
            />
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
          <v-btn
            color="teal-lighten-1"
            @click="clearFilters"
            dense
            outlined
            block
          >
            Clear
          </v-btn>
        </v-col>
      </v-row>
    </v-col>
  </v-expand-transition>
    </v-col>

    <!-- Alert Message -->
    <v-alert v-if="message" :type="messageType" class="mt-3">
      {{ message }}
    </v-alert>

    <!-- Activities Grid -->
    <activities-grid :activities="filteredActivities" />
  </v-container>
</template>

<script>
import api from "../services/api";
import ActivitiesGrid from "./ActivitiesGrid.vue";

export default {
  components: {
    ActivitiesGrid,
  },
  data() {
    return {
      showFilters: false, // Filters hidden by default
      activities: [],
      filteredActivities: [],
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
    };
  },
  methods: {
    async startScraping() {
      try {
        const response = await api.post("/scrape");
        if (response.data.success) {
          this.message = response.data.message;
          this.messageType = "success";
          this.fetchActivities();
        }
      } catch (error) {
        this.message = "Failed to start scraping: " + error.response.data.message;
        this.messageType = "error";
      }
    },
    async fetchActivities() {
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
    },
    clearFilters() {
      this.searchQuery = "";
      this.selectedSource = null;
      this.startDate = null;
      this.endDate = null;
      this.sortOption = null;
      this.applyFilters();
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

<style scoped>
.v-btn {
  min-height: 36px;
}

@media (max-width: 600px) {
  .v-col {
    margin-bottom: 10px;
  }
}
</style>
