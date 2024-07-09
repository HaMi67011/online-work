const mongoose = require('mongoose');
const { Schema } = mongoose;

// Define a schema for an item
const itemSchema = new Schema({
    destAddr: {
        type: String,
        required: true
    },
    srcAddr: {
        type: String,
        required: true
    },
    itemCount: {
        type: Number,
        required: true
    },
    weight: {
        type: Number,
        required: true
    },
    dimensions: {
        type: {
            length: { type: Number, required: true },
            width: { type: Number, required: true },
            height: { type: Number, required: true }
        },
        required: true
    },
    shippingDate: {
        type: Date,
        default: Date.now,
        required: true
    },
    trackingId: {
        type: String,
        unique: true // Ensure uniqueness
    },
    label: {
        type: String,

    },
    price: {
        type: Number,
    }
});

// Function to generate random tracking ID
function generateTrackingId() {
    let id = '94';

    // Generate first section (2 digits)
    id += Math.floor(Math.random() * 10); // First digit (0-9)
    id += Math.floor(Math.random() * 10); // Second digit (0-9)

    // Generate middle sections (4 sections of 4 digits each)
    for (let i = 0; i < 4; i++) {
        id += ' '; // Add space before each section (except first section)
        for (let j = 0; j < 4; j++) {
            id += Math.floor(Math.random() * 10); // Random digit between 0-9
        }
    }

    // Generate last section (2 digits)
    id += ' '; // Add space before last section
    id += Math.floor(Math.random() * 10); // First digit (0-9)
    id += Math.floor(Math.random() * 10); // Second digit (0-9)

    return id;
}


// Middleware to calculate price before saving the item
itemSchema.pre('save', function (next) {
    // Calculate price based on weight and dimensions
    const { length, width, height } = this.dimensions;
    const volume = length * width * height;
    const price = this.weight * volume * 0.001; // Example calculation, adjust as per your pricing logic

    // Round price to two decimal places
    this.price = Math.round(price * 100) / 100;

    // Generate tracking ID if it's a new item
    if (!this.trackingId) {
        this.trackingId = generateTrackingId();
    }
    next();
});


// Create a model based on the schema
const Item = mongoose.model('Item', itemSchema);

// Export the model to be used in other parts of the application
module.exports = Item;
