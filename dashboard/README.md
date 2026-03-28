# PhonePe Analytics Dashboard

A production-grade Streamlit dashboard for analyzing PhonePe transaction, user, and insurance data across India.

## 🚀 Features

- **7 Interactive Pages**
  - 🏠 **Home Dashboard**: KPI overview and key metrics
  - 💰 **Transaction Analytics**: Transaction trends, categories, and state analysis
  - 👥 **User Engagement**: User registration, activation, and device breakdown
  - 🛡️ **Insurance Insights**: Insurance market analysis and penetration metrics
  - 🗺️ **Geographic Analysis**: State-level and regional performance
  - 📊 **Reports & Export**: Data export and report generation

- **Real-time Data Visualization**
  - Interactive Plotly charts
  - Trend analysis with drill-down capability
  - Geographic distribution analysis
  - Comparative metrics

- **Data Export Capabilities**
  - Export to CSV
  - Export to Excel
  - Custom report generation

## 📋 Requirements

- Python 3.8+
- Streamlit 1.28+
- Plotly 5.0+
- Pandas 2.0+

See `requirements.txt` for complete list.

## 🔧 Installation

### 1. Install Dependencies

```bash
cd dashboard
pip install -r requirements.txt
```

### 2. Prepare Data

The dashboard expects CSV files in two locations:
- `../query_results/` - Raw query results
- `../data_extracts/` - Aggregated data files

### 3. Run the Dashboard

```bash
streamlit run app.py
```

The dashboard will open at `http://localhost:8501`

## 📁 Project Structure

```
dashboard/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .streamlit/
│   └── config.toml            # Streamlit configuration
├── config/
│   ├── __init__.py
│   └── constants.py           # App-wide constants
├── pages/
│   ├── home.py               # Home dashboard
│   ├── transactions.py       # Transaction analytics
│   ├── users.py              # User engagement
│   ├── insurance.py          # Insurance insights
│   ├── geographic.py         # Geographic analysis
│   └── reports.py            # Reports & export
├── utils/
│   ├── __init__.py
│   ├── database.py           # Data loading (CSV/DB)
│   ├── cache.py              # Caching utilities
│   ├── formatting.py         # Data formatting
│   ├── charts.py             # Chart generation
│   └── metrics.py            # KPI calculations
└── assets/
    └── style.css             # Custom styling
```

## 🔌 Data Source

### Current: CSV-based
The dashboard loads CSV files from:
- `query_results/` - Contains 23 pre-built query results
- `data_extracts/` - Contains aggregated datasets

### Future: Database Connection
To connect to PostgreSQL/MySQL:
1. Update `utils/database.py` with connection string
2. Create SQL queries in `data/queries/`
3. Update page modules to use database functions

## 📊 Key Queries Used

| Page | Primary Queries |
|------|-----------------|
| Home | Transaction KPIs, User metrics, Insurance overview |
| Transactions | Query_4.1, Query_1.1, Query_1.2 |
| Users | Query_2.1, Query_5.1, Query_2.4 |
| Insurance | Query_3.1, Query_3.3, Query_3.4 |
| Geographic | Query_4.1, Query_1.3, Query_1.4 |

## 🎨 Customization

### Colors
Edit `config/constants.py`:
- `PRIMARY_COLOR` - Main color scheme
- `SECONDARY_COLOR` - Accent color
- `SUCCESS_COLOR` - Positive trends
- `DANGER_COLOR` - Negative trends

### Page Titles
Modify `config/constants.py` dictionary `PAGE_TITLES`

### Chart Styling
Update functions in `utils/charts.py`

## ⚙️ Configuration

### Streamlit Settings
Edit `.streamlit/config.toml`:
- Theme colors
- Page layout
- Upload size limits
- Port configuration

### Logging
Enable debug logging in `app.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🧪 Testing

### Run Tests (if available)
```bash
pytest tests/
```

### Manual Testing Checklist
- [ ] All pages load without errors
- [ ] Charts display correctly
- [ ] Filters update data properly
- [ ] Export functionality works
- [ ] Performance acceptable (< 3s load time)

## 🚀 Deployment

### Streamlit Cloud
1. Push code to GitHub
2. Connect repository to Streamlit Cloud
3. Deploy directly from repo

### Docker
```bash
docker build -t phonepe-dashboard .
docker run -p 8501:8501 phonepe-dashboard
```

### Heroku
Configure `Procfile`:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

## 📈 Performance Optimization

- Streamlit caching with `@st.cache_data`
- CPU-bounded computations optimized
- Large DataFrames loaded selectively
- Chart rendering optimized with Plotly

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError"
**Solution**: Ensure all dependencies in `requirements.txt` are installed
```bash
pip install -r requirements.txt
```

### Issue: "No data available"
**Solution**: Check CSV file paths in `utils/database.py`
```python
# Verify paths exist
echo $PWD/../query_results
echo $PWD/../data_extracts
```

### Issue: Slow page loads
**Solution**: Add filters to reduce data size
- Check `utils/cache.py` TTL settings
- Consider pagination for large datasets

## 📚 Documentation

- Full API documentation in docstrings
- Page-specific guides in respective module headers
- Query specifications in `PHASE_6_DASHBOARD_DEVELOPMENT.md`

## 👥 Support

For issues or features:
1. Check `DEBUGGING_REPORT.md` for known issues
2. Review `PHASE_6_DASHBOARD_DEVELOPMENT.md` for implementation details
3. Check function docstrings in `utils/` modules

## 📝 License

Part of PhonePe Analytics Project - Phase 6

## 🎯 Success Metrics

Expected after deployment:
- ✅ 95%+ dashboard uptime
- ✅ Page load time < 2 seconds
- ✅ Support 10+ concurrent users
- ✅ 99%+ data accuracy vs source

---

**Last Updated**: 2024  
**Status**: Production Ready  
**Version**: 1.0.0
