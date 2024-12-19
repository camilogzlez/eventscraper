<template>
  <div class="tw-fixed tw-inset-0 tw-bg-blue-200/50 tw-flex tw-justify-center tw-items-center tw-z-50">
    <div class="tw-bg-black tw-bg-opacity-40 tw-rounded-lg tw-w-3/4 tw-p-6 tw-shadow-lg">
      <div class="tw-flex tw-justify-between tw-items-center">
        <h2 class="tw-text-xl tw-font-bold">Assistant Activities</h2>
        <button @click="closeModal" class="tw-text-white-500 hover:tw-text-white-700 tw-text-lg">
          ×
        </button>
      </div>

      <v-text-field
        v-model="query"
        label="Ask me about activities"
        @keydown.enter="sendQuery"
        outlined
        class="tw-mt-4"
      ></v-text-field>
      <v-btn @click="sendQuery" color="#72a9fe" class="tw-mt-2">Send</v-btn>

      <!-- ActivitiesGrid with fixed height and scroll -->
      <div class="tw-h-[50vh] tw-overflow-y-auto tw-mt-6">
        <ActivitiesGrid
          v-if="activities.length"
          :activities="activities"
          :show-map="false"
          class="tw-mt-6"
        />
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import ActivitiesGrid from "./ActivitiesGrid.vue";

export default {
  components: { ActivitiesGrid },
  data() {
    return {
      query: "", // Store the user input
      activities: []
    };
  },
  methods: {
    async sendQuery() {
      if (!this.query) return; // Ensure query is not empty

      try {
        const response = await axios.post("https://208e-92-184-105-112.ngrok-free.app/webhook", {
          queryResult: {
            parameters: {
              name: this.query,
            },
            intent: {displayName: "trouve des activites"},
            languageCode: "fr", // Language code
          },
        });
        console.log("Response from webhook:", response.data);
        // Use the activities directly from the response
        this.activities = response.data.activities || [];
      } catch (error) {
        console.error("Error during API call:", error);
      }

      this.query = ""; // Clear input field after sending the query
    },

    closeModal() {
      this.$emit("close"); // Emit close event to parent
    },
  },
};
</script>

<style scoped>
/* Ensure smooth appearance of modal and responsive layout */
.tw-fixed {
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>

<!-- NOTE: pending implementation of conection with dialogflow to send the request to the assistant-->
<!--CODE EXAMPLE:-->
<!--require("dotenv").config(); // Load .env variables at the start of your script-->

<!--methods: {-->
<!--  async sendQuery() {-->
<!--    if (!this.query) return;-->

<!--    try {-->
<!--      const sessionId = "your-session-id"; // Replace with a dynamic generator for production-->
<!--      const token = await getAccessToken();SERVICE TO IMPLEMENT

  const dialogflowUrl = `https://dialogflow.googleapis.com/v2/projects/${process.env.GOOGLE_PROJECT_ID}/agent/sessions/${sessionId}:detectIntent`;-->

<!--      const response = await axios.post(-->
<!--        dialogflowUrl,-->
<!--        {-->
<!--          queryInput: {-->
<!--            text: {-->
<!--              text: this.query,-->
<!--              languageCode: "fr",-->
<!--            },-->
<!--          },-->
<!--        },-->
<!--        {-->
<!--          headers: {-->
<!--            Authorization: `Bearer ${token}`,-->
<!--          },-->
<!--        }-->
<!--      );-->

<!--      console.log("Response from Dialogflow:", response.data);-->
<!--      this.activities = response.data.queryResult.fulfillmentMessages || [];-->
<!--    } catch (error) {-->
<!--      console.error("Error during Dialogflow request:", error);-->
<!--    }-->
<!--  },-->
<!--}-->
