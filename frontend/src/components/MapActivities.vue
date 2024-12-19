<template>
  <v-container  fluid class="justify-center pa-0">
    <l-map style="height: 500px; width: 100%;" :zoom="14" :center="[43.611, 3.877]">
      <l-tile-layer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution="&copy; OpenStreetMap contributors"
      />
      <l-marker
        v-for="(latLng, index) in activityCoordinates"
        :key="index"
        :lat-lng="latLng"
      >
        <l-popup>
          <strong>{{ activities[index].name }}</strong><br />
           {{ activities[index].location }}<br />
           {{ activities[index].date }}<br />
          <a :href="activities[index].url" target="_blank">More Info</a>
        </l-popup>
      </l-marker>

    </l-map>
    <v-alert v-if="geocodingError" type="error">
      Geocoding error: Unable to fetch coordinates for some activities.
    </v-alert>
  </v-container>
</template>

<script>
import { LMap, LTileLayer, LMarker, LPopup } from "@vue-leaflet/vue-leaflet";
import "leaflet/dist/leaflet.css";
import axios from "axios";

export default {
  name: "MapActivities",
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LPopup,
  },
  props: {
    activities: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      activityCoordinates: [],
      geocodingError: false,
    };
  },
  methods: {
    async fetchCoordinates() {
      const limitedActivities = this.activities.slice(0, 20); // Limit to first 20 activities

      for (const activity of limitedActivities) {
        try {
          const response = await axios.get(
            `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(
              activity.location
            )}&format=json&limit=1`
          );

          const result = response.data[0];
          if (result) {
            const latLng = [result.lat, result.lon];
            this.activityCoordinates.push(latLng);
          } else {
            this.activityCoordinates.push([43.611, 3.877]); // Default to Montpellier
          }
        } catch (error) {
          console.error("Geocoding error:", error);
          this.geocodingError = true;
          this.activityCoordinates.push([43.611, 3.877]); // Default to Montpellier
        }
      }
    },
  },
  watch: {
    activities: {
      immediate: true,
      handler() {
        this.fetchCoordinates();
      },
    },
  },
};
</script>

<style scoped>
/* Optional custom map styles */
</style>
