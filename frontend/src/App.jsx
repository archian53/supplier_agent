import React, { useState, useEffect } from 'react';
import {
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  Box,
  Alert,
  CircularProgress,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow
} from '@mui/material';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

function App() {
  const [supplierName, setSupplierName] = useState('');
  const [productName, setProductName] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [existingData, setExistingData] = useState([]);

  useEffect(() => {
    fetchExistingData();
  }, []);

  const fetchExistingData = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/data/SUPPLIER_PRODUCTS`);
      setExistingData(response.data.data);
    } catch (err) {
      setError('Failed to load existing data');
      console.error('Error fetching data:', err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(null);

    try {
      const response = await axios.post(`${API_BASE_URL}/generate-entry`, {
        supplier_name: supplierName,
        product_name: productName,
        table_name: 'SUPPLIER_PRODUCTS'
      });

      if (response.data.status === 'success') {
        setSuccess('Entry generated and inserted successfully');
        setSupplierName('');
        setProductName('');
        fetchExistingData();
      } else {
        setError('Failed to generate entry: ' + response.data.message);
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to generate entry');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 4, mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          AI-Powered Data Analysis System
        </Typography>

        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            New Entry
          </Typography>
          <form onSubmit={handleSubmit}>
            <TextField
              fullWidth
              label="Supplier Name"
              value={supplierName}
              onChange={(e) => setSupplierName(e.target.value)}
              margin="normal"
              required
            />
            <TextField
              fullWidth
              label="Product Name"
              value={productName}
              onChange={(e) => setProductName(e.target.value)}
              margin="normal"
              required
            />
            <Box sx={{ mt: 2 }}>
              <Button
                type="submit"
                variant="contained"
                disabled={loading}
                sx={{ mr: 2 }}
              >
                {loading ? <CircularProgress size={24} /> : 'Generate New Entry'}
              </Button>
            </Box>
          </form>

          {error && (
            <Alert severity="error" sx={{ mt: 2 }}>
              {error}
            </Alert>
          )}
          {success && (
            <Alert severity="success" sx={{ mt: 2 }}>
              {success}
            </Alert>
          )}
        </Paper>

        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>
            Existing Data
          </Typography>
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Supplier Name</TableCell>
                  <TableCell>Product Name</TableCell>
                  {existingData[0] && 
                    Object.keys(existingData[0])
                      .filter(key => !['supplier_name', 'product_name'].includes(key))
                      .map(key => (
                        <TableCell key={key}>{key}</TableCell>
                      ))
                  }
                </TableRow>
              </TableHead>
              <TableBody>
                {existingData.map((row, index) => (
                  <TableRow key={index}>
                    <TableCell>{row.supplier_name}</TableCell>
                    <TableCell>{row.product_name}</TableCell>
                    {Object.entries(row)
                      .filter(([key]) => !['supplier_name', 'product_name'].includes(key))
                      .map(([key, value]) => (
                        <TableCell key={key}>{value}</TableCell>
                      ))
                    }
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Paper>
      </Box>
    </Container>
  );
}

export default App;