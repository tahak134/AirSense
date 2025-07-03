import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getDatabase } from "firebase/database";
import { getFirestore } from "firebase/firestore";

const firebaseConfig = {
  apiKey: "AIzaSyBrdK-GF17BckvZ4l_cVv2MiNDdgeuHGA8",
  authDomain: "aq-monitoring-58f8a.firebaseapp.com",
  databaseURL: "https://aq-monitoring-58f8a-default-rtdb.firebaseio.com",
  projectId: "aq-monitoring-58f8a",
  storageBucket: "aq-monitoring-58f8a.appspot.com",
  messagingSenderId: "398240725362",
  appId: "1:398240725362:web:26371c46f00d0b397fc5eb"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const database = getDatabase(app);
const firestore = getFirestore(app);

export { app, auth, database, firestore };