# CampusGo – Smart Campus Navigator 🗺️

🚀 **Live Demo:** [Open CampusGo](https://smart-campus-navigator-8bz9fjzhwwpxyabtofjvbe.streamlit.app/)

A simple web-based campus navigation project built using Python and Streamlit. It helps students explore campus locations and access navigation features through an easy-to-use interface.

## 💡 What Is CampusGo?

Finding classrooms, laboratories, offices, and other campus locations can be confusing, especially for new students.

CampusGo aims to make campus navigation easier by providing a digital interface where users can explore locations and access navigation features.

## ✨ Features

- **Simple Interface:** Easy-to-use dashboard.
- **Campus Locations:** Explore available campus locations.
- **Navigation:** Find routes using the project's stored campus data.
- **Interactive Map:** View locations on a map.
- **Current Location:** Use browser GPS, with the user's permission, where supported.
- **Python Algorithms:** Apply data structures and algorithms to navigation-related tasks.

## ⚙️ How Does It Work?

1. **Open the application:** The CampusGo dashboard appears.
2. **Explore locations:** Select or search for a campus location using the available options.
3. **View the map:** The application displays map information and available navigation details.
4. **Find a route:** The application uses its stored campus data and navigation logic to determine a route.
5. **Use GPS:** If supported, allow location access to view your current location.

## 🛠️ Technologies Used

- **Python** – Main programming language
- **Streamlit** – Web application interface
- **Folium** – Interactive maps
- **streamlit-folium** – Displays Folium maps in Streamlit
- **streamlit-geolocation** – Browser-based location functionality
- **Data Structures and Algorithms** – Navigation and route-related logic

## 📁 Project Structure

```text
Smart-Campus-Navigator/
│
├── app.py
├── algorithms.py
├── campus_data.py
├── trie.py
├── requirements.txt
└── README.md
```

- `app.py` – Main application and user interface.
- `algorithms.py` – Navigation-related algorithms.
- `campus_data.py` – Stored campus location and route data.
- `trie.py` – Trie data structure implementation.
- `requirements.txt` – Required Python packages.
- `README.md` – Project documentation.

## 🚀 How to Run the Project

### 1. Install Python

Install Python on your computer if it is not already installed.

### 2. Download the project

Clone the repository or download it from GitHub.

```bash
git clone https://github.com/Manorama0310/Smart-Campus-Navigator.git
```

### 3. Open the project folder

```bash
cd Smart-Campus-Navigator
```

### 4. Install the required packages

```bash
python -m pip install -r requirements.txt
```

### 5. Start the application

```bash
python -m streamlit run app.py
```

The application will open in your browser. If it does not open automatically, visit `http://localhost:8501`.

## 🎯 Project Objective

The main objective of CampusGo is to demonstrate how Python, data structures, algorithms, and interactive maps can be combined to build a simple campus navigation application.

## ⚠️ Limitations

- Navigation depends on the accuracy and completeness of the stored campus data.
- GPS requires browser permission and a supported environment.
- Accurate real-world walking directions require verified campus coordinates and paths.

## 🔮 Future Improvements

- Add verified campus buildings and walking paths.
- Improve location search and route calculation.
- Add more campus locations.
- Make the application more accessible for new students.

## 👩‍💻 Project Information

**Project Name:** CampusGo – Smart Campus Navigator  
**Project Type:** DSA Mini Project  
**Language:** Python  
**Interface:** Streamlit

---

*CampusGo aims to make exploring a campus simpler, smarter, and more convenient for students.*
