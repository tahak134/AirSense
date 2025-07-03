const functions = require("firebase-functions");
const admin = require("firebase-admin");
const axios = require("axios");

admin.initializeApp();

exports.sendSensorDataToDjango = functions.database
    .ref("/sensor_readings/{pushId}")
    .onCreate(async (snapshot, context) => {
      const data = snapshot.val();

      try {
        const response = await axios.post("https://3b06-125-62-91-34.ngrok-free.app", data);
        console.log("Data sent successfully to Django:", response.data);
      } catch (error) {
        console.error("Error sending data to Django:", error.message);
      }
    });
