const express = require('express');
const mongoose = require('mongoose');
const path = require('path');
const Item = require('./item_schema'); // Adjust the path as per your project structure
const Contact = require('./contact_schema'); // Adjust the path as per your project structure

const app = express();
const port = 3000;

// Middleware to parse incoming JSON data
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Middleware to serve static files
app.use(express.static(path.join(__dirname, 'public')));

// Connect to MongoDB using Mongoose
const mongoURI = 'mongodb+srv://hamzaansari6060:MCoGLKAyr90uiWIQ@sna.cw74cqx.mongodb.net/?retryWrites=true&w=majority&appName=Sna';

mongoose.connect(mongoURI, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
})
    .then(() => {
        console.log('MongoDB connected');

        // Create a new Item instance
        const newItem = new Item({
            destAddr: 'Destination Address',
            srcAddr: 'Source Address',
            itemCount: 1,
            weight: 2.5,
            dimensions: {
                length: 10,
                width: 5,
                height: 3
            },
            shippingDate: new Date(),
            // No need to set trackingId or price here, they will be set automatically
        });

        // Save the new item to the database
        newItem.save()
            .then(savedItem => {
                console.log('Item saved:', savedItem);
            })
            .catch(error => {
                console.error('Error saving item:', error);
            });

    })
    .catch(err => console.error('MongoDB connection error:', err));

// Route to handle form submission for contact
app.post('/contact', async (req, res) => {
    try {
        const { name, email, subject, message } = req.body;
        const newContact = new Contact({ name, email, subject, message });
        await newContact.save();
        res.status(201).send('Contact data saved successfully');
    } catch (error) {
        res.status(500).send('Error saving contact data: ' + error.message);
    }
});

// Catch-all route to serve index.html for any other routes
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}/`);
});
