<template>
  <v-container>
    <v-btn color="primary" @click="startScraping">
      Start Scraping
    </v-btn>
    <v-alert v-if="message" :type="messageType" class="mt-3">
      {{ message }}
    </v-alert>
    <v-data-table
      v-if="activities.length"
      :items="activities"
      :headers="headers"
      class="mt-5"
      item-value="id"
    ></v-data-table>
  </v-container>
</template>

<script>
import api from '../services/api';
// import axios from "axios";

export default {
  data() {
    return {
      activities: [],
      message: "",
      messageType: "success",
      headers: [
        { text: "Name", value: "name" },
        { text: "Location", value: "location" },
        { text: "Date", value: "date" },
        { text: "Source", value: "source" },
        { text: "Price", value: "price" },
        { text: "URL", value: "url" },
      ],
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
        this.message = "Failed to start scraping: "   + error.response.data.message;
        this.messageType = "error";
      }
    },
    async fetchActivities() {
      try {
        const response = await api.get("/scraped-data");
        this.activities = response.data;
      } catch (error) {
        this.message = "Failed to fetch activities: " + error.message;
        this.messageType = "error";
      }
    },
  },
  mounted() {
    this.fetchActivities();
  },
};
</script>
