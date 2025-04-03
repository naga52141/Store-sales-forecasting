# 📊 Store Sales Forecasting Web App  

This project is a web-based application that helps you predict future store sales. It uses a model called SARIMA  to make these predictions. You can easily upload your sales data in a CSV file, and the app will show you both the actual and predicted sales in a chart and table format. It’s like having a secret sales forecasting tool at your fingertips!
---

## 🚀 **Features**
✅ Upload sales data (CSV format)  
✅ Predict future sales using **SARIMA model**  
✅ Display **actual vs. predicted sales** in an interactive **chart**  
✅ View sales data in a **table**  
✅ Supports **dark mode theme**  

---

## 🛠 **Tech Stack**
- **Frontend:** HTML, CSS, JavaScript, Chart.js  
- **Backend:** Node.js, Express.js  
- **Machine Learning:** Python, Pandas, Statsmodels (SARIMA), Prophet  
- **Database:** N/A (Uses CSV files for input)  

---

## 📂 **Project Structure**
```
store-sales-forecasting/
│── backend/
│   │── models/
│   │   ├── sarima.py          # SARIMA model for forecasting
│   │   ├── prophet.py         # Prophet model for forecasting
│   │── uploads/               # Uploaded CSV files
│   │── server.js              # Node.js backend
│── frontend/
│   │── index.html             # Web interface
│   │── styles.css             # Custom styles (Dark mode)
│   │── script.js              # Handles file upload, chart plotting
│── README.md                  # Project documentation
```

---

## 🔧 **Setup Instructions**
### **1️⃣ Install Backend Dependencies**
```bash
cd backend
npm install express multer cors child_process
```

### **2️⃣ Install Python Dependencies**
```bash
pip install pandas statsmodels pmdarima fbprophet
```

### **3️⃣ Start Backend Server**
```bash
node backend/server.js
```
The server will start at **http://localhost:4000**.

### **4️⃣ Open Frontend**
- Open `frontend/index.html` in a browser.

---

## 📤 **Usage**
1️⃣ **Upload a CSV file** (format: `date,sales`)  
2️⃣ **Wait for processing** – The app will run the SARIMA model.  
3️⃣ **View results** – The **chart and table** will show actual & predicted sales.  

---

## 🖥️ **API Endpoints**
### **Upload CSV & Get Forecast**
- **URL:** `POST http://localhost:4000/upload`
- **Request:** Multipart form-data with CSV file  
- **Response:** JSON containing `dates`, `forecast`, `actual_sales`

---

## 📌 **Issues & Fixes**
### ❌ `displayTable is not defined`
🔹 **Fix:** Ensure `displayTable()` is defined before calling it in `script.js`.

### ❌ `Fetch error: TypeError: data.actual_dates is not iterable`
🔹 **Fix:** Modify `sarima.py` to ensure `actual_dates` is properly extracted.

### ❌ Laptop lagging due to repeated charts  
🔹 **Fix:** Destroy existing chart before creating a new one:  
```js
if (window.salesChartInstance) {
    window.salesChartInstance.destroy();
}
```

---

## 🎯 **Future Improvements**
- [ ] Add Prophet model as an alternative  
- [ ] Support real-time data from a database  
- [ ] Allow multiple store forecasting  

---

## 📜 **License**
This project is **open-source** and available for modification.  
Feel free to contribute and improve! 🚀
