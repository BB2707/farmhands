# farmhands# 🌾 Farmhands – AI-Powered Crop Health & Recommendation Assistant

**Farmhands** is an open-source AI + IoT platform that empowers small-scale farmers with real-time crop health diagnostics and smart crop planning. By combining computer vision, IoT soil sensors, climate mapping, and market intelligence, Farmhands provides actionable insights that help farmers maximize yield and reduce uncertainty.

---

## 🧠 Features

- 📸 Crop image analysis using deep learning (CNN)
- 🌱 Real-time soil condition monitoring (moisture & pH)
- 🛰️ Satellite-based environmental context via Google Earth Engine
- 📊 Dynamic crop recommendations based on soil, weather & market price
- 📱 Mobile + web UI for farmers (React.js frontend)
- 🧪 ML prototyping using Google Teachable Machine

---

## 🛠️ Tech Stack

| Component         | Technology                      |
|------------------|----------------------------------|
| AI Model         | TensorFlow/Keras (Python)        |
| ML Prototyping   | Google Teachable Machine         |
| IoT Integration  | Arduino / ESP32 + Soil Sensors   |
| GIS Mapping      | Google Earth Engine (Python/JS)  |
| Backend API      | Node.js + Express.js             |
| Frontend         | React.js                         |
| Database         | MongoDB (hosted on MongoDB Atlas)|
| Image Storage    | Cloudinary or Firebase Storage   |

---

## 📂 Datasets Used

- [New Plant Diseases Dataset (Kaggle)](https://www.kaggle.com/datasets/vipoooool/new-plant-diseases-dataset)  
- [PlantDoc Dataset (GitHub)](https://github.com/pratikkayal/PlantDoc-Dataset)  
- [Paddy Doctor Dataset (arXiv)](https://arxiv.org/abs/2205.11108)

These datasets are open-source and used to train the crop health classification model.

---

## 📦 Installation & Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/Farmhands.git
cd Farmhands

# Install backend dependencies
cd backend
npm install

# Install frontend dependencies
cd ../frontend
npm install

# Run the backend server
cd ../backend
npm run start

# Run the frontend app
cd ../frontend
npm run start


graph TD
A[Crop Image Upload] --> B[CNN Model (TensorFlow)]
C[IoT Soil Sensors] --> E[Node.js Backend]
D[Google Earth Engine] --> E
B --> E[Crop Recommendation Engine]
F[Government Crop Price APIs] --> E
E --> G[React.js Farmer Dashboard]



🚀 Use Cases
Diagnosing crop diseases before symptoms spread

Planning next crops based on real-time data

Helping smallholder farmers without agronomy access

Bridging AI/IoT for grassroots agricultural impact



📈 Performance Goals
✅ 85%+ crop disease classification accuracy

✅ Soil data refresh every 15 minutes

✅ 60% faster decision-making over manual methods

✅ 80%+ user satisfaction from field tests



🔮 Future Roadmap
🌍 Voice support in regional languages

🌦️ Weather API integration for pest prediction

📶 GSM-based IoT modules for offline villages

🧠 Reinforcement learning for crop rotation planning

🧩 Integrate with farmer co-operative dashboards



🙌 Acknowledgements
TensorFlow Team

Google Earth Engine

Indian Government Agmarknet API

PlantDoc, PlantVillage & PaddyDoctor Datasets


---

Let me know if you want the `backend/`, `frontend/`, and `iot/` folder structures scaffolded too — or if you want this converted into a live GitHub repo with setup!




