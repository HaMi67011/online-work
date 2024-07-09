const mongoose = require('mongoose');
const { Schema } = mongoose;

// Define a schema for contact
const contactSchema = new Schema({
    name: {
        type: String,
        required: true,
    },
    email: {
        type: String,
        required: true,
        lowercase: true,
        match: [/^\S+@\S+\.\S+$/, 'Please use a valid email address.']
    },
    subject: {
        type: String,
        required: true,
    },
    message: {
        type: String,
        required: true,
    },
    date: {
        type: Date,
        default: Date.now
    }
});

// Create a model based on the schema
const Contact = mongoose.model('Contact', contactSchema);

// Export the model to be used in other parts of the application
module.exports = Contact;
